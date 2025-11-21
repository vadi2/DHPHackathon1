# Practitioner and PractitionerRole management

## Overview

Goal: Retrieve existing Practitioner and PractitionerRole records, integrate them into software, update and create as needed, assign roles in organizations, and manage qualifications.

- Resources: Practitioner, PractitionerRole
- Skills: GET/POST/PUT/DELETE operations, search, references, identifiers
- Base URL: `https://playground.dhp.uz/fhir`
- Profiles:
  - [uz-core-practitioner](https://dhp.uz/fhir/core/en/StructureDefinition-uz-core-practitioner.html)
  - [uz-core-practitionerrole](https://dhp.uz/fhir/core/en/StructureDefinition-uz-core-practitionerrole.html)

**Feedback:** Share your experience, issues and successes in the [connectathon document](https://docs.google.com/document/d/1PdQ8zBI9xkISP3tAqIK8-TGMql3kVVZ4UNoHVYqCy4Y/edit?usp=sharing).

## uz-core-practitioner profile

**Note**: Validation is currently disabled on the server, but client applications should follow the profile rules to ensure compatibility and data quality.

### Required elements

There are no mandatory elements with minimum cardinality greater than 0 in this profile. All elements are optional, though Must Support elements should be populated when data is available.

### Must-support elements

UZ Core profiles: Elements marked as Must Support must be populated when exchanging data between systems operating in Uzbekistan.

When data cannot be populated because it is unavailable in the source system, the element may be left empty - provided that cardinality rules allow it. However, when cardinality requirements mandate inclusion, systems must use the Data Absent Reason extension rather than leaving the element empty.

#### Profile elements

- **identifier**: Practitioner identifiers (nationalId from ARGOS system)
- **active**: Practice status
- **name**: Practitioner name
  - **use**: Name use (official, usual, etc.)
  - **text**: Full name as displayed
  - **family**: Family/surname
  - **given**: Given names
  - **suffix**: Name suffix (e.g., Jr., MD)
  - **period**: Time period when name was/is in use
- **telecom**: Contact details (phone, email, etc.)
  - **system**: Contact type (phone, email, fax, etc.)
  - **value**: Actual contact value
  - **use**: Purpose (home, work, mobile, etc.)
  - **rank**: Preference order
  - **period**: Time period when contact is/was valid
- **gender**: Administrative gender (male, female, other, unknown)
  - When gender is "other", the **gender-other extension** (`https://dhp.uz/fhir/core/StructureDefinition/gender-other`) must be included for gender differentiation
- **birthDate**: Date of birth
- **deceased[x]**: Death indicator (boolean) or date/time of death
- **address**: Practitioner addresses with two types:
  - **uzAddress**: Addresses in Uzbekistan (country code "UZ") with support for mahalla. **Must use coded values** from official registries for administrative divisions (state, district, city/mahalla)
  - **i18nAddress**: International addresses (non-Uzbekistan). Administrative divisions use free text without required valuesets
- **photo**: Practitioner photo
- **qualification**: Qualifications obtained by the practitioner
  - **identifier**: Qualification identifier
  - **code**: Qualification code (required)
  - **period**: Qualification validity period
  - **issuer**: Organization that issued the qualification

### Gender differentiation

When a practitioner's gender is set to "other", the profile requires the `gender-other` extension:

```json
{
  "gender": "other",
  "_gender": {
    "extension": [
      {
        "url": "https://dhp.uz/fhir/core/StructureDefinition/gender-other",
        "valueCodeableConcept": {
          "coding": [
            {
              "system": "https://terminology.dhp.uz/fhir/core/CodeSystem/gender-other-cs",
              "code": "regis0007.00005",
              "display": "Changed gender to male"
            }
          ]
        }
      }
    ]
  }
}
```

### Address types

For detailed guidance on working with addresses, see [Working with Addresses](https://dhp.uz/fhir/core/en/fhir-basics.html#working-with-addresses).

**Uzbek address (uzAddress):**
```json
{
  "use": "work",
  "type": "physical",
  "text": "Toshkent shahri, Yashnobod tumani, Qoʻshbegi mahallasi, Bunyodkor koʻchasi, 42-uy",
  "line": ["Bunyodkor koʻchasi, 42-uy"],
  "city": "17262900085",
  "district": "1726290",
  "state": "1726",
  "postalCode": "100084",
  "country": "UZ"
}
```

**International address (i18nAddress):**
```json
{
  "use": "home",
  "type": "postal",
  "line": ["123 Main St", "Apt 4B"],
  "city": "New York",
  "state": "NY",
  "postalCode": "10001",
  "country": "US"
}
```

## uz-core-practitionerrole profile

The PractitionerRole resource describes a specific set of roles, specialties, services, and locations where a practitioner may perform services.

### Key elements

- **identifier**: Business identifiers for this role
- **active**: Whether this practitioner role record is in active use
- **period**: Time period during which the practitioner is authorized to perform in these roles
- **practitioner**: Reference to the Practitioner resource
- **organization**: Reference to the Organization where the roles are performed
- **code**: Roles which this practitioner is authorized to perform
- **specialty**: Specific specialty of the practitioner
- **location**: Location(s) where this practitioner provides care
- **telecom**: Contact details specific to this role
- **endpoint**: Technical endpoints providing access to services operated for the role

### Practitioner-Organization relationship

PractitionerRole links practitioners to organizations where they work:

```json
{
  "resourceType": "PractitionerRole",
  "id": "example",
  "language": "uz",
  "active": true,
  "practitioner": {
    "reference": "Practitioner/123",
    "display": "Dr. Alisher Karimov"
  },
  "organization": {
    "reference": "Organization/456",
    "display": "Toshkent shahar 5-son poliklinika"
  },
  "code": [
    {
      "coding": [
        {
          "system": "https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs",
          "code": "2211.1",
          "display": "General practitioner"
        }
      ]
    }
  ],
  "specialty": [
    {
      "coding": [
        {
          "system": "https://terminology.dhp.uz/fhir/core/CodeSystem/profession-specialization-cs",
          "code": "419772000",
          "display": "Family practice"
        }
      ]
    }
  ]
}
```

## CRUD operations

### Create Practitioner

- HTTP method: POST
- Endpoint: `/Practitioner`
- Headers: `Content-Type: application/fhir+json`

Creating a new practitioner. The server assigns a unique ID and returns a Location header.

Minimal example:
```json
{
  "resourceType": "Practitioner",
  "meta": {
    "profile": ["https://dhp.uz/fhir/core/StructureDefinition/uz-core-practitioner"]
  },
  "language": "uz",
  "identifier": [
    {
      "use": "official",
      "type": {
        "coding": [
          {
            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
            "code": "NI"
          }
        ]
      },
      "system": "https://dhp.uz/fhir/core/sid/pro/uz/argos",
      "value": "12345678"
    }
  ],
  "active": true,
  "name": [
    {
      "use": "official",
      "family": "Karimov",
      "given": ["Alisher", "Akbarovich"]
    }
  ],
  "gender": "male",
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

Response: HTTP 201 Created with Location header and created resource.

### Create PractitionerRole

- HTTP method: POST
- Endpoint: `/PractitionerRole`
- Headers: `Content-Type: application/fhir+json`

Creating a new practitioner role, linking a practitioner to an organization.

Example:
```json
{
  "resourceType": "PractitionerRole",
  "meta": {
    "profile": ["https://dhp.uz/fhir/core/StructureDefinition/uz-core-practitionerrole"]
  },
  "language": "uz",
  "active": true,
  "practitioner": {
    "reference": "Practitioner/123",
    "display": "Dr. Alisher Karimov"
  },
  "organization": {
    "reference": "Organization/456",
    "display": "Toshkent shahar 5-son poliklinika"
  },
  "code": [
    {
      "coding": [
        {
          "system": "https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs",
          "code": "2211.1",
          "display": "General practitioner"
        }
      ]
    }
  ],
  "specialty": [
    {
      "coding": [
        {
          "system": "https://terminology.dhp.uz/fhir/core/CodeSystem/profession-specialization-cs",
          "code": "419772000",
          "display": "Family practice"
        }
      ]
    }
  ]
}
```

Response: HTTP 201 Created with Location header and created resource.

### Read Practitioner

- HTTP method: GET
- Endpoint: `/Practitioner/[id]`

Retrieving a specific practitioner by ID. The system has many practitioners already loaded from the Argos HRM system.

Response: HTTP 200 OK with Practitioner resource or HTTP 404 Not Found.

### Read PractitionerRole

- HTTP method: GET
- Endpoint: `/PractitionerRole/[id]`

Retrieving a specific practitioner role by ID.

Response: HTTP 200 OK with PractitionerRole resource or HTTP 404 Not Found.

### Update Practitioner

- HTTP method: PUT
- Endpoint: `/Practitioner/[id]`
- Headers:
  - `Content-Type: application/fhir+json`
  - `If-Match: W/"[versionId]"` (required to prevent conflicts)

Full update of a practitioner. The entire resource must be sent, including the `id` element. The `If-Match` header is required and must contain the resource version from the `meta.versionId` element to prevent conflicts during concurrent editing (optimistic locking).

Request example:
```
PUT /Practitioner/existing-id
If-Match: W/"2"
Content-Type: application/fhir+json
```

Request body example:
```json
{
  "resourceType": "Practitioner",
  "id": "existing-id",
  "meta": {
    "profile": ["https://dhp.uz/fhir/core/StructureDefinition/uz-core-practitioner"]
  },
  "language": "uz",
  "identifier": [...],
  "active": true,
  "name": [
    {
      "use": "official",
      "family": "Karimov",
      "given": ["Alisher", "Akbarovich"]
    }
  ],
  "gender": "male",
  "qualification": [...]
}
```

Response: HTTP 200 OK with updated resource.

### Update PractitionerRole

- HTTP method: PUT
- Endpoint: `/PractitionerRole/[id]`
- Headers:
  - `Content-Type: application/fhir+json`
  - `If-Match: W/"[versionId]"` (required to prevent conflicts)

Full update of a practitioner role. The entire resource must be sent, including the `id` element. The `If-Match` header is required for optimistic locking.

Response: HTTP 200 OK with updated resource.

### Delete Practitioner

- HTTP method: DELETE
- Endpoint: `/Practitioner/[id]`

Deleting a practitioner.

Response: HTTP 200 OK with OperationOutcome on successful deletion. When attempting to read a deleted resource, the server will return HTTP 410 Gone.

### Delete PractitionerRole

- HTTP method: DELETE
- Endpoint: `/PractitionerRole/[id]`

Deleting a practitioner role.

Response: HTTP 200 OK with OperationOutcome on successful deletion. When attempting to read a deleted resource, the server will return HTTP 410 Gone.

## Search operations

- HTTP method: GET
- Endpoint: `/Practitioner?[parameters]` or `/PractitionerRole?[parameters]`

All supported search parameters can be found in the capability statement at [DHPCapabilityStatement](https://dhp.uz/fhir/core/en/CapabilityStatement-DHPCapabilityStatement.html) or by querying the [/metadata](https://playground.dhp.uz/fhir/metadata) endpoint.

### Practitioner search parameters

| Parameter | Type | Description | Example |
|----------|-----|----------|--------|
| `_id` | token | Search by ID | `?_id=123` |
| `identifier` | token | Search by identifier | `?identifier=https://dhp.uz/fhir/core/sid/pro/uz/argos\|12345` |
| `name` | string | Search by name (partial match) | `?name=Karimov` |
| `given` | string | Search by given name | `?given=Alisher` |
| `family` | string | Search by family name | `?family=Karimov` |
| `telecom` | token | Search by contact details | `?telecom=%2B998901234567` |
| `phone` | token | Search by phone number | `?phone=%2B998901234567` |
| `email` | token | Search by email | `?email=doctor@example.com` |
| `address` | string | Search by address | `?address=Toshkent` |
| `address-city` | string | Search by city | `?address-city=Toshkent` |
| `address-country` | string | Search by country | `?address-country=UZ` |
| `address-postalcode` | string | Search by postal code | `?address-postalcode=100084` |
| `address-state` | string | Search by state/region | `?address-state=Toshkent` |
| `gender` | token | Search by gender | `?gender=male` |
| `birthdate` | date | Search by birth date | `?birthdate=1980-05-15` |
| `active` | token | Filter by status | `?active=true` |
| `deceased` | token | Filter by deceased status | `?deceased=false` |
| `qualification-code` | token | Search by qualification | `?qualification-code=MD` |

### PractitionerRole search parameters

| Parameter | Type | Description | Example |
|----------|-----|----------|--------|
| `_id` | token | Search by ID | `?_id=456` |
| `identifier` | token | Search by identifier | `?identifier=system\|value` |
| `practitioner` | reference | Search by practitioner | `?practitioner=Practitioner/123` |
| `organization` | reference | Search by organization | `?organization=Organization/789` |
| `location` | reference | Search by location | `?location=Location/101` |
| `role` | token | Search by role | `?role=doctor` |
| `specialty` | token | Search by specialty | `?specialty=394814009` |
| `active` | token | Filter by status | `?active=true` |
| `date` | date | Search by period | `?date=2024` |
| `service` | reference | Search by service | `?service=HealthcareService/202` |
| `endpoint` | reference | Search by endpoint | `?endpoint=Endpoint/303` |
| `telecom` | token | Search by contact | `?telecom=phone\|%2B998901234567` |
| `phone` | token | Search by phone | `?phone=%2B998901234567` |

### Common search patterns

**Find practitioners by name:**
```
GET /Practitioner?name=Karimov
```

**Find practitioners in a specific city:**
```
GET /Practitioner?address-city=Toshkent&active=true
```

**Find all roles for a specific practitioner:**
```
GET /PractitionerRole?practitioner=Practitioner/123
```

**Find all practitioners working at a specific organization:**
```
GET /PractitionerRole?organization=Organization/789
```

**Find practitioners by qualification:**
```
GET /Practitioner?qualification-code=http://terminology.hl7.org/CodeSystem/v2-0360|MD
```

**Find active specialists of a specific type:**
```
GET /PractitionerRole?specialty=https://terminology.dhp.uz/fhir/core/CodeSystem/profession-specialization-cs|419772000&active=true
```

### Modifiers and prefixes

Combining parameters (logical AND):
```
GET /Practitioner?family=Karimov&address-city=Toshkent&active=true
```

Multiple values (logical OR):
```
GET /Practitioner?gender=male,female
```

Date comparisons:
```
GET /Practitioner?birthdate=gt1980-01-01&birthdate=lt1990-12-31
```

### Pagination

Search results are returned in a Bundle with pagination (20 records per page):

```json
{
  "resourceType": "Bundle",
  "type": "searchset",
  "total": 150,
  "link": [
    {
      "relation": "self",
      "url": "https://playground.dhp.uz/fhir/Practitioner?name=Karimov&_page=1"
    },
    {
      "relation": "next",
      "url": "https://playground.dhp.uz/fhir/Practitioner?name=Karimov&_page=2"
    }
  ],
  "entry": [...]
}
```

Use `Bundle.link` with `relation="next"` to get the next page.

**Known issue**: The `Bundle.total` field may return `0` even when results are present. To count practitioners on the current page, filter `Bundle.entry` by `resourceType == "Practitioner"` (the response may contain `OperationOutcome` resources).

## Integration workflow

### Typical integration scenario

1. **Search for practitioners** in your organization:
   ```
   GET /PractitionerRole?organization=Organization/your-org-id
   ```

2. **Get practitioner details** for each role:
   ```
   GET /Practitioner/practitioner-id
   ```

3. **Retrieve qualifications** from the Practitioner resource

4. **Get additional role details** if needed:
   ```
   GET /PractitionerRole/role-id
   ```

### Finding practitioners and their organizations

To find all practitioners and where they work:

```
GET /PractitionerRole?_include=PractitionerRole:practitioner&_include=PractitionerRole:organization
```

This will return PractitionerRole resources along with the referenced Practitioner and Organization resources in a single Bundle.

## Error handling

### Response codes

| Code | Description |
|-----|----------|
| 200 | OK - successful retrieval |
| 400 | Bad Request - invalid search parameters |
| 404 | Not Found - resource not found |
| 410 | Gone - resource was deleted |

### OperationOutcome

On errors, the server returns an OperationOutcome:

```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "not-found",
      "diagnostics": "Resource Practitioner/invalid-id not found"
    }
  ]
}
```

## Example practitioners in the system

The system contains practitioners loaded from the Argos HRM system, including:
- Physicians with various specialties (general practice, cardiology, pediatrics, etc.)
- Nurses
- Laboratory specialists
- Administrative staff
- Medical technicians

Each practitioner has:
- National identifier from ARGOS
- Full name in Uzbek (with possible Russian and Karakalpak translations)
- Contact information
- Address (typically in Uzbekistan)
- Qualifications and specializations
- Associated roles in healthcare organizations

## Useful links

- [FHIR Practitioner Resource](http://hl7.org/fhir/R5/practitioner.html)
- [FHIR PractitionerRole Resource](http://hl7.org/fhir/R5/practitionerrole.html)
- [uz-core-practitioner Profile](https://dhp.uz/fhir/core/en/StructureDefinition-uz-core-practitioner.html)
- [uz-core-practitionerrole Profile](https://dhp.uz/fhir/core/en/StructureDefinition-uz-core-practitionerrole.html)
- [FHIR RESTful API](http://hl7.org/fhir/R5/http.html)
- [FHIR Search](http://hl7.org/fhir/R5/search.html)

---

## Code examples

{% include code-tabs-style.html %}

Below are examples of creating a new practitioner in various programming languages:

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
<pre><code class="language-bash">curl -X POST "https://playground.dhp.uz/fhir/Practitioner" \
  -H "Content-Type: application/fhir+json" \
  -d '{
  "resourceType": "Practitioner",
  "meta": {
    "profile": ["https://dhp.uz/fhir/core/StructureDefinition/uz-core-practitioner"]
  },
  "language": "uz",
  "identifier": [
    {
      "use": "official",
      "type": {
        "coding": [
          {
            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
            "code": "NI"
          }
        ]
      },
      "system": "https://dhp.uz/fhir/core/sid/pro/uz/argos",
      "value": "12345678"
    }
  ],
  "active": true,
  "name": [
    {
      "use": "official",
      "family": "Karimov",
      "given": ["Alisher", "Akbarovich"]
    }
  ],
  "gender": "male",
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
}'
</code></pre>
    </div>
    <div class="tab-pane" id="python">
<pre><code class="language-python">import requests
from fhir.resources.practitioner import Practitioner
from fhir.resources.identifier import Identifier
from fhir.resources.humanname import HumanName
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.meta import Meta

# FHIR server base URL
base_url = "https://playground.dhp.uz/fhir"

# Creating a new practitioner using fhir.resources
practitioner = Practitioner(
    meta=Meta(
        profile=["https://dhp.uz/fhir/core/StructureDefinition/uz-core-practitioner"]
    ),
    language="uz",
    identifier=[
        Identifier(
            use="official",
            system="https://dhp.uz/fhir/core/sid/pro/uz/argos",
            type=CodeableConcept(
                coding=[
                    Coding(
                        system="http://terminology.hl7.org/CodeSystem/v2-0203",
                        code="NI"
                    )
                ]
            ),
            value="12345678"
        )
    ],
    active=True,
    name=[
        HumanName(
            use="official",
            family="Karimov",
            given=["Alisher", "Akbarovich"]
        )
    ],
    gender="male",
    qualification=[
        {
            "code": CodeableConcept(
                coding=[
                    Coding(
                        system="http://terminology.hl7.org/CodeSystem/v2-0360",
                        code="MD",
                        display="Doctor of Medicine"
                    )
                ]
            )
        }
    ]
)

# Sending POST request
response = requests.post(
    f"{base_url}/Practitioner",
    headers={"Content-Type": "application/fhir+json"},
    data=practitioner.json()
)

if response.status_code == 201:
    created_practitioner = response.json()
    print(f"Practitioner created with ID: {created_practitioner['id']}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
</code></pre>
    </div>
    <div class="tab-pane" id="javascript">
<pre><code class="language-javascript">// Using fetch API
const baseUrl = "https://playground.dhp.uz/fhir";

const practitioner = {
  resourceType: "Practitioner",
  meta: {
    profile: ["https://dhp.uz/fhir/core/StructureDefinition/uz-core-practitioner"]
  },
  language: "uz",
  identifier: [
    {
      use: "official",
      type: {
        coding: [
          {
            system: "http://terminology.hl7.org/CodeSystem/v2-0203",
            code: "NI"
          }
        ]
      },
      system: "https://dhp.uz/fhir/core/sid/pro/uz/argos",
      value: "12345678"
    }
  ],
  active: true,
  name: [
    {
      use: "official",
      family: "Karimov",
      given: ["Alisher", "Akbarovich"]
    }
  ],
  gender: "male",
  qualification: [
    {
      code: {
        coding: [
          {
            system: "http://terminology.hl7.org/CodeSystem/v2-0360",
            code: "MD",
            display: "Doctor of Medicine"
          }
        ]
      }
    }
  ]
};

// Creating practitioner
fetch(`${baseUrl}/Practitioner`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/fhir+json'
  },
  body: JSON.stringify(practitioner)
})
.then(response => {
  if (response.status === 201) {
    return response.json();
  }
  throw new Error(`Error: ${response.status}`);
})
.then(data => {
  console.log(`Practitioner created with ID: ${data.id}`);
})
.catch(error => {
  console.error('Error:', error);
});
</code></pre>
    </div>
    <div class="tab-pane" id="java">
<pre><code class="language-java">import ca.uhn.fhir.context.FhirContext;
import ca.uhn.fhir.rest.client.api.IGenericClient;
import org.hl7.fhir.r5.model.*;

// Creating FHIR context and client
FhirContext ctx = FhirContext.forR5();
IGenericClient client = ctx.newRestfulGenericClient("https://playground.dhp.uz/fhir");

// Creating practitioner
Practitioner practitioner = new Practitioner();

// Setting profile
practitioner.getMeta()
    .addProfile("https://dhp.uz/fhir/core/StructureDefinition/uz-core-practitioner");

// Setting language
practitioner.setLanguage("uz");

// Adding identifier
Identifier nationalId = practitioner.addIdentifier();
nationalId.setUse(Identifier.IdentifierUse.OFFICIAL);
nationalId.setSystem("https://dhp.uz/fhir/core/sid/pro/uz/argos");
nationalId.setValue("12345678");
CodeableConcept idType = new CodeableConcept();
idType.addCoding()
    .setSystem("http://terminology.hl7.org/CodeSystem/v2-0203")
    .setCode("NI");
nationalId.setType(idType);

// Setting status
practitioner.setActive(true);

// Adding name
HumanName name = practitioner.addName();
name.setUse(HumanName.NameUse.OFFICIAL);
name.setFamily("Karimov");
name.addGiven("Alisher");
name.addGiven("Akbarovich");

// Setting gender
practitioner.setGender(Enumerations.AdministrativeGender.MALE);

// Adding qualification
Practitioner.PractitionerQualificationComponent qual = practitioner.addQualification();
CodeableConcept qualCode = new CodeableConcept();
qualCode.addCoding()
    .setSystem("http://terminology.hl7.org/CodeSystem/v2-0360")
    .setCode("MD")
    .setDisplay("Doctor of Medicine");
qual.setCode(qualCode);

// Creating on server
MethodOutcome outcome = client.create()
    .resource(practitioner)
    .execute();

// Getting ID of created practitioner
IdType id = (IdType) outcome.getId();
System.out.println("Practitioner created with ID: " + id.getIdPart());
</code></pre>
    </div>
    <div class="tab-pane" id="csharp">
<pre><code class="language-csharp">using Hl7.Fhir.Model;
using Hl7.Fhir.Rest;
using System;

// Creating FHIR client
var client = new FhirClient("https://playground.dhp.uz/fhir");

// Creating practitioner
var practitioner = new Practitioner
{
    Meta = new Meta
    {
        Profile = new[] { "https://dhp.uz/fhir/core/StructureDefinition/uz-core-practitioner" }
    },
    Language = "uz",
    Identifier = new List&lt;Identifier&gt;
    {
        new Identifier
        {
            Use = Identifier.IdentifierUse.Official,
            System = "https://dhp.uz/fhir/core/sid/pro/uz/argos",
            Type = new CodeableConcept
            {
                Coding = new List&lt;Coding&gt;
                {
                    new Coding
                    {
                        System = "http://terminology.hl7.org/CodeSystem/v2-0203",
                        Code = "NI"
                    }
                }
            },
            Value = "12345678"
        }
    },
    Active = true,
    Name = new List&lt;HumanName&gt;
    {
        new HumanName
        {
            Use = HumanName.NameUse.Official,
            Family = "Karimov",
            Given = new[] { "Alisher", "Akbarovich" }
        }
    },
    Gender = AdministrativeGender.Male,
    Qualification = new List&lt;Practitioner.QualificationComponent&gt;
    {
        new Practitioner.QualificationComponent
        {
            Code = new CodeableConcept
            {
                Coding = new List&lt;Coding&gt;
                {
                    new Coding
                    {
                        System = "http://terminology.hl7.org/CodeSystem/v2-0360",
                        Code = "MD",
                        Display = "Doctor of Medicine"
                    }
                }
            }
        }
    }
};

// Creating on server
var createdPractitioner = client.Create(practitioner);
Console.WriteLine($"Practitioner created with ID: {createdPractitioner.Id}");
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
)

type Practitioner struct {
    ResourceType  string                        `json:"resourceType"`
    ID            string                        `json:"id,omitempty"`
    Meta          *Meta                         `json:"meta,omitempty"`
    Language      string                        `json:"language,omitempty"`
    Identifier    []Identifier                  `json:"identifier,omitempty"`
    Active        bool                          `json:"active"`
    Name          []HumanName                   `json:"name,omitempty"`
    Gender        string                        `json:"gender,omitempty"`
    Qualification []PractitionerQualification   `json:"qualification,omitempty"`
}

type Meta struct {
    Profile []string `json:"profile"`
}

type Identifier struct {
    Use    string           `json:"use,omitempty"`
    System string           `json:"system"`
    Type   *CodeableConcept `json:"type,omitempty"`
    Value  string           `json:"value"`
}

type HumanName struct {
    Use    string   `json:"use,omitempty"`
    Family string   `json:"family,omitempty"`
    Given  []string `json:"given,omitempty"`
}

type CodeableConcept struct {
    Coding []Coding `json:"coding,omitempty"`
}

type Coding struct {
    System  string `json:"system"`
    Code    string `json:"code"`
    Display string `json:"display,omitempty"`
}

type PractitionerQualification struct {
    Code CodeableConcept `json:"code"`
}

func main() {
    baseURL := "https://playground.dhp.uz/fhir"

    // Creating practitioner
    pract := Practitioner{
        ResourceType: "Practitioner",
        Meta: &amp;Meta{
            Profile: []string{"https://dhp.uz/fhir/core/StructureDefinition/uz-core-practitioner"},
        },
        Language: "uz",
        Identifier: []Identifier{
            {
                Use:    "official",
                System: "https://dhp.uz/fhir/core/sid/pro/uz/argos",
                Type: &amp;CodeableConcept{
                    Coding: []Coding{
                        {
                            System: "http://terminology.hl7.org/CodeSystem/v2-0203",
                            Code:   "NI",
                        },
                    },
                },
                Value: "12345678",
            },
        },
        Active: true,
        Name: []HumanName{
            {
                Use:    "official",
                Family: "Karimov",
                Given:  []string{"Alisher", "Akbarovich"},
            },
        },
        Gender: "male",
        Qualification: []PractitionerQualification{
            {
                Code: CodeableConcept{
                    Coding: []Coding{
                        {
                            System:  "http://terminology.hl7.org/CodeSystem/v2-0360",
                            Code:    "MD",
                            Display: "Doctor of Medicine",
                        },
                    },
                },
            },
        },
    }

    // Serializing to JSON
    jsonData, err := json.Marshal(pract)
    if err != nil {
        panic(err)
    }

    // Sending POST request
    resp, err := http.Post(
        baseURL+"/Practitioner",
        "application/fhir+json",
        bytes.NewBuffer(jsonData),
    )
    if err != nil {
        panic(err)
    }
    defer resp.Body.Close()

    if resp.StatusCode == 201 {
        body, _ := io.ReadAll(resp.Body)
        var createdPract Practitioner
        json.Unmarshal(body, &amp;createdPract)
        fmt.Printf("Practitioner created with ID: %s\n", createdPract.ID)
    } else {
        fmt.Printf("Error: %d\n", resp.StatusCode)
    }
}
</code></pre>
    </div>
  </div>
</div>
