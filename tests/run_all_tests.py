#!/usr/bin/env python3
"""
Main test runner for FHIR API tests
Runs selected test suites and provides comprehensive reporting
"""
import sys
import time
import argparse
from test_utils import Colors, TestResults
from test_organization import run_organization_tests
from test_practitioner import run_practitioner_tests
from test_patient import run_patient_tests
from config import BASE_URL


def print_header(scenarios):
    """Print test suite header"""
    print(f"\n{Colors.BOLD}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}FHIR API Test Suite{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*70}{Colors.RESET}")
    print(f"\nTesting against: {Colors.BLUE}{BASE_URL}{Colors.RESET}")
    print(f"Scenarios: {Colors.CYAN}{', '.join(scenarios)}{Colors.RESET}\n")


def print_separator():
    """Print separator between test suites"""
    print(f"\n{Colors.BOLD}{'-'*70}{Colors.RESET}\n")


def aggregate_results(all_results: list) -> TestResults:
    """Aggregate results from multiple test suites"""
    total = TestResults()
    for results in all_results:
        total.passed += results.passed
        total.failed += results.failed
        total.skipped += results.skipped
        total.failures.extend(results.failures)
    return total


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Run FHIR API test scenarios',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_all_tests.py                    # Run all scenarios
  python run_all_tests.py organization       # Run only organization tests
  python run_all_tests.py patient practitioner  # Run patient and practitioner tests
  python run_all_tests.py org pract pat      # Short names also work
        """
    )
    parser.add_argument(
        'scenarios',
        nargs='*',
        choices=['organization', 'org', 'practitioner', 'pract', 'patient', 'pat', 'all'],
        help='Scenarios to run (organization, practitioner, patient, or all). Short names accepted (org, pract, pat).'
    )
    return parser.parse_args()


def normalize_scenarios(scenarios):
    """Normalize scenario names and handle 'all'"""
    # Map short names to full names
    name_map = {
        'org': 'organization',
        'pract': 'practitioner',
        'pat': 'patient',
        'organization': 'organization',
        'practitioner': 'practitioner',
        'patient': 'patient'
    }

    # If no scenarios specified or 'all' is specified, run all
    if not scenarios or 'all' in scenarios:
        return ['organization', 'practitioner', 'patient']

    # Normalize and deduplicate
    normalized = []
    for scenario in scenarios:
        full_name = name_map.get(scenario.lower())
        if full_name and full_name not in normalized:
            normalized.append(full_name)

    return normalized


def main():
    """Run selected test suites"""
    args = parse_args()
    scenarios = normalize_scenarios(args.scenarios)

    print_header(scenarios)

    start_time = time.time()
    all_results = []

    # Available test scenarios
    test_scenarios = {
        'organization': ('Organization', run_organization_tests),
        'practitioner': ('Practitioner/PractitionerRole', run_practitioner_tests),
        'patient': ('Patient', run_patient_tests)
    }

    # Run selected scenarios
    for scenario in scenarios:
        if scenario not in test_scenarios:
            continue

        name, test_func = test_scenarios[scenario]
        try:
            results = test_func()
            all_results.append(results)
            if scenario != scenarios[-1]:  # Don't print separator after last test
                print_separator()
        except Exception as e:
            print(f"{Colors.RED}{name} tests failed with exception: {e}{Colors.RESET}")
            sys.exit(1)

    # Aggregate and print final results
    elapsed_time = time.time() - start_time
    total_results = aggregate_results(all_results)

    print(f"\n{Colors.BOLD}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}Overall Test Results{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*70}{Colors.RESET}")
    print(f"\nTest Suites Run: {len(all_results)}")
    print(f"Time Elapsed: {elapsed_time:.2f} seconds")

    total_results.print_summary()

    # Exit with appropriate code
    exit_code = 0 if total_results.failed == 0 else 1

    if exit_code == 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ All tests passed!{Colors.RESET}\n")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}✗ Some tests failed{Colors.RESET}\n")

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
