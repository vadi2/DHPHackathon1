"""
Utility functions for FHIR API tests
"""
import requests
import json
from typing import Dict, Any, Optional, List
from config import BASE_URL, REQUEST_TIMEOUT, VERBOSE


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'


class TestResults:
    """Track test results"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.failures = []

    def add_pass(self, test_name: str):
        self.passed += 1
        print(f"{Colors.GREEN}✓{Colors.RESET} {test_name}")

    def add_fail(self, test_name: str, reason: str):
        self.failed += 1
        self.failures.append((test_name, reason))
        print(f"{Colors.RED}✗{Colors.RESET} {test_name}: {reason}")

    def add_skip(self, test_name: str, reason: str):
        self.skipped += 1
        print(f"{Colors.YELLOW}⊘{Colors.RESET} {test_name}: {reason}")

    def print_summary(self):
        print(f"\n{Colors.BOLD}Test Summary{Colors.RESET}")
        print(f"{'='*60}")
        print(f"Passed:  {Colors.GREEN}{self.passed}{Colors.RESET}")
        print(f"Failed:  {Colors.RED}{self.failed}{Colors.RESET}")
        print(f"Skipped: {Colors.YELLOW}{self.skipped}{Colors.RESET}")
        print(f"Total:   {self.passed + self.failed + self.skipped}")

        if self.failures:
            print(f"\n{Colors.RED}Failed Tests:{Colors.RESET}")
            for test_name, reason in self.failures:
                print(f"  - {test_name}: {reason}")

        return self.failed == 0


def highlight_json_field(obj: Any, highlight_paths: List[str] = None, current_path: str = "") -> str:
    """
    Convert object to JSON string with highlighted paths.
    highlight_paths: List of JSON paths to highlight (e.g., ['name', 'identifier[0].value'])
    """
    if highlight_paths is None:
        highlight_paths = []

    def should_highlight(path: str) -> bool:
        """Check if current path matches any highlight pattern"""
        for hp in highlight_paths:
            # Simple match or prefix match
            if path == hp or path.startswith(hp + ".") or hp.startswith(path + "."):
                return True
        return False

    def format_value(val: Any, path: str, indent: int = 0) -> str:
        """Recursively format value with highlighting"""
        spaces = "  " * indent
        highlighted = should_highlight(path)

        if isinstance(val, dict):
            if not val:
                return "{}"
            lines = ["{"]
            for i, (k, v) in enumerate(val.items()):
                new_path = f"{path}.{k}" if path else k
                comma = "," if i < len(val) - 1 else ""
                formatted_v = format_value(v, new_path, indent + 1)
                key_color = Colors.CYAN if highlighted else ""
                reset = Colors.RESET if highlighted else ""
                lines.append(f"{spaces}  {key_color}\"{k}\"{reset}: {formatted_v}{comma}")
            lines.append(f"{spaces}}}")
            return "\n".join(lines)
        elif isinstance(val, list):
            if not val:
                return "[]"
            lines = ["["]
            for i, item in enumerate(val):
                new_path = f"{path}[{i}]"
                comma = "," if i < len(val) - 1 else ""
                formatted_item = format_value(item, new_path, indent + 1)
                lines.append(f"{spaces}  {formatted_item}{comma}")
            lines.append(f"{spaces}]")
            return "\n".join(lines)
        elif isinstance(val, str):
            color = Colors.GREEN if highlighted else ""
            reset = Colors.RESET if highlighted else ""
            return f'{color}"{val}"{reset}'
        elif isinstance(val, bool):
            color = Colors.YELLOW if highlighted else ""
            reset = Colors.RESET if highlighted else ""
            return f"{color}{str(val).lower()}{reset}"
        elif val is None:
            return "null"
        else:
            color = Colors.MAGENTA if highlighted else ""
            reset = Colors.RESET if highlighted else ""
            return f"{color}{val}{reset}"

    return format_value(obj, current_path)


def make_request(method: str, endpoint: str, data: Optional[Dict] = None,
                 headers: Optional[Dict] = None, params: Optional[Dict] = None,
                 highlight_fields: List[str] = None) -> requests.Response:
    """
    Make HTTP request to FHIR server

    Args:
        highlight_fields: List of JSON paths to highlight in response (e.g., ['name', 'identifier[0].value'])
    """
    url = f"{BASE_URL}/{endpoint.lstrip('/')}"

    default_headers = {'Content-Type': 'application/fhir+json'}
    if headers:
        default_headers.update(headers)

    if VERBOSE:
        print(f"\n{Colors.BLUE}→{Colors.RESET} {method} {url}")
        if params:
            print(f"  {Colors.BOLD}Params:{Colors.RESET} {params}")
        if data:
            print(f"  {Colors.BOLD}Request Data:{Colors.RESET}")
            print("  " + json.dumps(data, indent=2).replace("\n", "\n  "))

    try:
        response = requests.request(
            method=method,
            url=url,
            json=data,
            headers=default_headers,
            params=params,
            timeout=REQUEST_TIMEOUT
        )

        if VERBOSE:
            print(f"{Colors.BLUE}←{Colors.RESET} {Colors.BOLD}Status:{Colors.RESET} {response.status_code}")
            if response.content:
                try:
                    resp_json = response.json()
                    print(f"  {Colors.BOLD}Response:{Colors.RESET}")
                    if highlight_fields:
                        print("  " + highlight_json_field(resp_json, highlight_fields).replace("\n", "\n  "))
                    else:
                        print("  " + json.dumps(resp_json, indent=2).replace("\n", "\n  "))
                except:
                    print(f"  {Colors.BOLD}Response:{Colors.RESET} {response.text}")

        return response
    except requests.exceptions.RequestException as e:
        print(f"{Colors.RED}Request failed: {e}{Colors.RESET}")
        raise


def create_resource(resource_type: str, data: Dict) -> Optional[Dict]:
    """Create a FHIR resource"""
    response = make_request('POST', f'/{resource_type}', data=data)
    if response.status_code == 201:
        return response.json()
    return None


def read_resource(resource_type: str, resource_id: str) -> Optional[Dict]:
    """Read a FHIR resource by ID"""
    response = make_request('GET', f'/{resource_type}/{resource_id}')
    if response.status_code == 200:
        return response.json()
    return None


def update_resource(resource_type: str, resource_id: str, data: Dict, version: Optional[str] = None) -> Optional[Dict]:
    """Update a FHIR resource"""
    headers = {}
    if version:
        headers['If-Match'] = f'W/"{version}"'

    response = make_request('PUT', f'/{resource_type}/{resource_id}', data=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None


def delete_resource(resource_type: str, resource_id: str) -> bool:
    """Delete a FHIR resource"""
    response = make_request('DELETE', f'/{resource_type}/{resource_id}')
    return response.status_code == 200


def search_resources(resource_type: str, params: Dict) -> Optional[Dict]:
    """Search for FHIR resources"""
    response = make_request('GET', f'/{resource_type}', params=params)
    if response.status_code == 200:
        return response.json()
    return None


def extract_entries(bundle: Dict, resource_type: str) -> List[Dict]:
    """Extract resources of specific type from a search bundle"""
    if not bundle or bundle.get('resourceType') != 'Bundle':
        return []

    entries = bundle.get('entry', [])
    return [
        entry['resource']
        for entry in entries
        if entry.get('resource', {}).get('resourceType') == resource_type
    ]


def assert_status_code(response: requests.Response, expected: int, test_name: str, results: TestResults):
    """Assert that response has expected status code"""
    if response.status_code == expected:
        results.add_pass(test_name)
        return True
    else:
        results.add_fail(test_name, f"Expected status {expected}, got {response.status_code}")
        return False


def assert_resource_exists(bundle: Dict, resource_type: str, test_name: str, results: TestResults):
    """Assert that search bundle contains at least one resource of given type"""
    resources = extract_entries(bundle, resource_type)
    if resources:
        print(f"  {Colors.CYAN}→ Found {len(resources)} {resource_type} resource(s){Colors.RESET}")
        results.add_pass(test_name)
        return True
    else:
        print(f"  {Colors.RED}→ No {resource_type} resources found in bundle{Colors.RESET}")
        results.add_fail(test_name, f"No {resource_type} resources found in bundle")
        return False


def assert_no_resources(bundle: Dict, resource_type: str, test_name: str, results: TestResults):
    """Assert that search bundle contains no resources of given type"""
    resources = extract_entries(bundle, resource_type)
    if not resources:
        results.add_pass(test_name)
        return True
    else:
        results.add_fail(test_name, f"Found {len(resources)} {resource_type} resources, expected 0")
        return False


def assert_field_equals(resource: Dict, field_path: str, expected_value: Any, test_name: str, results: TestResults):
    """Assert that a field in resource equals expected value"""
    fields = field_path.split('.')
    value = resource

    try:
        for field in fields:
            if '[' in field:
                # Handle array access like "name[0]"
                field_name, index = field.rstrip(']').split('[')
                value = value[field_name][int(index)]
            else:
                value = value[field]

        if value == expected_value:
            print(f"  {Colors.CYAN}→ {field_path} = {Colors.GREEN}{value}{Colors.RESET}")
            results.add_pass(test_name)
            return True
        else:
            print(f"  {Colors.RED}→ {field_path}: expected {expected_value}, got {value}{Colors.RESET}")
            results.add_fail(test_name, f"Expected {field_path}={expected_value}, got {value}")
            return False
    except (KeyError, IndexError, TypeError) as e:
        print(f"  {Colors.RED}→ Field {field_path} not found: {e}{Colors.RESET}")
        results.add_fail(test_name, f"Field {field_path} not found: {e}")
        return False


def get_field_value(obj: Dict, field_path: str) -> Any:
    """
    Extract value from nested object using dot notation
    Example: get_field_value(obj, 'name[0].given[0]')
    """
    fields = field_path.split('.')
    value = obj

    for field in fields:
        if '[' in field:
            field_name, index = field.rstrip(']').split('[')
            value = value[field_name][int(index)]
        else:
            value = value[field]

    return value
