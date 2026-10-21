#!/usr/bin/env python3
"""ISC / chess-solving result auditor. Python standard library only.

Reads cached XLSX values (does not recalculate Excel formulas) or normalized CSV.
Produces a reproducible copy of the workbook's empirical Z method and a
rated-only sensitivity analysis. No accusation is made from statistics.
"""
import argparse
import collections
import csv
import json
import math
import pathlib
import re
import statistics
import xml.etree.ElementTree as ET
import zipfile

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def number(value):
    if value is None or str(value).strip() in ("", "-", "–", "—"):
        return None
    s = str(value).strip().replace("\u00a0", "").replace(" ", "")
    if "," in s and "." in s:
        s = s.replace(".", "") if s.rfind(",") > s.rfind(".") else s.replace(",", "")
    return float(s.replace(",", "."))


def col(ref):
    return re.match(r"[A-Z]+", ref).group()


def row_index(ref):
    return int(re.search(r"\d+", ref).group())


def cell_value(cell, strings):
    value = cell.find("m:v", NS)
    if cell.get("t") == "inlineStr":
        return "".join(x.text or "" for x in cell.findall(".//m:t", NS))
    if value is None:
        return ""
    if cell.get("t") == "s":
        return strings[int(value.text)]
    return value.text or ""


def load_xlsx(path):
    with zipfile.ZipFile(path) as book:
        strings = []
        if "xl/sharedStrings.xml" in book.namelist():
            root = ET.fromstring(book.read("xl/sharedStrings.xml"))
            strings = [
                "".join(x.text or "" for x in el.findall(".//m:t", NS))
                for el in root.findall("m:si", NS)
            ]
        workbook = ET.fromstring(book.read("xl/workbook.xml"))
        relationships = ET.fromstring(book.read("xl/_rels/workbook.xml.rels"))
        targets = {rel.get("Id"): rel.get("Target").lstrip("/") for rel in relationships}
        sheets = {}
        for sheet in workbook.findall("m:sheets/m:sheet", NS):
            name = sheet.get("name")
            target = targets[sheet.get("{" + REL + "}id")]
            filename = target if target.startswith("xl/") else "xl/" + target
            root = ET.fromstring(book.read(filename))
            rows = {}
            for row in root.findall("m:sheetData/m:row", NS):
                cells = {}
                for c in row.findall("m:c", NS):
                    f = c.find("m:f", NS)
                    cells[col(c.get("r"))] = {
                        "value": cell_value(c, strings),
                        "formula": f.text if f is not None else None,
                    }
                rows[int(row.get("r"))] = cells
            sheets[name] = rows
        return sheets


def locate_headers(rows):
    headers = {k: v["value"].strip().lower() for k, v in rows.get(2, {}).items()}
    def find(predicate):
        return next((k for k, text in headers.items() if predicate(text)), None)
    name = find(lambda s: s == "name")
    prior = find(lambda s: s == "rating")
    perf = find(lambda s: "perf" in s and "rat" in s)
    rank = find(lambda s: s == "rank")
    place = find(lambda s: s == "location")
    country = find(lambda s: s == "country")
    category = find(lambda s: s == "cat.")
    mheaders = {k: v["value"].lower().strip() for k, v in rows.get(4, {}).items()}
    diff = next((k for k, s in mheaders.items() if "difference" in s or "perf - rating" in s or "perf -rating" in s), None)
    z = next((k for k, s in mheaders.items() if "z-score" in s), None)
    mean = next((k for k, s in mheaders.items() if "μδ" in s or "µδ" in s), None)
    sigma = next((k for k, s in mheaders.items() if "σδ" in s), None)
    prob = next((k for k, s in mheaders.items() if "probability" in s), None)
    if not (name and prior and perf and rank):
        raise ValueError("Missing necessary Rank/Name/Rating/Perf. Rat. headers")
    return locals()


def cached(cells, key):
    return number(cells.get(key, {}).get("value")) if key else None


def rank_number(value):
    match = re.match(r"^\s*(\d+)", str(value or ""))
    return int(match.group(1)) if match else None


def excel_range(rows, func):
    for cell in rows.get(5, {}).values():
        f = cell.get("formula") or ""
        if func in f:
            m = re.search(r"([A-Z]+)(\d+):([A-Z]+)(\d+)", f)
            return (int(m.group(2)), int(m.group(4))) if m else None
    return None


