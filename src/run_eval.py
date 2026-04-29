import json

try:
    from .eval_harness import DEFAULT_CASES, run_suite
except ImportError:  # Allows running as a script
    from eval_harness import DEFAULT_CASES, run_suite


def main() -> None:
    results = run_suite(DEFAULT_CASES)
    passed = sum(1 for r in results if r.passed)
    total = len(results)
    print(f"Eval: {passed}/{total} passed")
    for r in results:
        status = "PASS" if r.passed else "FAIL"
        print(f"- {status}: {r.case.name} ({json.dumps(r.checks)})")


if __name__ == "__main__":
    main()
