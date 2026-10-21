"""No external dependencies; anonymized regression tests for the ISC method."""
import math
import os
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import analyze as analyzer


def record(i, delta, rated=True, place="A"):
    return {
        "row": i + 5, "name": "Participant " + str(i),
        "rank": i + 1, "rank_text": str(i + 1),
        "country": "", "location": place, "category": "1",
        "prior_rating": 2000.0 if rated else None,
        "performance_rating": 2000.0 + delta if rated else 1000.0,
        "delta": float(delta) if rated else 0.0,
        "excel_delta": None, "cached_z": None, "cached_p": None,
    }


def group(records, mr=None, sr=None):
    return {
        "name": "Example", "title": "", "records": records,
        "mean_range": mr, "sd_range": sr, "excel_mu": None, "excel_sd": None,
    }


class EmpiricalZTests(unittest.TestCase):
    def test_locale_numbers(self):
        self.assertEqual(analyzer.number("2 734,47"), 2734.47)
        self.assertEqual(analyzer.number("2,734.47"), 2734.47)
        self.assertIsNone(analyzer.number("–"))

    def test_verified_isc_2025_excel_reference(self):
        mu = -6.867068965517231
        sd = 216.28673810324122
        z = (890.97 - mu) / sd
        self.assertAlmostEqual(z, 4.151142491857027, places=7)
        p = math.erfc(z / math.sqrt(2)) / 2
        self.assertAlmostEqual(p, 0.00001654098560843753, places=11)

    def test_high_outlier_meets_four_conditions(self):
        entries = [record(0, 500)] + [record(i, 0) for i in range(1, 15)]
        meta, calculated = analyzer.analyze(group(entries))
        self.assertEqual(meta["participant_count"], 15)
        self.assertAlmostEqual(calculated[0]["z_historical"], math.sqrt(14))
        self.assertTrue(calculated[0]["strict_four_flags"])
        self.assertEqual(calculated[0]["difference_band"], "violet")
        self.assertTrue(calculated[0]["flag_rank20"])
        self.assertEqual(calculated[0]["venue_or_cohort_n"], 15)

    def test_missing_rating_sensitivity(self):
        entries = [record(0, 500), record(1, 0), record(2, 0, rated=False)]
        meta, calculated = analyzer.analyze(group(entries))
        self.assertEqual(meta["without_prior_rating"], 1)
        self.assertAlmostEqual(meta["mu_historical"], 500/3)
        self.assertAlmostEqual(meta["mu_rated_only"], 250)
        self.assertNotAlmostEqual(calculated[0]["z_historical"], calculated[0]["z_rated_only"])

    def test_mismatched_formula_ranges_are_detected(self):
        entries = [record(0, 300), record(1, 200), record(2, -50)]
        meta, _ = analyzer.analyze(group(entries, (5, 6), (5, 7)))
        self.assertNotEqual(meta["mean_sample_size"], meta["sd_sample_size"])
        self.assertTrue(any("different row ranges" in w for w in meta["warnings"]))

    def test_missing_local_group_is_not_automatically_approved(self):
        entries = [record(i, 0, place=("A" if i < 8 else "B")) for i in range(15)]
        _, calculated = analyzer.analyze(group(entries))
        self.assertFalse(calculated[0]["flag_n14"])

    @unittest.skipUnless(os.environ.get("ISC_WORKBOOK"), "Supply ISC_WORKBOOK path for original-file integration")
    def test_original_workbook_reference_values(self):
        sheets = analyzer.load_xlsx(os.environ["ISC_WORKBOOK"])
        a, r = analyzer.analyze(analyzer.xlsx_group("ISC 2025", sheets["ISC 2025"]))
        self.assertAlmostEqual(r[0]["z_historical"], 4.151142491857027, places=4)
        self.assertEqual(a["without_prior_rating"], 12)
        _, records = analyzer.analyze(analyzer.xlsx_group("ISC 2026", sheets["ISC 2026"]))
        target = next(x for x in records if x["row"] == 10)
        self.assertAlmostEqual(target["z_historical"], 5.086752659656939, places=4)
        self.assertIn("WCSC 2024", sheets)


if __name__ == "__main__":
    unittest.main()
