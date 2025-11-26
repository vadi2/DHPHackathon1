# Organization management

## Overview

Goal: Retrieve existing organizations and departments, integrate them into software, update and create as needed.

- Resources: Organization
- Skills: GET/POST/PUT/DELETE operations, search, references, identifiers
- Base URL: `https://playground.dhp.uz/fhir`
- Profile: [uz-core-organization](https://dhp.uz/fhir/core/en/StructureDefinition-uz-core-organization.html)

**Feedback:** Share your experience, issues and successes in the [connectathon document](https://docs.google.com/document/d/1PdQ8zBI9xkISP3tAqIK8-TGMql3kVVZ4UNoHVYqCy4Y/edit?usp=sharing).

## uz-core-organization profile

**Note**: Validation is currently disabled on the server but is expected to be enabled for the connectathon. Client applications should follow the profile rules to ensure compatibility and data quality.

### Required elements

- **name** (1..1): Organization name in Uzbek language

#### Name translations

To add translations of the name in Russian and Karakalpak languages, use the standard [translation](http://hl7.org/fhir/R5/extension-translation.html) extension. The extension is applied to the `_name` element:

```json
{
  "language": "uz",
  "name": "Toshkent viloyati yuqumli kasalliklar shifoxonasi",
  "_name": {
    "extension": [
      {
        "extension": [
          {"url": "lang", "valueCode": "ru"},
          {
            "url": "content",
            "valueString": "Ташкентская областная инфекционная больница"
          }
        ],
        "url": "http://hl7.org/fhir/StructureDefinition/translation"
      },
      {
        "extension": [
          {"url": "lang", "valueCode": "kaa"},
          {
            "url": "content",
            "valueString": "Tashkent wálayat juqpalı kesellikler emlewxanası"
          }
        ],
        "url": "http://hl7.org/fhir/StructureDefinition/translation"
      }
    ]
  }
}
```

Language codes:
- `uz` - Uzbek (primary language for the `name` field)
- `ru` - Russian
- `kaa` - Karakalpak

### Must-support elements

UZ Core profiles: Elements marked as Must Support must be populated when exchanging data between systems operating in Uzbekistan.

When data cannot be populated because it is unavailable in the source system, the element may be left empty - provided that cardinality rules allow it. However, when cardinality requirements mandate inclusion, systems must use the Data Absent Reason extension rather than leaving the element empty.

#### Profile elements

- **identifier**: Organization identifiers
  - **taxId**: Tax identifier (`system`: `https://dhp.uz/fhir/core/sid/org/uz/soliq`)
  - **argosId**: ARGOS identifier (`system`: `https://dhp.uz/fhir/core/sid/org/uz/argos`)
- **active**: Activity status
- **type**: Organization type. The element uses multiple coding systems to classify organizations across different dimensions:
  - Nomenclature group (nomenclatureGroup) - institutional grouping
  - Organizational service group (organizationalServiceGroup) - classification by provided services
  - Organizational structure (organizationalStructure) - structural classification
  - Organization type (organizationType) - primary institution type
  - Specialization (specialization) - medical specialization
  - Subordination group (subordinationGroup) - administrative subordination
  - Without legal status (withoutLegalStatus) - legal status

  Valid codes for each dimension can be found in the corresponding ValueSets bound to each slice in the [uz-core-organization profile](https://dhp.uz/fhir/core/en/StructureDefinition-uz-core-organization.html).
- **partOf**: Reference to parent organization

## CRUD operations

### Create

- HTTP method: POST
- Endpoint: `/Organization`
- Headers: `Content-Type: application/fhir+json`

Creating a new organization. The server assigns a unique ID and returns a Location header.

Minimal example:
```json
{
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
      "value": "123456789"
    }
  ],
  "active": true,
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
  "name": "Yangi tibbiyot muassasasi"
}
```

Response: HTTP 201 Created with Location header and created resource.

### Read

- HTTP method: GET
- Endpoint: `/Organization/[id]`

Retrieving a specific organization by ID. The system has many organizations and their departments already loaded from the Argos HRM personnel management system.

Response: HTTP 200 OK with Organization resource or HTTP 404 Not Found.

### Update

- HTTP method: PUT
- Endpoint: `/Organization/[id]`
- Headers:
  - `Content-Type: application/fhir+json`
  - `If-Match: W/"[versionId]"` (required to prevent conflicts)

Full update of an organization. The entire resource must be sent, including the `id` element. The `If-Match` header is required and must contain the resource version from the `meta.versionId` element to prevent conflicts during concurrent editing (optimistic locking).

Request example:
```
PUT /Organization/existing-id
If-Match: W/"2"
Content-Type: application/fhir+json
```

Request body example:
```json
{
  "resourceType": "Organization",
  "id": "existing-id",
  "meta": {
    "profile": ["https://dhp.uz/fhir/core/StructureDefinition/uz-core-organization"]
  },
  "identifier": [...],
  "active": true,
  "name": "Updated name"
}
```

Response: HTTP 200 OK with updated resource.

### Delete

- HTTP method: DELETE
- Endpoint: `/Organization/[id]`

Deleting an organization.

Response: HTTP 200 OK with OperationOutcome on successful deletion. When attempting to read a deleted resource, the server will return HTTP 410 Gone.

## Search

- HTTP method: GET
- Endpoint: `/Organization?[parameters]`

### Search parameters

All supported search parameters can be found in the capability statement at [DHPCapabilityStatement](https://dhp.uz/fhir/core/en/CapabilityStatement-DHPCapabilityStatement.html) or by querying the [/metadata](https://playground.dhp.uz/fhir/metadata) endpoint.

| Parameter | Type | Description | Example |
|----------|-----|----------|--------|
| `_id` | token | Search by ID | `?_id=123` |
| `identifier` | token | Search by identifier | `?identifier=https://dhp.uz/fhir/core/sid/org/uz/soliq\|123456789` |
| `name` | string | Search by name (partial match) | `?name=Fergana` |
| `name:exact` | string | Exact name match | `?name:exact=Fergana` |
| `type` | token | Search by organization type | `?type=prov` |
| `active` | token | Filter by status | `?active=true` |
| `partof` | reference | Search for departments | `?partof=Organization/parent-id` |

### Modifiers and prefixes

Combining parameters (logical AND):
```
GET /Organization?name=Hospital&active=true
```

Multiple values (logical OR):
```
GET /Organization?type=prov,dept
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
      "url": "https://playground.dhp.uz/fhir/Organization?_page=1"
    },
    {
      "relation": "next",
      "url": "https://playground.dhp.uz/fhir/Organization?_page=2"
    }
  ],
  "entry": [...]
}
```

Use `Bundle.link` with `relation="next"` to get the next page.

**Known issue**: The `Bundle.total` field may return `0` even when results are present. To count organizations on the current page, filter `Bundle.entry` by `resourceType == "Organization"` (the response may contain `OperationOutcome` resources).

## Organization hierarchy

Departments are linked to parent organizations through the `partOf` element:

```json
{
  "resourceType": "Organization",
  "name": "Endoskopiya kabineti",
  "type": [
    {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/organization-type",
          "code": "dept"
        }
      ]
    }
  ],
  "partOf": {
    "reference": "Organization/parent-org-id",
    "display": "Asosiy shifoxona"
  }
}
```

Get all departments of an organization:
```
GET /Organization?partof=Organization/parent-org-id
```

## Error handling

### Response codes

| Code | Description |
|-----|----------|
| 200 | OK - successful retrieval/update/deletion |
| 201 | Created - successful creation |
| 400 | Bad Request - invalid JSON |
| 404 | Not Found - resource not found |
| 409 | Conflict - version conflict |
| 410 | Gone - resource was deleted |
| 412 | Precondition Failed - If-Match header not provided or version mismatch |
| 422 | Unprocessable Entity - failed profile validation |

### OperationOutcome

On errors, the server returns an OperationOutcome:

```json
{
  "resourceType": "OperationOutcome",
  "issue": [
    {
      "severity": "error",
      "code": "invalid",
      "diagnostics": "Organization.name: minimum required = 1, but only found 0"
    }
  ]
}
```

## Example organizations in the system

Organization types:
- **prov** (Healthcare Provider): Medical institutions
- **dept** (Department): Departments and offices

Examples of medical institutions (type=prov):
- Farg'ona tumani sanitariya-epidemiologik osoyishtalik va jamoat salomatligi bo'limi
- Yashnobod tumani tibbiyot birlashmasi - 32-son oilaviy poliklinikasi
- Tumanlararo 4-son Teri tanosil kasalliklari dispanseri

Examples of departments (type=dept):
- Эндоскопия кабинети (Endoscopy Cabinet)
- Бактериология лабораторияси (Bacteriology Laboratory)

## Useful links

- [FHIR Organization Resource](http://hl7.org/fhir/R5/organization.html)
- [uz-core-organization Profile](https://dhp.uz/fhir/core/en/StructureDefinition-uz-core-organization.html)
- [FHIR RESTful API](http://hl7.org/fhir/R5/http.html)
- [FHIR Search](http://hl7.org/fhir/R5/search.html)

---

## Code examples

{% include code-tabs-style.html %}

Below are examples of creating a new organization in various programming languages:

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
<pre><code class="language-bash">curl -X POST "https://playground.dhp.uz/fhir/Organization" \
  -H "Content-Type: application/fhir+json" \
  -d '{
  "resourceType": "Organization",
  "meta": {
    "profile": ["https://dhp.uz/fhir/core/StructureDefinition/uz-core-organization"]
  },
  "identifier": [
    {
      "system": "https://dhp.uz/fhir/core/sid/org/uz/soliq",
      "type": {
        "coding": [
          {
            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
            "code": "TAX"
          }
        ]
      },
      "value": "123456789"
    }
  ],
  "active": true,
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
  "name": "Yangi tibbiyot muassasasi"
}'
</code></pre>
    </div>
    <div class="tab-pane" id="python">
<pre><code class="language-python">import requests
from fhir.resources.organization import Organization
from fhir.resources.identifier import Identifier
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.meta import Meta

# FHIR server base URL
base_url = "https://playground.dhp.uz/fhir"

# Creating a new organization using fhir.resources
organization = Organization(
    meta=Meta(
        profile=["https://dhp.uz/fhir/core/StructureDefinition/uz-core-organization"]
    ),
    identifier=[
        Identifier(
            system="https://dhp.uz/fhir/core/sid/org/uz/soliq",
            type=CodeableConcept(
                coding=[
                    Coding(
                        system="http://terminology.hl7.org/CodeSystem/v2-0203",
                        code="TAX"
                    )
                ]
            ),
            value="123456789"
        )
    ],
    active=True,
    type=[
        CodeableConcept(
            coding=[
                Coding(
                    system="http://terminology.hl7.org/CodeSystem/organization-type",
                    code="prov",
                    display="Healthcare Provider"
                )
            ]
        )
    ],
    name="Yangi tibbiyot muassasasi"
)

# Sending POST request
response = requests.post(
    f"{base_url}/Organization",
    headers={"Content-Type": "application/fhir+json"},
    data=organization.json()
)

if response.status_code == 201:
    created_org = response.json()
    print(f"Organization created with ID: {created_org['id']}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
</code></pre>
    </div>
    <div class="tab-pane" id="javascript">
<pre><code class="language-javascript">// Using fetch API
const baseUrl = "https://playground.dhp.uz/fhir";

const organization = {
  resourceType: "Organization",
  meta: {
    profile: ["https://dhp.uz/fhir/core/StructureDefinition/uz-core-organization"]
  },
  identifier: [
    {
      system: "https://dhp.uz/fhir/core/sid/org/uz/soliq",
      type: {
        coding: [
          {
            system: "http://terminology.hl7.org/CodeSystem/v2-0203",
            code: "TAX"
          }
        ]
      },
      value: "123456789"
    }
  ],
  active: true,
  type: [
    {
      coding: [
        {
          system: "http://terminology.hl7.org/CodeSystem/organization-type",
          code: "prov",
          display: "Healthcare Provider"
        }
      ]
    }
  ],
  name: "Yangi tibbiyot muassasasi"
};

// Creating organization
fetch(`${baseUrl}/Organization`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/fhir+json'
  },
  body: JSON.stringify(organization)
})
.then(response =&gt; {
  if (response.status === 201) {
    return response.json();
  }
  throw new Error(`Error: ${response.status}`);
})
.then(data =&gt; {
  console.log(`Organization created with ID: ${data.id}`);
})
.catch(error =&gt; {
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

// Creating organization
Organization organization = new Organization();

// Setting profile
organization.getMeta()
    .addProfile("https://dhp.uz/fhir/core/StructureDefinition/uz-core-organization");

// Adding identifier
Identifier taxId = organization.addIdentifier();
taxId.setSystem("https://dhp.uz/fhir/core/sid/org/uz/soliq");
taxId.setValue("123456789");
CodeableConcept taxType = new CodeableConcept();
taxType.addCoding()
    .setSystem("http://terminology.hl7.org/CodeSystem/v2-0203")
    .setCode("TAX");
taxId.setType(taxType);

// Setting status
organization.setActive(true);

// Adding type
CodeableConcept orgType = new CodeableConcept();
orgType.addCoding()
    .setSystem("http://terminology.hl7.org/CodeSystem/organization-type")
    .setCode("prov")
    .setDisplay("Healthcare Provider");
organization.addType(orgType);

// Setting name
organization.setName("Yangi tibbiyot muassasasi");

// Creating on server
MethodOutcome outcome = client.create()
    .resource(organization)
    .execute();

// Getting ID of created organization
IdType id = (IdType) outcome.getId();
System.out.println("Organization created with ID: " + id.getIdPart());
</code></pre>
    </div>
    <div class="tab-pane" id="csharp">
<pre><code class="language-csharp">using Hl7.Fhir.Model;
using Hl7.Fhir.Rest;
using System;

// Creating FHIR client
var client = new FhirClient("https://playground.dhp.uz/fhir");

// Creating organization
var organization = new Organization
{
    Meta = new Meta
    {
        Profile = new[] { "https://dhp.uz/fhir/core/StructureDefinition/uz-core-organization" }
    },
    Identifier = new List&lt;Identifier&gt;
    {
        new Identifier
        {
            System = "https://dhp.uz/fhir/core/sid/org/uz/soliq",
            Type = new CodeableConcept
            {
                Coding = new List&lt;Coding&gt;
                {
                    new Coding
                    {
                        System = "http://terminology.hl7.org/CodeSystem/v2-0203",
                        Code = "TAX"
                    }
                }
            },
            Value = "123456789"
        }
    },
    Active = true,
    Type = new List&lt;CodeableConcept&gt;
    {
        new CodeableConcept
        {
            Coding = new List&lt;Coding&gt;
            {
                new Coding
                {
                    System = "http://terminology.hl7.org/CodeSystem/organization-type",
                    Code = "prov",
                    Display = "Healthcare Provider"
                }
            }
        }
    },
    Name = "Yangi tibbiyot muassasasi"
};

// Creating on server
var createdOrg = client.Create(organization);
Console.WriteLine($"Organization created with ID: {createdOrg.Id}");
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

type Organization struct {
    ResourceType string                 `json:"resourceType"`
    ID           string                 `json:"id,omitempty"`
    Meta         *Meta                  `json:"meta,omitempty"`
    Identifier   []Identifier           `json:"identifier,omitempty"`
    Active       bool                   `json:"active"`
    Type         []CodeableConcept      `json:"type,omitempty"`
    Name         string                 `json:"name"`
}

type Meta struct {
    Profile []string `json:"profile"`
}

type Identifier struct {
    System string           `json:"system"`
    Type   *CodeableConcept `json:"type,omitempty"`
    Value  string           `json:"value"`
}

type CodeableConcept struct {
    Coding []Coding `json:"coding,omitempty"`
}

type Coding struct {
    System  string `json:"system"`
    Code    string `json:"code"`
    Display string `json:"display,omitempty"`
}

func main() {
    baseURL := "https://playground.dhp.uz/fhir"

    // Creating organization
    org := Organization{
        ResourceType: "Organization",
        Meta: &amp;Meta{
            Profile: []string{"https://dhp.uz/fhir/core/StructureDefinition/uz-core-organization"},
        },
        Identifier: []Identifier{
            {
                System: "https://dhp.uz/fhir/core/sid/org/uz/soliq",
                Type: &amp;CodeableConcept{
                    Coding: []Coding{
                        {
                            System: "http://terminology.hl7.org/CodeSystem/v2-0203",
                            Code:   "TAX",
                        },
                    },
                },
                Value: "123456789",
            },
        },
        Active: true,
        Type: []CodeableConcept{
            {
                Coding: []Coding{
                    {
                        System:  "http://terminology.hl7.org/CodeSystem/organization-type",
                        Code:    "prov",
                        Display: "Healthcare Provider",
                    },
                },
            },
        },
        Name: "Yangi tibbiyot muassasasi",
    }

    // Serializing to JSON
    jsonData, err := json.Marshal(org)
    if err != nil {
        panic(err)
    }

    // Sending POST request
    resp, err := http.Post(
        baseURL+"/Organization",
        "application/fhir+json",
        bytes.NewBuffer(jsonData),
    )
    if err != nil {
        panic(err)
    }
    defer resp.Body.Close()

    if resp.StatusCode == 201 {
        body, _ := io.ReadAll(resp.Body)
        var createdOrg Organization
        json.Unmarshal(body, &amp;createdOrg)
        fmt.Printf("Organization created with ID: %s\n", createdOrg.ID)
    } else {
        fmt.Printf("Error: %d\n", resp.StatusCode)
    }
}
</code></pre>
    </div>
  </div>
</div>
