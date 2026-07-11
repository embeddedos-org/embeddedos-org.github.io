#!/usr/bin/env python3
"""
tests/run_all_tests.py — Master test runner
SPDX-License-Identifier: MIT  Copyright (c) 2026 EmbeddedOS Foundation

Runs all 9 test categories and produces a comprehensive report.
Usage:  python3 tests/run_all_tests.py
"""
import sys, time, unittest, io
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

SITE_ROOT = Path(__file__).parent.parent

CATEGORIES = [
    ("1. Unit Tests",        "tests.unit.test_unit_core"),
    ("2. Integration Tests", "tests.integration.test_integration"),
    ("3. Functional Tests",  "tests.functional.test_functional_e2e"),
    ("4. E2E Tests",         "tests.functional.test_functional_e2e"),
    ("5. Security Tests",    "tests.security.test_security"),
    ("6. Performance Tests", "tests.performance.test_performance_benchmarks"),
    ("7. Smoke Tests",       "tests.smoke.test_smoke"),
    ("8. Regression Tests",  "tests.regression.test_regression"),
    ("9. UI/UX Tests",       "tests.ui_ux.test_ui_ux"),
]

BANNER = "=" * 70

def run_category(label, module_path):
    loader = unittest.TestLoader()
    try:
        suite = loader.loadTestsFromName(module_path)
    except Exception as e:
        return {"label": label, "run": 0, "errors": 0, "failures": 1, "skipped": 0,
                "load_error": str(e), "elapsed": 0.0, "details": str(e)}

    buf = io.StringIO()
    runner = unittest.TextTestRunner(stream=buf, verbosity=2)
    t0 = time.perf_counter()
    result = runner.run(suite)
    elapsed = time.perf_counter() - t0

    return {
        "label": label,
        "run": result.testsRun,
        "errors": len(result.errors),
        "failures": len(result.failures),
        "skipped": len(result.skipped),
        "elapsed": elapsed,
        "details": buf.getvalue(),
        "load_error": None,
    }

def main():
    print(BANNER)
    print("  EmbeddedOS Website — Comprehensive Test Suite")
    print(f"  Site root: {SITE_ROOT}")
    print(BANNER)

    results = []
    seen_modules = set()
    for label, module in CATEGORIES:
        if module in seen_modules:
            # E2E reuses functional module — just clone the result
            prev = next(r for r in results if r.get("_module") == module)
            r = dict(prev); r["label"] = label
            results.append(r); continue
        seen_modules.add(module)
        print(f"\n{'─'*70}")
        print(f"  Running: {label}")
        print(f"{'─'*70}")
        r = run_category(label, module)
        r["_module"] = module
        results.append(r)
        status = "PASS" if r["failures"] == 0 and r["errors"] == 0 else "FAIL"
        print(f"  {status}  {r['run']} tests  |  {r['failures']} failures  |  {r['errors']} errors  |  {r['elapsed']:.2f}s")

    # ── Summary ──────────────────────────────────────────────────────────────
    print(f"\n{BANNER}")
    print("  FINAL SUMMARY")
    print(BANNER)
    total_run = total_fail = total_err = total_skip = 0
    all_pass = True
    for r in results:
        total_run  += r["run"]
        total_fail += r["failures"]
        total_err  += r["errors"]
        total_skip += r["skipped"]
        status = "✓ PASS" if r["failures"] == 0 and r["errors"] == 0 else "✗ FAIL"
        if r["failures"] > 0 or r["errors"] > 0:
            all_pass = False
        print(f"  {status}  {r['label']:<30} {r['run']:>3} tests  {r['failures']:>2} fail  {r['errors']:>2} err  {r['elapsed']:.2f}s")

    print(BANNER)
    print(f"  TOTAL: {total_run} tests  |  {total_fail} failures  |  {total_err} errors  |  {total_skip} skipped")
    print(f"  RESULT: {'ALL TESTS PASSED ✓' if all_pass else 'SOME TESTS FAILED ✗'}")
    print(BANNER)

    # ── Failure details ───────────────────────────────────────────────────────
    if not all_pass:
        print("\n  FAILURE DETAILS:")
        for r in results:
            if r["failures"] > 0 or r["errors"] > 0:
                print(f"\n  [{r['label']}]")
                for line in r["details"].splitlines():
                    if "FAIL:" in line or "ERROR:" in line or "AssertionError" in line:
                        print(f"    {line}")

    return 0 if all_pass else 1

if __name__ == "__main__":
    sys.exit(main())