def xlsx_group(name, rows):
    hdr = locate_headers(rows)
    participants = []
    for r, cells in sorted(rows.items()):
        if r < 5:
            continue
        person = cells.get(hdr["name"], {}).get("value", "").strip()
        rank_text = cells.get(hdr["rank"], {}).get("value", "")
        rank = rank_number(rank_text)
        if not person or rank is None:
            continue
        performance = cached(cells, hdr["perf"])
        if performance is None:
            continue
        prior = cached(cells, hdr["prior"])
        delta = performance - prior if prior is not None else 0.0
        excel_delta = cached(cells, hdr["diff"])
        participants.append({
            "row": r, "name": person, "rank": rank, "rank_text": rank_text,
            "country": cells.get(hdr["country"], {}).get("value", "") if hdr["country"] else "",
            "location": cells.get(hdr["place"], {}).get("value", "") if hdr["place"] else "",
            "category": cells.get(hdr["category"], {}).get("value", "") if hdr["category"] else "",
            "prior_rating": prior, "performance_rating": performance,
            "delta": delta, "excel_delta": excel_delta,
            "cached_z": cached(cells, hdr["z"]),
            "cached_p": cached(cells, hdr["prob"]),
        })
    title = rows.get(1, {}).get("A", {}).get("value", "")
    return {
        "name": name, "title": title, "records": participants,
        "mean_range": excel_range(rows, "AVERAGE("),
        "sd_range": excel_range(rows, "STDEV.P("),
        "excel_mu": cached(rows.get(5, {}), hdr["mean"]),
        "excel_sd": cached(rows.get(5, {}), hdr["sigma"]),
    }


