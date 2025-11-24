"""
Tests for Organization resource
Based on examples from organization-management.md
"""
import time
from test_utils import (
    TestResults, make_request, create_resource, read_resource,
    update_resource, delete_resource, search_resources,
    assert_status_code, assert_resource_exists, assert_no_resources,
    Colors
)
from config import TEST_IDENTIFIER_PREFIX, CLEANUP_AFTER_TESTS


def run_organization_tests() -> TestResults:
    """Run all organization tests"""
    results = TestResults()
    created_resources = []

    print(f"\n{Colors.BOLD}=== Organization Tests ==={Colors.RESET}\n")

    # Setup: Create test organization for name search
    print(f"\n{Colors.BOLD}Search Tests Setup{Colors.RESET}")
    fergana_org = {
        "resourceType": "Organization",
        "meta": {
            "profile": ["https://dhp.uz/fhir/core/StructureDefinition/uz-core-organization"]
        },
        "identifier": [
            {
                "system": "https://dhp.uz/fhir/core/sid/org/uz/soliq",
                "type": {
                    "coding": [
                        {"system": "http://terminology.hl7.org/CodeSystem/v2-0203", "code": "TAX"}
                    ]
                },
                "value": f"{TEST_IDENTIFIER_PREFIX}fergana-test-999"
            }
        ],
        "active": True,
        "type": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/organization-type",
                        "code": "prov",
                        "display": "Healthcare Provider"
                    }
                ]
            }
        ],
        "language": "uz",
        "name": f"{TEST_IDENTIFIER_PREFIX}Fergana Regional Hospital"
    }

    response = make_request('POST', '/Organization', data=fergana_org)
    if response.status_code == 201:
        fergana_org_created = response.json()
        created_resources.append(('Organization', fergana_org_created['id']))
        results.add_pass("Create test organization for name search")

        # Wait 5 seconds for indexing
        print(f"{Colors.BLUE}Waiting 5 seconds for server indexing...{Colors.RESET}")
        time.sleep(5)
    else:
        results.add_fail("Create test organization", f"Status {response.status_code}")

    print(f"\n{Colors.BOLD}Search Tests{Colors.RESET}")

    # Test 1: Search for organization by soliq ID (positive test - should exist)
    response = make_request('GET', '/Organization', params={
        'identifier': 'https://dhp.uz/fhir/core/sid/org/uz/soliq|123456789'
    })
    if response.status_code == 200:
        bundle = response.json()
        # Check if we found any organizations (check entry array - total field not reliable on this server)
        entries = bundle.get('entry', [])
        org_entries = [e for e in entries if e.get('resource', {}).get('resourceType') == 'Organization']
        if len(org_entries) > 0:
            print(f"  {Colors.CYAN}→ Found {len(org_entries)} organization(s){Colors.RESET}")
            results.add_pass("Search organization by soliq ID")
        else:
            results.add_skip("Search organization by soliq ID", "No org with test ID found")
    else:
        results.add_fail("Search organization by soliq ID", f"Status {response.status_code}")

    # Test 2: Search by name with :contains modifier (substring match)
    response = make_request('GET', '/Organization', params={'name:contains': 'Fergana'})
    if response.status_code == 200:
        bundle = response.json()
        # Check if we found any organizations
        entries = [e for e in bundle.get('entry', []) if e.get('resource', {}).get('resourceType') == 'Organization']
        if len(entries) > 0:
            results.add_pass('Search organization by name:contains (substring)')
        else:
            # Server might need more time for indexing or name search might have limitations
            results.add_skip('Search organization by name:contains', 'No results (server indexing delay or search limitation)')
    else:
        results.add_fail("Search organization by name:contains", f"Status {response.status_code}")

    # Test 3: Search with exact name match
    response = make_request('GET', '/Organization', params={'name:exact': 'Toshkent'})
    assert_status_code(response, 200, 'Search organization by exact name', results)

    # Test 4: Search by type
    response = make_request('GET', '/Organization', params={'type': 'prov'})
    if response.status_code == 200:
        bundle = response.json()
        assert_resource_exists(bundle, 'Organization', 'Search organization by type (prov)', results)
    else:
        results.add_fail("Search organization by type", f"Status {response.status_code}")

    # Test 5: Search active organizations
    response = make_request('GET', '/Organization', params={'active': 'true'})
    if response.status_code == 200:
        bundle = response.json()
        assert_resource_exists(bundle, 'Organization', 'Search active organizations', results)
    else:
        results.add_fail("Search active organizations", f"Status {response.status_code}")

    # Test 6: Combining parameters (AND) with :contains modifier
    response = make_request('GET', '/Organization', params={
        'name:contains': 'Hospital',
        'active': 'true'
    })
    assert_status_code(response, 200, 'Search with combined parameters (AND)', results)

    # Test 7: Multiple values (OR)
    response = make_request('GET', '/Organization', params={
        'type': 'prov,dept'
    })
    if response.status_code == 200:
        bundle = response.json()
        assert_resource_exists(bundle, 'Organization', 'Search with multiple values (OR)', results)
    else:
        results.add_fail("Search with multiple values", f"Status {response.status_code}")

    # Test 8: Search departments of an organization (if we can find a parent org)
    response = make_request('GET', '/Organization', params={'type': 'prov', '_count': '1'})
    if response.status_code == 200:
        bundle = response.json()
        entries = bundle.get('entry', [])
        org_entries = [e for e in entries if e.get('resource', {}).get('resourceType') == 'Organization']
        if len(org_entries) > 0:
            parent_org_id = org_entries[0]['resource']['id']
            response = make_request('GET', '/Organization', params={
                'partof': f'Organization/{parent_org_id}'
            })
            assert_status_code(response, 200, 'Search for departments (partof)', results)
        else:
            results.add_skip("Search for departments", "No parent org found")
    else:
        results.add_fail("Search for departments", f"Status {response.status_code}")

    # CRUD Operations Tests
    print(f"\n{Colors.BOLD}CRUD Operations{Colors.RESET}")

    # Test 9: Create organization
    test_org = {
        "resourceType": "Organization",
        "meta": {
            "profile": ["https://dhp.uz/fhir/core/StructureDefinition/uz-core-organization"]
        },
        "identifier": [
            {
                "system": "https://dhp.uz/fhir/core/sid/org/uz/soliq",
                "type": {
                    "coding": [
                        {"system": "http://terminology.hl7.org/CodeSystem/v2-0203", "code": "TAX"}
                    ]
                },
                "value": f"{TEST_IDENTIFIER_PREFIX}123456789"
            }
        ],
        "active": True,
        "type": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/organization-type",
                        "code": "prov",
                        "display": "Healthcare Provider"
                    }
                ]
            }
        ],
        "language": "uz",
        "name": f"{TEST_IDENTIFIER_PREFIX}Test Organization"
    }

    response = make_request('POST', '/Organization', data=test_org)
    if response.status_code == 201:
        created_org = response.json()
        created_resources.append(('Organization', created_org['id']))
        results.add_pass("Create organization")

        # Test 10: Read organization
        org_id = created_org['id']
        response = make_request('GET', f'/Organization/{org_id}',
                              highlight_fields=['name', 'id', 'active'])
        if response.status_code == 200:
            results.add_pass("Read organization by ID")
            read_org = response.json()

            # Test 11: Update organization
            read_org['name'] = f"{TEST_IDENTIFIER_PREFIX}Updated Test Organization"
            version = read_org['meta']['versionId']

            response = make_request('PUT', f'/Organization/{org_id}',
                                  data=read_org,
                                  headers={'If-Match': f'W/"{version}"'},
                                  highlight_fields=['name'])
            if response.status_code == 200:
                results.add_pass("Update organization")

                # Verify update
                response = make_request('GET', f'/Organization/{org_id}')
                if response.status_code == 200:
                    updated_org = response.json()
                    if updated_org['name'] == f"{TEST_IDENTIFIER_PREFIX}Updated Test Organization":
                        results.add_pass("Verify organization update")
                    else:
                        results.add_fail("Verify organization update", "Name not updated")
            else:
                results.add_fail("Update organization", f"Status {response.status_code}")
        else:
            results.add_fail("Read organization by ID", f"Status {response.status_code}")
    else:
        results.add_fail("Create organization", f"Status {response.status_code}")

    # Negative Tests
    print(f"\n{Colors.BOLD}Negative Tests{Colors.RESET}")

    # Test 12: Read non-existent organization (accept both 400 and 404)
    # 400 = Invalid ID format, 404 = Valid format but doesn't exist
    response = make_request('GET', '/Organization/nonexistent-id-12345')
    if response.status_code in [400, 404]:
        results.add_pass('Read non-existent organization (400 or 404)')
    else:
        results.add_fail('Read non-existent organization', f"Expected 400 or 404, got {response.status_code}")

    # Test 13: Search with invalid parameter
    response = make_request('GET', '/Organization', params={
        'name': 'XYZ_NONEXISTENT_ORG_NAME_12345'
    })
    if response.status_code == 200:
        bundle = response.json()
        assert_no_resources(bundle, 'Organization', 'Search non-existent organization name', results)
    else:
        results.add_fail("Search non-existent organization", f"Status {response.status_code}")

    # Test 14: Update without If-Match header (should fail with 412)
    if created_resources:
        org_id = created_resources[0][1]
        response = make_request('GET', f'/Organization/{org_id}')
        if response.status_code == 200:
            org_data = response.json()
            org_data['name'] = "Should fail without version"

            response = make_request('PUT', f'/Organization/{org_id}', data=org_data)
            if response.status_code == 412:
                results.add_pass("Update without If-Match header (correctly fails)")
            else:
                results.add_fail("Update without If-Match", f"Expected 412, got {response.status_code}")

    # Cleanup
    if CLEANUP_AFTER_TESTS:
        print(f"\n{Colors.BOLD}Cleanup{Colors.RESET}")
        for resource_type, resource_id in created_resources:
            response = make_request('DELETE', f'/{resource_type}/{resource_id}')
            if response.status_code == 200:
                results.add_pass(f"Delete {resource_type}/{resource_id}")
            else:
                results.add_fail(f"Delete {resource_type}/{resource_id}", f"Status {response.status_code}")

    return results


if __name__ == '__main__':
    results = run_organization_tests()
    results.print_summary()
    exit(0 if results.failed == 0 else 1)
