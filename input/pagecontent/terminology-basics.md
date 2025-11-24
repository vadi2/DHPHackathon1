# Terminology basics

## Overview

Goal: Learn to search and retrieve terminology resources (CodeSystem, ValueSet, ConceptMap), understand version management, and use FHIR terminology operations to support coded data in your applications.

- Resources: CodeSystem, ValueSet, ConceptMap
- Skills: Search parameters, filtering, terminology operations ($expand, $validate-code, $lookup), version management
- Base URL: `https://playground.dhp.uz/fhir`
  - **Note:** This is a temporary URL that will be replaced with the final one closer to the connectathon
- Useful links:
  - [FHIR Terminology Service](http://hl7.org/fhir/R5/terminology-service.html)
  - [uz-core Artifacts](https://dhp.uz/fhir/core/en/artifacts.html)
  - [FHIR CodeSystem Resource](http://hl7.org/fhir/R5/codesystem.html)
  - [FHIR ValueSet Resource](http://hl7.org/fhir/R5/valueset.html)
  - [FHIR ConceptMap Resource](http://hl7.org/fhir/R5/conceptmap.html)

**Feedback:** Share your experience, issues and successes in the [connectathon document](https://docs.google.com/document/d/1PdQ8zBI9xkISP3tAqIK8-TGMql3kVVZ4UNoHVYqCy4Y/edit?usp=sharing).

## Understanding FHIR terminology

FHIR provides three main resources for working with terminology. Understanding when and how to use each one is essential for building interoperable healthcare applications.

### CodeSystem

A **CodeSystem** defines a collection of codes with their meanings. Think of it as a dictionary of medical codes.

**Example:** The [`position-and-profession-cs`](https://dhp.uz/fhir/core/en/CodeSystem-position-and-profession-cs.html) CodeSystem contains codes for healthcare professions:
- Code `2211.1` means "General practitioner"
- Code `2212` means "Medical specialist"
- Code `3221` means "Nurse"

Key elements:
- **url**: Canonical identifier that never changes (e.g., `https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs`)
- **version**: Business version number (e.g., `1.0.0`)
- **concept**: Array of codes with their properties
- **property**: Additional information about codes (e.g., status, parent code)
- **content**: Indicates if all codes are present (`complete`) or not (`not-present`)

### ValueSet

A **ValueSet** is a selection of codes from one or more CodeSystems for a specific purpose. While a CodeSystem defines all possible codes, a ValueSet defines which codes are allowed in a particular context.

**Example:** The [`position-and-profession-vs`](https://dhp.uz/fhir/core/en/ValueSet-position-and-profession-vs.html) ValueSet might only include codes for licensed medical practitioners, excluding administrative staff.

Key elements:
- **url**: Canonical identifier
- **version**: Business version
- **compose**: Defines how the ValueSet is constructed
  - **include**: Which codes to include from which CodeSystems
  - **exclude**: Which codes to exclude
  - **filter**: Rules for selecting codes
- **expansion**: The actual list of codes (may be generated on-demand)

**Common use cases:**
- Populating dropdown lists in forms
- Validating user input
- Defining allowed values for coded fields in profiles

### ConceptMap

A **ConceptMap** defines mappings between codes in different CodeSystems. This is essential when you need to translate data between different coding systems.

**Example:** The [`iso-3166-alpha3-to-alpha2-cs`](https://dhp.uz/fhir/core/en/ConceptMap-iso-3166-alpha3-to-alpha2-cs.html) ConceptMap translates between ISO 3-letter and 2-letter country codes:
- `UZB` (3-letter code) → `UZ` (2-letter code)
- `ABW` (Aruba 3-letter) → `AW` (Aruba 2-letter)

Key elements:
- **sourceCanonical**: URL of the source CodeSystem or ValueSet
- **targetCanonical**: URL of the target CodeSystem or ValueSet
- **group**: Contains the actual mappings
  - **element**: Individual code mappings
  - **equivalence**: Type of mapping (equivalent, wider, narrower, etc.)

**Common use cases:**
- Converting data when exchanging with international systems
- Supporting multiple coding standards simultaneously
- Migrating from old to new code systems

### Version management

Every terminology resource can have multiple versions. Understanding versions is crucial for:
- **Consistency**: Ensuring the same code means the same thing over time
- **Compliance**: Some regulations require specific versions
- **Compatibility**: Different systems may use different versions

Two types of versions:
1. **Business version** (`version` element): Semantic version like `1.0.0`, `2.1.0`
2. **Technical version** (`meta.versionId`): Server-assigned version for each resource update

**Best practice:** Always specify the version in production systems to ensure consistent meaning of codes.

## Read operations

### Read CodeSystem

- HTTP method: GET
- Endpoint: `/CodeSystem?url=[canonical-url]`

Retrieving a specific CodeSystem by its canonical URL. This is the recommended approach as canonical URLs are globally unique identifiers that remain stable across different servers.

Example:
```
GET /CodeSystem?url=https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs
```

Response: HTTP 200 OK with a Bundle containing the CodeSystem resource in `entry[0].resource`.

**Understanding the response:**

The response is a Bundle with the CodeSystem resource in `entry[0].resource`:

```json
{
  "resourceType": "Bundle",
  "type": "searchset",
  "entry": [
    {
      "resource": {
        "resourceType": "CodeSystem",
        "id": "position-and-profession-cs",
        "url": "https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs",
        "version": "1.0.0",
        "name": "PositionAndProfessionCS",
        "title": "Position and Profession Codes",
        "status": "active",
        "content": "complete",
        "concept": [
          {
            "code": "2211.1",
            "display": "General practitioner",
            "definition": "Medical doctor providing primary care services"
          },
          {
            "code": "2212",
            "display": "Medical specialist",
            "definition": "Medical doctor specialized in specific field"
          }
        ]
      }
    }
  ]
}
```

### Read ValueSet

- HTTP method: GET
- Endpoint: `/ValueSet?url=[canonical-url]`

Retrieving a specific ValueSet by its canonical URL. This is the recommended approach as canonical URLs are globally unique identifiers that remain stable across different servers.

Example:
```
GET /ValueSet?url=https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs
```

Response: HTTP 200 OK with a Bundle containing the ValueSet resource in `entry[0].resource`.

**Understanding the response:**

The response is a Bundle with the ValueSet resource in `entry[0].resource`:

```json
{
  "resourceType": "Bundle",
  "type": "searchset",
  "entry": [
    {
      "resource": {
        "resourceType": "ValueSet",
        "id": "position-and-profession-vs",
        "url": "https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs",
        "version": "1.0.0",
        "name": "PositionAndProfessionVS",
        "title": "Position and Profession Values",
        "status": "active",
        "compose": {
          "include": [
            {
              "system": "https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs"
            }
          ]
        }
      }
    }
  ]
}
```

**Note:** The response shows how the ValueSet is defined (compose) but may not contain the actual list of codes. To get the codes, use the `$expand` operation (see below).

### Read ConceptMap

- HTTP method: GET
- Endpoint: `/ConceptMap?url=[canonical-url]`

Retrieving a specific ConceptMap by its canonical URL. This is the recommended approach as canonical URLs are globally unique identifiers that remain stable across different servers.

Example:
```
GET /ConceptMap?url=https://terminology.dhp.uz/fhir/core/ConceptMap/iso-3166-alpha3-to-alpha2-cs
```

Response: HTTP 200 OK with a Bundle containing the ConceptMap resource showing the mappings between code systems in `entry[0].resource`.

## Search operations

- HTTP method: GET
- Endpoint: `/CodeSystem?[parameters]`, `/ValueSet?[parameters]`, `/ConceptMap?[parameters]`

### CodeSystem search parameters

| Parameter | Type | Description | Example |
|----------|-----|----------|--------|
| `url` | uri | Search by canonical URL | `?url=https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs` |
| `name` | string | Search by name | `?name=position` |
| `title` | string | Search by title | `?title=profession` |
| `status` | token | Filter by status | `?status=active` |
| `version` | token | Search by version | `?version=0.3.0` |
| `publisher` | string | Search by publisher | `?publisher=Digital Health Platform` |
| `content` | token | Content type | `?content=complete` |
| `system` | uri | Search for specific system | `?system=http://snomed.info/sct` |

### ValueSet search parameters

| Parameter | Type | Description | Example |
|----------|-----|----------|--------|
| `url` | uri | Search by canonical URL | `?url=https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs` |
| `name` | string | Search by name | `?name=position` |
| `title` | string | Search by title | `?title=profession` |
| `status` | token | Filter by status | `?status=active` |
| `version` | token | Search by version | `?version=0.3.0` |
| `publisher` | string | Search by publisher | `?publisher=Digital Health Platform` |
| `context` | token | Search by use context | `?context=practitioner` |
| `expansion` | uri | Search by expansion identifier | `?expansion=urn:uuid:...` |

### ConceptMap search parameters

| Parameter | Type | Description | Example |
|----------|-----|----------|--------|
| `url` | uri | Search by canonical URL | `?url=https://terminology.dhp.uz/fhir/core/ConceptMap/iso-3166-alpha3-to-alpha2-cs` |
| `name` | string | Search by name | `?name=iso` |
| `status` | token | Filter by status | `?status=active` |
| `title` | string | Search by title | `?title=alpha` |
| `publisher` | string | Search by publisher | `?publisher=Uzinfocom` |
| `source-scope-uri` | uri | Source system or ValueSet | `?source-scope-uri=urn:iso:std:iso:3166` |
| `target-scope-uri` | uri | Target system or ValueSet | `?target-scope-uri=urn:iso:std:iso:3166` |

### Common search patterns

**Find all CodeSystems in the system:**
```
GET /CodeSystem?_summary=true&_count=20
```

**Find CodeSystems by publisher:**
```
GET /CodeSystem?publisher=Health Level Seven
```

**Find active ValueSets:**
```
GET /ValueSet?status=active
```

**Find ConceptMaps for ISO 3166 country codes:**
```
GET /ConceptMap?source-scope-uri=urn:iso:std:iso:3166
```

### Pagination

Search results are returned in a Bundle with pagination (20 records per page). Use `Bundle.link` with `relation="next"` to get the next page.

## Terminology operations

FHIR defines several operations specifically for working with terminology. These operations are essential for building applications that use coded data.

### $expand operation

The `$expand` operation expands a ValueSet to return the actual list of codes. This is the most commonly used terminology operation.

**When to use:**
- Building dropdown lists or selection controls
- Getting all allowed codes for a field
- Checking what codes are available

**Endpoint:** `/ValueSet/$expand` or `/ValueSet/[id]/$expand`

**Parameters:**
- `url`: Canonical URL of the ValueSet (required if not using ID)
- `valueSetVersion`: Specific version to expand
- `count`: Maximum number of codes to return
- `offset`: Offset for pagination
- `filter`: Text filter to match code display names

**Example 1: Basic expansion**
```
GET /ValueSet/$expand?url=https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs
```

Response:
```json
{
  "resourceType": "ValueSet",
  "expansion": {
    "timestamp": "2024-11-24T10:00:00Z",
    "total": 150,
    "offset": 0,
    "contains": [
      {
        "system": "https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs",
        "code": "2211.1",
        "display": "General practitioner"
      },
      {
        "system": "https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs",
        "code": "2212",
        "display": "Medical specialist"
      }
    ]
  }
}
```

**Example 2: Expansion with count limit**
```
GET /ValueSet/$expand?url=https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs&count=10
```

This returns only the first 10 codes.

**Example 3: Expansion by ID**
```
GET /ValueSet/position-and-profession-vs/$expand
```

### $validate-code operation

The `$validate-code` operation checks if a code is valid in a ValueSet. This is essential for data validation.

**When to use:**
- Validating user input before saving
- Checking if received data uses valid codes
- Ensuring data quality

**Endpoint:** `/ValueSet/$validate-code` or `/ValueSet/[id]/$validate-code`

**Parameters:**
- `url`: Canonical URL of the ValueSet (required if not using ID)
- `code`: The code to validate (required)
- `system`: The system the code comes from (required)
- `display`: The display string (optional, can be validated too)
- `valueSetVersion`: Specific version to validate against

**Example 1: Valid code**
```
GET /ValueSet/$validate-code?url=https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs&code=2211.1&system=https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs
```

Response:
```json
{
  "resourceType": "Parameters",
  "parameter": [
    {
      "name": "result",
      "valueBoolean": true
    },
    {
      "name": "display",
      "valueString": "Umumiy amaliyot vrachi"
    },
    {
      "name": "code",
      "valueCode": "2211.1"
    },
    {
      "name": "system",
      "valueUri": "https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs"
    }
  ]
}
```

**Example 2: Invalid code**
```
GET /ValueSet/$validate-code?url=https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs&code=INVALID&system=https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs
```

Response:
```json
{
  "resourceType": "Parameters",
  "parameter": [
    {
      "name": "result",
      "valueBoolean": false
    },
    {
      "name": "message",
      "valueString": "Code 'INVALID' not found in ValueSet"
    }
  ]
}
```

### $lookup operation

The `$lookup` operation retrieves details about a specific code in a CodeSystem.

**When to use:**
- Getting the display name for a code
- Retrieving code definition and properties
- Showing detailed information about selected codes

**Endpoint:** `/CodeSystem/$lookup`

**Parameters:**
- `system`: The CodeSystem URL (required)
- `code`: The code to look up (required)
- `version`: Specific version of the CodeSystem

**Example:**
```
GET /CodeSystem/$lookup?system=https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs&code=2211.1
```

Response:
```json
{
  "resourceType": "Parameters",
  "parameter": [
    {
      "name": "name",
      "valueString": "PositionAndProfessionCS"
    },
    {
      "name": "display",
      "valueString": "General practitioner"
    },
    {
      "name": "designation",
      "part": [
        {
          "name": "language",
          "valueCode": "uz"
        },
        {
          "name": "value",
          "valueString": "Umumiy amaliyot shifokori"
        }
      ]
    },
    {
      "name": "designation",
      "part": [
        {
          "name": "language",
          "valueCode": "ru"
        },
        {
          "name": "value",
          "valueString": "Врач общей практики"
        }
      ]
    }
  ]
}
```

## Version management in practice

### Understanding version elements

Every terminology resource has two version identifiers:

1. **Business version** (`version` element):
   - Semantic version (e.g., `1.0.0`, `2.1.0`)
   - Set by the terminology author
   - Indicates the content version
   - Should be specified when using terminology in production

2. **Technical version** (`meta.versionId`):
   - Server-assigned version (e.g., `1`, `2`, `3`)
   - Changes with each update to the resource
   - Used for optimistic locking (If-Match header)
   - Not typically used for version selection

### Searching by version

**Get a specific version:**
```
GET /CodeSystem?url=https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs&version=0.3.0
```

### Using versions in operations

**Expand a specific version of a ValueSet:**
```
GET /ValueSet/$expand?url=https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs&valueSetVersion=0.3.0
```

**Validate against a specific version:**
```
GET /ValueSet/$validate-code?url=https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs&valueSetVersion=0.3.0&code=2211.1&system=https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs
```

**Look up in a specific version:**
```
GET /CodeSystem/$lookup?system=https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs&version=0.3.0&code=2211.1
```

## Working with ConceptMaps

ConceptMaps enable translation between different coding systems. This is essential when integrating with systems that use different terminologies.

### When do you need ConceptMaps?

- Exchanging data with international systems (e.g., mapping UZ codes to SNOMED or LOINC)
- Supporting multiple coding standards simultaneously
- Migrating from old code systems to new ones
- Creating reports that aggregate data from different coding systems

### Finding relevant ConceptMaps

**Find all available ConceptMaps:**
```
GET /ConceptMap?status=active
```

**Find ConceptMaps for a specific source system:**
```
GET /ConceptMap?source-uri=https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs
```

**Find ConceptMaps for ISO 3166 country codes:**
```
GET /ConceptMap?source-scope-uri=urn:iso:std:iso:3166
```

### Using $translate operation

The `$translate` operation translates a code from one system to another using a ConceptMap.

**Endpoint:** `/ConceptMap/$translate` or `/ConceptMap/[id]/$translate`

**Parameters:**
- `url`: Canonical URL of the ConceptMap
- `source`: Source ValueSet (optional)
- `system`: Source CodeSystem URL (required)
- `code`: Code to translate (required)
- `target`: Target ValueSet or CodeSystem
- `reverse`: Reverse the translation (use target as source)

**Example: Translate ISO 3166 country code**

Using GET:
```
GET /ConceptMap/$translate?url=https://terminology.dhp.uz/fhir/core/ConceptMap/iso-3166-alpha3-to-alpha2-cs&system=urn:iso:std:iso:3166&code=UZB&target=urn:iso:std:iso:3166
```

Using POST (recommended for complex requests):
```
POST /ConceptMap/$translate
Content-Type: application/fhir+json

{
  "resourceType": "Parameters",
  "parameter": [
    {
      "name": "url",
      "valueUri": "https://terminology.dhp.uz/fhir/core/ConceptMap/iso-3166-alpha3-to-alpha2-cs"
    },
    {
      "name": "system",
      "valueUri": "urn:iso:std:iso:3166"
    },
    {
      "name": "code",
      "valueCode": "UZB"
    },
    {
      "name": "target",
      "valueUri": "urn:iso:std:iso:3166"
    }
  ]
}
```

Response:
```json
{
  "resourceType": "Parameters",
  "parameter": [
    {
      "name": "result",
      "valueBoolean": true
    },
    {
      "name": "match",
      "part": [
        {
          "name": "equivalence",
          "valueCode": "equivalent"
        },
        {
          "name": "concept",
          "valueCoding": {
            "system": "urn:iso:std:iso:3166",
            "code": "UZ",
            "display": "Uzbekistan"
          }
        }
      ]
    }
  ]
}
```

## Practical integration workflow

Let's walk through a complete scenario: building a practitioner registration form that uses terminology properly.

### Scenario: Practitioner registration form

**Requirements:**
- User needs to select their license/credential from a dropdown
- Only valid credentials should be selectable
- The display should show the credential name in the user's language

**Resources used in this scenario:**
- [License, Certificate, Degree ValueSet](https://dhp.uz/fhir/core/en/ValueSet-license-certificate-vs.html)

**Step 1: Find the relevant ValueSet**

First, identify which ValueSet defines allowed credentials by browsing the [uz-core terminology artifacts page](https://dhp.uz/fhir/core/en/artifacts.html#4).

From the artifacts page, we find the ValueSet URL: `https://terminology.dhp.uz/fhir/core/ValueSet/license-certificate-vs`

**Step 2: Expand the ValueSet to populate the dropdown**

```
GET /ValueSet/$expand?url=https://terminology.dhp.uz/fhir/core/ValueSet/license-certificate-vs&count=100
```

Response gives us all codes to populate the dropdown:
```json
{
  "expansion": {
    "contains": [
      {
        "system": "http://terminology.hl7.org/CodeSystem/v2-0360",
        "code": "MD",
        "display": "Doctor of Medicine"
      },
      {
        "system": "http://terminology.hl7.org/CodeSystem/v2-0360",
        "code": "RN",
        "display": "Registered Nurse"
      }
    ]
  }
}
```

**Step 3: User selects a credential**

User selects "Doctor of Medicine" (code: `MD`)

**Step 4: Look up display names for other languages (optional)**

If you need to show the credential in multiple languages:

```
GET /CodeSystem/$lookup?system=http://terminology.hl7.org/CodeSystem/v2-0360&code=MD
```

This returns all available designations (translations).

**Step 5: Save in the Practitioner resource**

```json
{
  "resourceType": "Practitioner",
  "...": "...",
  "qualification": [
    {
      "code": {
        "coding": [
          {
            "system": "http://terminology.hl7.org/CodeSystem/v2-0360",
            "code": "MD",
            "display": "Doctor of Medicine"
          }
        ]
      }
    }
  ]
}
```

### Implementation tips

1. **Cache expansion results**: Expanding ValueSets can be slow. Cache the results and refresh periodically or on version changes.

2. **Handle pagination**: If a ValueSet is large, the expansion may be paginated. Implement proper pagination handling.

3. **Use version binding**: In production, pin to specific ValueSet versions to ensure consistency.

4. **Handle missing codes gracefully**: If a code isn't found during lookup, handle it gracefully rather than failing.

## Error handling

### Common errors and how to handle them

**Error 1: Code not found in ValueSet**

Request:
```
GET /ValueSet/$validate-code?url=https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs&code=INVALID&system=https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs
```

Response:
```json
{
  "resourceType": "Parameters",
  "parameter": [
    {
      "name": "result",
      "valueBoolean": false
    },
    {
      "name": "message",
      "valueString": "The code 'INVALID' is not in the ValueSet"
    }
  ]
}
```

**Handling:** Display a user-friendly error message and ask the user to select a valid code from the list.

**Error 2: ValueSet not found**

Request:
```
GET /ValueSet/$expand?url=https://terminology.dhp.uz/fhir/core/ValueSet/nonexistent-vs
```

Response:
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "diagnostics": "ValueSet with URL 'https://terminology.dhp.uz/fhir/core/ValueSet/nonexistent-vs' not found"
    }
  ]
}
```

**Handling:** Check the ValueSet URL for typos. Verify that the ValueSet exists on the server. Use search to find available ValueSets.

**Error 3: Version not found**

Request:
```
GET /CodeSystem?url=https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs&version=99.99.99
```

Response:
```json
{
  "resourceType": "Bundle",
  "type": "searchset",
  "total": 0,
  "entry": []
}
```

**Handling:** Verify the version number. Search without version to find available versions. Consider falling back to the latest version if specific version not found.

**Error 4: Expansion too large**

Request:
```
GET /ValueSet/$expand?url=http://hl7.org/fhir/ValueSet/all-languages
```

Response:
```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "too-costly",
      "diagnostics": "The ValueSet expansion would be too large (>1000 codes). Use count and offset parameters to paginate."
    }
  ]
}
```

**Handling:** Use the `count` and `offset` parameters to paginate through large expansions. Consider using filters to narrow down the results.

**Error 5: Invalid system**

Request:
```
GET /ValueSet/$validate-code?url=https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs&code=2211.1&system=http://wrong-system.com
```

Response:
```json
{
  "resourceType": "Parameters",
  "parameter": [
    {
      "name": "result",
      "valueBoolean": false
    },
    {
      "name": "message",
      "valueString": "The code system 'http://wrong-system.com' is not in the ValueSet"
    }
  ]
}
```

**Handling:** Ensure you're using the correct CodeSystem URL. The system must match one of the systems included in the ValueSet.

### Response codes

| Code | Description |
|-----|----------|
| 200 | OK - successful operation |
| 400 | Bad Request - invalid parameters |
| 404 | Not Found - resource not found |
| 410 | Gone - resource was deleted |
| 422 | Unprocessable Entity - operation cannot be processed |
| 500 | Internal Server Error - server error |

## Progressive learning exercises

Work through these exercises in order, from basic to advanced.

### Beginner exercises

**Exercise 1: Read a CodeSystem**

Task: Retrieve the position-and-profession CodeSystem and examine its structure.

```
GET /CodeSystem/position-and-profession-cs
```

Questions to explore:
- How many concepts are defined?
- What is the version number?
- Is the content complete or partial?

**Exercise 2: Search for ValueSets**

Task: Find all ValueSets available in the system.

```
GET /ValueSet?_summary=true&_count=20
```

Questions to explore:
- How many ValueSets are there in total?
- Which ones are related to practitioners?
- Which ones are Uzbekistan-specific vs international?

**Exercise 3: Expand a simple ValueSet**

Task: Expand the gender-other ValueSet to see all possible values.

```
GET /ValueSet/$expand?url=https://terminology.dhp.uz/fhir/core/ValueSet/gender-other-vs
```

Questions to explore:
- How many codes are in this ValueSet?
- What do the different codes mean?

**Exercise 4: Validate a code**

Task: Check if code "2211.1" is valid in the position-and-profession ValueSet.

```
GET /ValueSet/$validate-code?url=https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs&code=2211.1&system=https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs
```

Questions to explore:
- Is the code valid?
- What display name is returned?
- Try with an invalid code like "INVALID" - what happens?

### Intermediate exercises

**Exercise 5: Search ValueSets by context**

Task: Find all ValueSets that are used in the context of practitioners.

```
GET /ValueSet?context=practitioner
```

Questions to explore:
- Which ValueSets are practitioner-specific?
- Can you find the ValueSet for practitioner specialties?

**Exercise 6: Use $lookup to get code details**

Task: Look up detailed information about code "2211.1".

```
GET /CodeSystem/$lookup?system=https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs&code=2211.1
```

Questions to explore:
- What designations (translations) are available?
- Is there a definition for the code?
- Are there any properties defined?

**Exercise 7: Work with versions**

Task: Find all versions of the position-and-profession CodeSystem.

```
GET /CodeSystem?url=https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs&_sort=-version
```

Questions to explore:
- How many versions exist?
- What is the latest version?
- Try expanding the ValueSet with a specific version - does it work?

**Exercise 8: Use filters in expansion**

Task: Expand the position-and-profession ValueSet but filter to only show codes containing "nurse".

```
GET /ValueSet/$expand?url=https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs&filter=nurse
```

Questions to explore:
- How many codes match the filter?
- Try different filter terms - what results do you get?
- Try combining filter with `count` parameter

### Advanced exercises

**Exercise 9: Find and use a ConceptMap**

Task: Find a ConceptMap that maps between Uzbekistan codes and an international terminology.

```
GET /ConceptMap?source-uri:contains=terminology.dhp.uz
```

Then translate a code:
```
GET /ConceptMap/$translate?url=[url-from-search]&system=[source-system]&code=[code]
```

Questions to explore:
- What ConceptMaps are available?
- Can you successfully translate a code?
- What equivalence types are used in the mappings?

**Exercise 10: Build a terminology-aware form**

Task: Design and implement a complete flow for a coded field:

1. Search for the appropriate ValueSet
2. Expand it to get codes for a dropdown
3. Validate the user's selection
4. Look up display names in multiple languages
5. Save the coded data in a FHIR resource

Questions to explore:
- How do you handle large ValueSets (>100 codes)?
- How do you cache expansion results efficiently?
- How do you handle errors at each step?

**Exercise 11: Implement version pinning**

Task: Modify your Exercise 10 implementation to:
- Pin to a specific version of the ValueSet
- Check if a newer version is available
- Provide a migration path when updating versions

Questions to explore:
- How do you detect version changes?
- How do you test against multiple versions?
- What happens to data coded with old versions?

**Exercise 12: Handle errors gracefully**

Task: Implement comprehensive error handling for all terminology operations:

1. Try to expand a non-existent ValueSet
2. Try to validate a code with wrong system
3. Try to look up a non-existent code
4. Try to expand with an invalid version

Questions to explore:
- What error codes are returned?
- How can you provide user-friendly error messages?
- How do you log errors for debugging?

## Useful links

**FHIR Documentation:**
- [FHIR Terminology Service](http://hl7.org/fhir/R5/terminology-service.html)
- [FHIR CodeSystem Resource](http://hl7.org/fhir/R5/codesystem.html)
- [FHIR ValueSet Resource](http://hl7.org/fhir/R5/valueset.html)
- [FHIR ConceptMap Resource](http://hl7.org/fhir/R5/conceptmap.html)

**Uzbekistan-Specific Terminology:**
- [Position and Profession CodeSystem](https://dhp.uz/fhir/core/en/CodeSystem-position-and-profession-cs.html) - Healthcare positions and professions
- [Position and Profession ValueSet](https://dhp.uz/fhir/core/en/ValueSet-position-and-profession-vs.html) - Allowed healthcare professions
- [uz-core Artifacts](https://dhp.uz/fhir/core/en/artifacts.html) - All uz-core terminology resources
- [DHPCapabilityStatement](https://dhp.uz/fhir/core/en/CapabilityStatement-DHPCapabilityStatement.html)

---

## Code examples

{% include code-tabs-style.html %}

Below are examples of expanding a ValueSet and validating a code in various programming languages:

<div class="code-tabs">
  <ul class="nav nav-tabs" role="tablist">
    <li class="active">
      <a href="#curl" data-toggle="tab">cURL</a>
    </li>
    <li>
      <a href="#python" data-toggle="tab">Python</a>
    </li>
    <li>
      <a href="#javascript" data-toggle="tab">JavaScript</a>
    </li>
    <li>
      <a href="#java" data-toggle="tab">Java</a>
    </li>
    <li>
      <a href="#csharp" data-toggle="tab">C#</a>
    </li>
    <li>
      <a href="#go" data-toggle="tab">Go</a>
    </li>
  </ul>
  <div class="tab-content">
    <div class="tab-pane active" id="curl">
<pre><code class="language-bash"># Expand a ValueSet
curl -X GET "https://playground.dhp.uz/fhir/ValueSet/\$expand?url=https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs" \
  -H "Accept: application/fhir+json"

# Validate a code
curl -X GET "https://playground.dhp.uz/fhir/ValueSet/\$validate-code?url=https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs&code=2211.1&system=https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs" \
  -H "Accept: application/fhir+json"

# Lookup a code
curl -X GET "https://playground.dhp.uz/fhir/CodeSystem/\$lookup?system=https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs&code=2211.1" \
  -H "Accept: application/fhir+json"
</code></pre>
    </div>
    <div class="tab-pane" id="python">
<pre><code class="language-python">import requests
from typing import List, Dict

# FHIR server base URL
base_url = "https://playground.dhp.uz/fhir"

def expand_valueset(valueset_url: str) -> List[Dict]:
    """Expand a ValueSet to get all codes."""
    response = requests.get(
        f"{base_url}/ValueSet/$expand",
        params={
            "url": valueset_url
        },
        headers={"Accept": "application/fhir+json"}
    )

    if response.status_code == 200:
        expansion = response.json()
        if "expansion" in expansion and "contains" in expansion["expansion"]:
            return expansion["expansion"]["contains"]

    return []

def validate_code(valueset_url: str, code: str, system: str) -> bool:
    """Validate if a code is in a ValueSet."""
    response = requests.get(
        f"{base_url}/ValueSet/$validate-code",
        params={
            "url": valueset_url,
            "code": code,
            "system": system
        },
        headers={"Accept": "application/fhir+json"}
    )

    if response.status_code == 200:
        result = response.json()
        for param in result.get("parameter", []):
            if param.get("name") == "result":
                return param.get("valueBoolean", False)

    return False

def lookup_code(system: str, code: str) -> Dict:
    """Look up details about a code."""
    response = requests.get(
        f"{base_url}/CodeSystem/$lookup",
        params={
            "system": system,
            "code": code
        },
        headers={"Accept": "application/fhir+json"}
    )

    if response.status_code == 200:
        return response.json()

    return {}

# Example usage
valueset_url = "https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs"
codesystem_url = "https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs"

# Expand ValueSet
print("Expanding ValueSet...")
codes = expand_valueset(valueset_url)
for code in codes[:5]:  # Show first 5
    print(f"  {code['code']}: {code['display']}")

# Validate a code
print("\nValidating code '2211.1'...")
is_valid = validate_code(valueset_url, "2211.1", codesystem_url)
print(f"  Valid: {is_valid}")

# Lookup code details
print("\nLooking up code '2211.1'...")
details = lookup_code(codesystem_url, "2211.1")
print(f"  Details: {details}")
</code></pre>
    </div>
    <div class="tab-pane" id="javascript">
<pre><code class="language-javascript">// Using fetch API
const baseUrl = "https://playground.dhp.uz/fhir";

async function expandValueSet(valueSetUrl) {
  const params = new URLSearchParams({
    url: valueSetUrl
  });

  const response = await fetch(`${baseUrl}/ValueSet/$expand?${params}`, {
    headers: { 'Accept': 'application/fhir+json' }
  });

  if (response.ok) {
    const data = await response.json();
    return data.expansion?.contains || [];
  }

  return [];
}

async function validateCode(valueSetUrl, code, system) {
  const params = new URLSearchParams({
    url: valueSetUrl,
    code: code,
    system: system
  });

  const response = await fetch(`${baseUrl}/ValueSet/$validate-code?${params}`, {
    headers: { 'Accept': 'application/fhir+json' }
  });

  if (response.ok) {
    const data = await response.json();
    const resultParam = data.parameter?.find(p => p.name === "result");
    return resultParam?.valueBoolean || false;
  }

  return false;
}

async function lookupCode(system, code) {
  const params = new URLSearchParams({
    system: system,
    code: code
  });

  const response = await fetch(`${baseUrl}/CodeSystem/$lookup?${params}`, {
    headers: { 'Accept': 'application/fhir+json' }
  });

  if (response.ok) {
    return await response.json();
  }

  return null;
}

// Example usage
const valueSetUrl = "https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs";
const codeSystemUrl = "https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs";

(async () => {
  // Expand ValueSet
  console.log("Expanding ValueSet...");
  const codes = await expandValueSet(valueSetUrl);
  codes.slice(0, 5).forEach(code => {
    console.log(`  ${code.code}: ${code.display}`);
  });

  // Validate a code
  console.log("\nValidating code '2211.1'...");
  const isValid = await validateCode(valueSetUrl, "2211.1", codeSystemUrl);
  console.log(`  Valid: ${isValid}`);

  // Lookup code details
  console.log("\nLooking up code '2211.1'...");
  const details = await lookupCode(codeSystemUrl, "2211.1");
  console.log("  Details:", details);
})();
</code></pre>
    </div>
    <div class="tab-pane" id="java">
<pre><code class="language-java">import ca.uhn.fhir.context.FhirContext;
import ca.uhn.fhir.rest.client.api.IGenericClient;
import org.hl7.fhir.r5.model.*;
import java.util.List;

public class TerminologyExample {
    private static final String BASE_URL = "https://playground.dhp.uz/fhir";
    private static final FhirContext ctx = FhirContext.forR5();
    private static final IGenericClient client = ctx.newRestfulGenericClient(BASE_URL);

    public static List&lt;ValueSet.ValueSetExpansionContainsComponent&gt; expandValueSet(String valueSetUrl) {
        // Create parameters for $expand operation
        Parameters params = new Parameters();
        params.addParameter("url", new UriType(valueSetUrl));

        // Execute $expand operation
        ValueSet expanded = client
            .operation()
            .onType(ValueSet.class)
            .named("$expand")
            .withParameters(params)
            .returnResourceType(ValueSet.class)
            .execute();

        return expanded.getExpansion().getContains();
    }

    public static boolean validateCode(String valueSetUrl, String code, String system) {
        // Create parameters for $validate-code operation
        Parameters params = new Parameters();
        params.addParameter("url", new UriType(valueSetUrl));
        params.addParameter("code", new CodeType(code));
        params.addParameter("system", new UriType(system));

        // Execute $validate-code operation
        Parameters result = client
            .operation()
            .onType(ValueSet.class)
            .named("$validate-code")
            .withParameters(params)
            .returnResourceType(Parameters.class)
            .execute();

        // Extract result
        for (Parameters.ParametersParameterComponent param : result.getParameter()) {
            if ("result".equals(param.getName())) {
                return param.getValue() instanceof BooleanType &&
                       ((BooleanType) param.getValue()).booleanValue();
            }
        }

        return false;
    }

    public static Parameters lookupCode(String system, String code) {
        // Create parameters for $lookup operation
        Parameters params = new Parameters();
        params.addParameter("system", new UriType(system));
        params.addParameter("code", new CodeType(code));

        // Execute $lookup operation
        return client
            .operation()
            .onType(CodeSystem.class)
            .named("$lookup")
            .withParameters(params)
            .returnResourceType(Parameters.class)
            .execute();
    }

    public static void main(String[] args) {
        String valueSetUrl = "https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs";
        String codeSystemUrl = "https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs";

        // Expand ValueSet
        System.out.println("Expanding ValueSet...");
        List&lt;ValueSet.ValueSetExpansionContainsComponent&gt; codes = expandValueSet(valueSetUrl);
        codes.stream().limit(5).forEach(code ->
            System.out.println("  " + code.getCode() + ": " + code.getDisplay())
        );

        // Validate a code
        System.out.println("\nValidating code '2211.1'...");
        boolean isValid = validateCode(valueSetUrl, "2211.1", codeSystemUrl);
        System.out.println("  Valid: " + isValid);

        // Lookup code details
        System.out.println("\nLooking up code '2211.1'...");
        Parameters details = lookupCode(codeSystemUrl, "2211.1");
        System.out.println("  Details: " + ctx.newJsonParser().encodeResourceToString(details));
    }
}
</code></pre>
    </div>
    <div class="tab-pane" id="csharp">
<pre><code class="language-csharp">using Hl7.Fhir.Model;
using Hl7.Fhir.Rest;
using System;
using System.Collections.Generic;
using System.Linq;

class TerminologyExample
{
    private const string BaseUrl = "https://playground.dhp.uz/fhir";
    private static readonly FhirClient client = new FhirClient(BaseUrl);

    static List&lt;ValueSet.ContainsComponent&gt; ExpandValueSet(string valueSetUrl)
    {
        var parameters = new Parameters();
        parameters.Add("url", new FhirUri(valueSetUrl));

        var expanded = client.TypeOperation&lt;ValueSet&gt;("expand", parameters) as ValueSet;

        return expanded?.Expansion?.Contains?.ToList() ?? new List&lt;ValueSet.ContainsComponent&gt;();
    }

    static bool ValidateCode(string valueSetUrl, string code, string system)
    {
        var parameters = new Parameters();
        parameters.Add("url", new FhirUri(valueSetUrl));
        parameters.Add("code", new Code(code));
        parameters.Add("system", new FhirUri(system));

        var result = client.TypeOperation&lt;ValueSet&gt;("validate-code", parameters) as Parameters;

        var resultParam = result?.Parameter?.FirstOrDefault(p => p.Name == "result");
        return resultParam?.Value is FhirBoolean boolValue && boolValue.Value == true;
    }

    static Parameters LookupCode(string system, string code)
    {
        var parameters = new Parameters();
        parameters.Add("system", new FhirUri(system));
        parameters.Add("code", new Code(code));

        return client.TypeOperation&lt;CodeSystem&gt;("lookup", parameters) as Parameters;
    }

    static void Main()
    {
        var valueSetUrl = "https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs";
        var codeSystemUrl = "https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs";

        // Expand ValueSet
        Console.WriteLine("Expanding ValueSet...");
        var codes = ExpandValueSet(valueSetUrl);
        foreach (var code in codes.Take(5))
        {
            Console.WriteLine($"  {code.Code}: {code.Display}");
        }

        // Validate a code
        Console.WriteLine("\nValidating code '2211.1'...");
        var isValid = ValidateCode(valueSetUrl, "2211.1", codeSystemUrl);
        Console.WriteLine($"  Valid: {isValid}");

        // Lookup code details
        Console.WriteLine("\nLooking up code '2211.1'...");
        var details = LookupCode(codeSystemUrl, "2211.1");
        Console.WriteLine("  Details retrieved successfully");
    }
}
</code></pre>
    </div>
    <div class="tab-pane" id="go">
<pre><code class="language-go">package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io"
    "net/http"
    "net/url"
)

const baseURL = "https://playground.dhp.uz/fhir"

type ValueSetExpansion struct {
    Contains []struct {
        System  string `json:"system"`
        Code    string `json:"code"`
        Display string `json:"display"`
    } `json:"contains"`
}

type ValueSetExpanded struct {
    Expansion ValueSetExpansion `json:"expansion"`
}

type Parameters struct {
    Parameter []struct {
        Name         string `json:"name"`
        ValueBoolean *bool  `json:"valueBoolean,omitempty"`
        ValueString  string `json:"valueString,omitempty"`
    } `json:"parameter"`
}

func expandValueSet(valueSetURL string) ([]struct {
    System  string
    Code    string
    Display string
}, error) {
    params := url.Values{}
    params.Add("url", valueSetURL)

    resp, err := http.Get(fmt.Sprintf("%s/ValueSet/$expand?%s", baseURL, params.Encode()))
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    body, _ := io.ReadAll(resp.Body)

    var expanded ValueSetExpanded
    if err := json.Unmarshal(body, &expanded); err != nil {
        return nil, err
    }

    return expanded.Expansion.Contains, nil
}

func validateCode(valueSetURL, code, system string) (bool, error) {
    params := url.Values{}
    params.Add("url", valueSetURL)
    params.Add("code", code)
    params.Add("system", system)

    resp, err := http.Get(fmt.Sprintf("%s/ValueSet/$validate-code?%s", baseURL, params.Encode()))
    if err != nil {
        return false, err
    }
    defer resp.Body.Close()

    body, _ := io.ReadAll(resp.Body)

    var result Parameters
    if err := json.Unmarshal(body, &result); err != nil {
        return false, err
    }

    for _, param := range result.Parameter {
        if param.Name == "result" && param.ValueBoolean != nil {
            return *param.ValueBoolean, nil
        }
    }

    return false, nil
}

func lookupCode(system, code string) (*Parameters, error) {
    params := url.Values{}
    params.Add("system", system)
    params.Add("code", code)

    resp, err := http.Get(fmt.Sprintf("%s/CodeSystem/$lookup?%s", baseURL, params.Encode()))
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    body, _ := io.ReadAll(resp.Body)

    var result Parameters
    if err := json.Unmarshal(body, &result); err != nil {
        return nil, err
    }

    return &result, nil
}

func main() {
    valueSetURL := "https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs"
    codeSystemURL := "https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs"

    // Expand ValueSet
    fmt.Println("Expanding ValueSet...")
    codes, err := expandValueSet(valueSetURL)
    if err != nil {
        fmt.Printf("Error: %v\n", err)
        return
    }

    for i, code := range codes {
        if i >= 5 {
            break
        }
        fmt.Printf("  %s: %s\n", code.Code, code.Display)
    }

    // Validate a code
    fmt.Println("\nValidating code '2211.1'...")
    isValid, err := validateCode(valueSetURL, "2211.1", codeSystemURL)
    if err != nil {
        fmt.Printf("Error: %v\n", err)
        return
    }
    fmt.Printf("  Valid: %v\n", isValid)

    // Lookup code details
    fmt.Println("\nLooking up code '2211.1'...")
    details, err := lookupCode(codeSystemURL, "2211.1")
    if err != nil {
        fmt.Printf("Error: %v\n", err)
        return
    }
    fmt.Println("  Details retrieved successfully")
    _ = details // Use details as needed
}
</code></pre>
    </div>
  </div>
</div>