def csv_group(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        sample = f.read(2048)
        f.seek(0)
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        rows = list(csv.DictReader(f, dialect=dialect))
    rec = []
    for i, row in enumerate(rows, start=2):
        performance = number(row.get("performance_rating"))
        if performance is None:
            continue
        prior = number(row.get("prior_rating"))
        rank = rank_number(row.get("rank"))
        rec.append({
            "row": i, "name": row.get("name", ""), "rank": rank,
            "rank_text": row.get("rank", ""), "country": row.get("country", ""),
            "location": row.get("location", ""), "category": row.get("category", ""),
            "prior_rating": prior, "performance_rating": performance,
            "delta": performance - prior if prior is not None else 0.0,
            "excel_delta": None, "cached_z": None, "cached_p": None,
        })
    return {
        "name": pathlib.Path(path).stem, "title": "",
        "records": rec, "mean_range": None, "sd_range": None,
        "excel_mu": None, "excel_sd": None,
    }


def stats(vals):
    if not vals:
        return None, None
    mu = statistics.fmean(vals)
    sd = math.sqrt(statistics.fmean([(v - mu) ** 2 for v in vals]))
    return mu, sd


def analyze(group):
    all_rec = group["records"]
    warnings = []
    def within(span, record):
        return span is None or span[0] <= record["row"] <= span[1]
    mean_rows = [r["delta"] for r in all_rec if within(group["mean_range"], r)]
    sd_rows = [r["delta"] for r in all_rec if within(group["sd_range"], r)]
    mu = stats(mean_rows)[0]
    sd = stats(sd_rows)[1]
    valid = [r["delta"] for r in all_rec if r["prior_rating"] is not None]
    mu_rated, sd_rated = stats(valid)
    if group["mean_range"] != group["sd_range"]:
        warnings.append("Excel mean and SD reference different row ranges; reproduced separately")
    included = len(mean_rows)
    if included < len(all_rec):
        warnings.append("Historical Excel mean range omits some ranked participants")
    without = sum(r["prior_rating"] is None for r in all_rec)
    if without:
        warnings.append("Missing initial ratings become delta=0 in historical method; rated-only sensitivity also shown")
    if group["excel_mu"] is not None and mu is not None and abs(mu - group["excel_mu"]) > 0.05:
        warnings.append("Computed mean differs from workbook cached mean; inspect formulas/cached values")
    if group["excel_sd"] is not None and sd is not None and abs(sd - group["excel_sd"]) > 0.05:
        warnings.append("Computed SD differs from workbook cached SD; inspect formulas/cached values")
    counts = collections.Counter((r["location"], r["category"]) for r in all_rec) if any(r["location"] for r in all_rec) else None
    for r in all_rec:
        zr = (r["delta"] - mu) / sd if sd and mu is not None else None
        za = (r["delta"] - mu_rated) / sd_rated if sd_rated and mu_rated is not None and r["prior_rating"] is not None else None
        p = math.erfc(zr / math.sqrt(2)) / 2 if zr is not None else None
        venue_n = counts[(r["location"], r["category"])] if counts and r["location"] else (len(all_rec) if counts is None else None)
        r.update({
            "z_historical": zr, "z_rated_only": za,
            "p_upper_tail": p, "one_in": 1 / p if p and p > 0 else None,
            "difference_band": ("green" if r["delta"] < 200 else "yellow" if r["delta"] <= 300
                                else "red" if r["delta"] <= 400 else "violet"),
            "z_band": ("green" if zr is not None and zr < 2 else "red" if zr is not None and zr <= 3 else "violet" if zr is not None else "unknown"),
            "probability_band": ("under_1_percent" if p is not None and p < .01 and r["delta"] > 0
                                 else "under_2_percent" if p is not None and p < .02 and r["delta"] > 0
                                 else "none"),
            "precheck_z3": zr is not None and zr >= 3,
            "flag_z35": zr is not None and zr >= 3.5,
            "flag_delta450": r["delta"] >= 450,
            "flag_rank20": r["rank"] is not None and r["rank"] <= 20,
            "venue_or_cohort_n": venue_n,
            "flag_n14": venue_n is not None and venue_n >= 14,
            "strict_four_flags": (zr is not None and zr >= 3.5 and r["delta"] >= 450
                                  and r["rank"] is not None and r["rank"] <= 20 and venue_n is not None and venue_n >= 14),
            "cached_z_difference": zr - r["cached_z"] if zr is not None and r["cached_z"] is not None else None,
        })
    mismatches = [r for r in all_rec if r["cached_z_difference"] is not None and abs(r["cached_z_difference"]) > .02]
    if mismatches:
        warnings.append(str(len(mismatches)) + " Excel cached Z scores differ by more than 0.02")
    delta_mismatch = [r for r in all_rec if r["excel_delta"] is not None and abs(r["excel_delta"] - r["delta"]) > .05]
    if delta_mismatch:
        warnings.append(str(len(delta_mismatch)) + " cached Excel differences disagree with performance minus prior rating")
    if group["title"] and group["name"].startswith("ISC 20"):
        yr = re.search(r"20\d\d", group["name"])
        if yr and yr.group() not in group["title"]:
            warnings.append("Sheet name and embedded event title disagree")
    summary = {
        "sheet": group["name"], "title": group["title"],
        "model": "in-event empirical delta Z; STDEV.P",
        "participant_count": len(all_rec), "mean_sample_size": len(mean_rows),
        "sd_sample_size": len(sd_rows), "without_prior_rating": without,
        "mu_historical": mu, "sd_historical": sd, "mu_rated_only": mu_rated,
        "sd_rated_only": sd_rated,
        "cached_excel_mu": group["excel_mu"], "cached_excel_sd": group["excel_sd"],
        "mean_range": group["mean_range"], "sd_range": group["sd_range"],
        "max_z": max((r["z_historical"] for r in all_rec if r["z_historical"] is not None), default=None),
        "z35_count": sum(r["flag_z35"] for r in all_rec),
        "four_flags_count": sum(r["strict_four_flags"] for r in all_rec),
        "warnings": warnings,
        "notice": "Statistical flag only; not proof of cheating or an official WFCC finding.",
    }
    return summary, all_rec


def output(group, folder):
    summary, rows = analyze(group)
    folder.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", group["name"].lower()).strip("-")
    (folder / (slug + "-summary.json")).write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    if rows:
        with open(folder / (slug + "-analysis.csv"), "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    return summary


def main():
    parser = argparse.ArgumentParser(description="Chess solving empirical Z model with audit checks")
    parser.add_argument("file", help="XLSX workbook or normalized CSV")
    parser.add_argument("--sheet", help="Select a specific Excel sheet")
    parser.add_argument("--all", action="store_true", help="Analyze every Excel sheet")
    parser.add_argument("--output-dir", default="chess-analysis")
    args = parser.parse_args()
    if args.file.lower().endswith(".csv"):
        groups = [csv_group(args.file)]
    else:
        sheets = load_xlsx(args.file)
        names = list(sheets) if args.all else [args.sheet or next(iter(sheets))]
        groups = [xlsx_group(name, sheets[name]) for name in names]
    result = [output(group, pathlib.Path(args.output_dir)) for group in groups]
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
