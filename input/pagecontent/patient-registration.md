# Patient registration

## Overview

Goal: Create patient records with appropriate identifiers (PINFL), search and match patients, handle duplicates.

- Resources: Patient
- Skills: Search and matching, duplicate detection logic
- Base URL: `https://playground.dhp.uz/fhir`
  - **Note:** This is a temporary URL that will be replaced with the final one closer to the connectathon
- Profile: [uz-core-patient](https://dhp.uz/fhir/core/en/StructureDefinition-uz-core-patient.html)

**Feedback:** Share your experience, issues and successes in the [connectathon document](https://docs.google.com/document/d/1PdQ8zBI9xkISP3tAqIK8-TGMql3kVVZ4UNoHVYqCy4Y/edit?usp=sharing).

## uz-core-patient profile

**Note**: Validation is currently disabled on the server but is expected to be enabled for the connectathon. Client applications should follow the profile rules to ensure compatibility and data quality.

### Required elements

There are no mandatory elements with minimum cardinality greater than 0 in this profile. All elements are optional, though Must Support elements should be populated when data is available.

### Must-support elements

UZ Core profiles: Elements marked as Must Support must be populated when exchanging data between systems operating in Uzbekistan.

When data cannot be populated because it is unavailable in the source system, the element may be left empty - provided that cardinality rules allow it. However, when cardinality requirements mandate inclusion, systems must use the Data Absent Reason extension rather than leaving the element empty.

#### Profile elements

- **identifier**: Patient identifiers
  - **pinfl**: Personal identification number (PINFL) - national identifier (`system`: `https://dhp.uz/fhir/core/sid/pid/uz/ni`)
- **active**: Whether this patient record is in active use
- **name**: Patient name
  - **use**: Name use (official, usual, etc.)
  - **text**: Full name as displayed
  - **family**: Family/surname
  - **given**: Given names
  - **suffix**: Name suffix
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
- **address**: Patient addresses with two types:
  - **uzAddress**: Addresses in Uzbekistan (country code "UZ") with support for mahalla. **Must use coded values** from official registries for administrative divisions: [state](https://dhp.uz/fhir/core/en/ValueSet-state-vs.html), [district](https://dhp.uz/fhir/core/en/ValueSet-regions-vs.html), [city/mahalla](https://dhp.uz/fhir/core/en/ValueSet-mahalla-vs.html)
  - **i18nAddress**: International addresses (non-Uzbekistan). Administrative divisions use free text without required valuesets
- **maritalStatus**: Marital status (married, single, divorced, etc.)
- **multipleBirth[x]**: Whether patient is part of a multiple birth
- **photo**: Patient photo
- **contact**: Contact party (emergency contact, family member, etc.)
- **communication**: Languages for communication
  - **language**: Language code (uz, ru, kaa, etc.)
  - **preferred**: Preferred language for communication
- **generalPractitioner**: Patient's nominated primary care provider
- **managingOrganization**: Organization that is the custodian of the patient record
- **link**: Link to another Patient resource (for duplicate resolution)

### Gender differentiation

When a patient's gender is set to "other", the profile requires the `gender-other` extension:

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

For Uzbekistan addresses, coded values must be used from official registries:
- `state` field must use codes from the [state valueset](https://dhp.uz/fhir/core/en/ValueSet-state-vs.html)
- `district` field must use codes from the [regions valueset](https://dhp.uz/fhir/core/en/ValueSet-regions-vs.html)
- `city` field must use codes from the [mahalla valueset](https://dhp.uz/fhir/core/en/ValueSet-mahalla-vs.html)

```json
{
  "use": "home",
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

## CRUD operations

### Create Patient

- HTTP method: POST
- Endpoint: `/Patient`
- Headers: `Content-Type: application/fhir+json`

Creating a new patient. The server assigns a unique ID and returns a Location header.

Minimal example:
```json
{
  "resourceType": "Patient",
  "meta": {
    "profile": ["https://dhp.uz/fhir/core/StructureDefinition/uz-core-patient"]
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
      "system": "https://dhp.uz/fhir/core/sid/pid/uz/ni",
      "value": "12345678901234"
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
  "birthDate": "1985-05-15"
}
```

Response: HTTP 201 Created with Location header and created resource.

### Read Patient

- HTTP method: GET
- Endpoint: `/Patient/[id]`

Retrieving a specific patient by ID.

Response: HTTP 200 OK with Patient resource or HTTP 404 Not Found.

### Update Patient

- HTTP method: PUT
- Endpoint: `/Patient/[id]`
- Headers:
  - `Content-Type: application/fhir+json`
  - `If-Match: W/"[versionId]"` (required to prevent conflicts)

Full update of a patient. The entire resource must be sent, including the `id` element. The `If-Match` header is required and must contain the resource version from the `meta.versionId` element to prevent conflicts during concurrent editing (optimistic locking).

Request example:
```
PUT /Patient/existing-id
If-Match: W/"2"
Content-Type: application/fhir+json
```

Request body example:
```json
{
  "resourceType": "Patient",
  "id": "existing-id",
  "meta": {
    "profile": ["https://dhp.uz/fhir/core/StructureDefinition/uz-core-patient"]
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
  "birthDate": "1985-05-15"
}
```

Response: HTTP 200 OK with updated resource.

### Delete Patient

- HTTP method: DELETE
- Endpoint: `/Patient/[id]`

Deleting a patient.

Response: HTTP 200 OK with OperationOutcome on successful deletion. When attempting to read a deleted resource, the server will return HTTP 410 Gone.

## Search operations

- HTTP method: GET
- Endpoint: `/Patient?[parameters]`

All supported search parameters can be found in the capability statement at [DHPCapabilityStatement](https://dhp.uz/fhir/core/en/CapabilityStatement-DHPCapabilityStatement.html) or by querying the [/metadata](https://playground.dhp.uz/fhir/metadata) endpoint.

### Search parameters

| Parameter | Type | Description | Example |
|----------|-----|----------|--------|
| `_id` | token | Search by ID | `?_id=123` |
| `identifier` | token | Search by identifier | `?identifier=https://dhp.uz/fhir/core/sid/pid/uz/ni\|12345678901234` |
| `name` | string | Search by name (partial match) | `?name=Karimov` |
| `given` | string | Search by given name | `?given=Alisher` |
| `family` | string | Search by family name | `?family=Karimov` |
| `telecom` | token | Search by contact details | `?telecom=%2B998901234567` |
| `phone` | token | Search by phone number | `?phone=%2B998901234567` |
| `email` | token | Search by email | `?email=patient@example.com` |
| `address` | string | Search by address | `?address=Toshkent` |
| `address-city` | string | Search by city | `?address-city=Toshkent` |
| `address-country` | string | Search by country | `?address-country=UZ` |
| `address-postalcode` | string | Search by postal code | `?address-postalcode=100084` |
| `address-state` | string | Search by state/region | `?address-state=Toshkent` |
| `gender` | token | Search by gender | `?gender=male` |
| `birthdate` | date | Search by birth date | `?birthdate=1985-05-15` |
| `active` | token | Filter by status | `?active=true` |
| `deceased` | token | Filter by deceased status | `?deceased=false` |
| `organization` | reference | Search by managing organization | `?organization=Organization/123` |
| `general-practitioner` | reference | Search by GP | `?general-practitioner=Practitioner/456` |

### Common search patterns

**Find patient by PINFL:**
```
GET /Patient?identifier=https://dhp.uz/fhir/core/sid/pid/uz/ni|12345678901234
```

**Find patients by name:**
```
GET /Patient?name=Karimov
```

**Find patients by phone number:**
```
GET /Patient?phone=%2B998901234567
```

**Find patients by birth date:**
```
GET /Patient?birthdate=1985-05-15
```

**Find patients in a specific city:**
```
GET /Patient?address-city=Toshkent&active=true
```

**Combine multiple search criteria:**
```
GET /Patient?family=Karimov&birthdate=1985-05-15&gender=male
```

### Modifiers and prefixes

Combining parameters (logical AND):
```
GET /Patient?family=Karimov&address-city=Toshkent&active=true
```

Multiple values (logical OR):
```
GET /Patient?gender=male,female
```

Date comparisons:
```
GET /Patient?birthdate=gt1980-01-01&birthdate=lt1990-12-31
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
      "url": "https://playground.dhp.uz/fhir/Patient?name=Karimov&_page=1"
    },
    {
      "relation": "next",
      "url": "https://playground.dhp.uz/fhir/Patient?name=Karimov&_page=2"
    }
  ],
  "entry": [...]
}
```

Use `Bundle.link` with `relation="next"` to get the next page.

**Known issue**: The `Bundle.total` field may return `0` even when results are present. To count patients on the current page, filter `Bundle.entry` by `resourceType == "Patient"` (the response may contain `OperationOutcome` resources).

## Patient matching and duplicate detection

### Search before create

Before creating a new patient, search for potential matches to avoid duplicates:

1. **Search by PINFL** (strongest match):
   ```
   GET /Patient?identifier=https://dhp.uz/fhir/core/sid/pid/uz/ni|12345678901234
   ```

2. **Search by demographics** if PINFL not available:
   ```
   GET /Patient?family=Karimov&given=Alisher&birthdate=1985-05-15
   ```

3. **Search by phone number**:
   ```
   GET /Patient?phone=%2B998901234567
   ```

### Matching logic

Implement matching logic based on available data:

**Strong match criteria** (likely same patient):
- Same PINFL
- Same full name + birth date + gender
- Same phone number + birth date + gender

**Weak match criteria** (possible duplicate - needs review):
- Similar name (fuzzy match) + same birth date
- Same phone number + similar birth date
- Same address + similar name

### Handling duplicates with Patient.link

When duplicates are identified, use the `link` element to connect patient resources:

```json
{
  "resourceType": "Patient",
  "id": "patient-main",
  "identifier": [...],
  "name": [...],
  "link": [
    {
      "other": {
        "reference": "Patient/patient-duplicate",
        "display": "Duplicate record"
      },
      "type": "replaced-by"
    }
  ]
}
```

Link types:
- **replaced-by**: This record is replaced by the linked record
- **replaces**: This record replaces the linked record
- **refer**: This record should be consulted with the linked record
- **seealso**: This record is possibly the same patient as the linked record

### Duplicate resolution workflow

1. **Identify potential duplicates** through search
2. **Review matches** manually or with business rules
3. **Choose master record** (usually the one with most complete data or earliest creation date)
4. **Update duplicate records**:
   - Set `active: false` on duplicate
   - Add `link` element pointing to master record with type "replaced-by"
5. **Optionally merge data** from duplicate into master before deactivating

Example of marking a duplicate:
```json
{
  "resourceType": "Patient",
  "id": "patient-duplicate",
  "active": false,
  "identifier": [...],
  "name": [...],
  "link": [
    {
      "other": {
        "reference": "Patient/patient-main",
        "display": "Main patient record"
      },
      "type": "replaced-by"
    }
  ]
}
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
      "diagnostics": "Patient.identifier: minimum required = 1, but only found 0"
    }
  ]
}
```

## Useful links

- [FHIR Patient Resource](http://hl7.org/fhir/R5/patient.html)
- [uz-core-patient Profile](https://dhp.uz/fhir/core/en/StructureDefinition-uz-core-patient.html)
- [FHIR RESTful API](http://hl7.org/fhir/R5/http.html)
- [FHIR Search](http://hl7.org/fhir/R5/search.html)
- [Patient Matching](http://hl7.org/fhir/R5/patient.html#matching)

---

## Code examples

{% include code-tabs-style.html %}

Below are examples of creating and searching for patients in various programming languages:

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
<pre><code class="language-bash"># Search for existing patient by PINFL before creating
curl "https://playground.dhp.uz/fhir/Patient?identifier=https://dhp.uz/fhir/core/sid/pid/uz/ni|12345678901234"

# If not found, create new patient
curl -X POST "https://playground.dhp.uz/fhir/Patient" \
  -H "Content-Type: application/fhir+json" \
  -d '{
  "resourceType": "Patient",
  "meta": {
    "profile": ["https://dhp.uz/fhir/core/StructureDefinition/uz-core-patient"]
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
      "system": "https://dhp.uz/fhir/core/sid/pid/uz/ni",
      "value": "12345678901234"
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
  "birthDate": "1985-05-15",
  "telecom": [
    {
      "system": "phone",
      "value": "+998901234567",
      "use": "mobile"
    }
  ]
}'
</code></pre>
    </div>
    <div class="tab-pane" id="python">
<pre><code class="language-python">import requests
from fhir.resources.patient import Patient
from fhir.resources.identifier import Identifier
from fhir.resources.humanname import HumanName
from fhir.resources.contactpoint import ContactPoint
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.meta import Meta

# FHIR server base URL
base_url = "https://playground.dhp.uz/fhir"
pinfl = "12345678901234"

# Search for existing patient by PINFL
search_url = f"{base_url}/Patient?identifier=https://dhp.uz/fhir/core/sid/pid/uz/ni|{pinfl}"
response = requests.get(search_url)

if response.status_code == 200:
    bundle = response.json()
    if bundle.get('total', 0) > 0:
        print(f"Patient found with PINFL {pinfl}")
        existing_patient = bundle['entry'][0]['resource']
        print(f"Patient ID: {existing_patient['id']}")
    else:
        print("Patient not found, creating new patient")

        # Create new patient
        patient = Patient(
            meta=Meta(
                profile=["https://dhp.uz/fhir/core/StructureDefinition/uz-core-patient"]
            ),
            language="uz",
            identifier=[
                Identifier(
                    use="official",
                    system="https://dhp.uz/fhir/core/sid/pid/uz/ni",
                    type=CodeableConcept(
                        coding=[
                            Coding(
                                system="http://terminology.hl7.org/CodeSystem/v2-0203",
                                code="NI"
                            )
                        ]
                    ),
                    value=pinfl
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
            birthDate="1985-05-15",
            telecom=[
                ContactPoint(
                    system="phone",
                    value="+998901234567",
                    use="mobile"
                )
            ]
        )

        # Send POST request
        create_response = requests.post(
            f"{base_url}/Patient",
            headers={"Content-Type": "application/fhir+json"},
            data=patient.json()
        )

        if create_response.status_code == 201:
            created_patient = create_response.json()
            print(f"Patient created with ID: {created_patient['id']}")
        else:
            print(f"Error: {create_response.status_code}")
            print(create_response.text)
</code></pre>
    </div>
    <div class="tab-pane" id="javascript">
<pre><code class="language-javascript">// Using fetch API
const baseUrl = "https://playground.dhp.uz/fhir";
const pinfl = "12345678901234";

// Search for existing patient by PINFL
async function findOrCreatePatient() {
  try {
    // Search for patient
    const searchUrl = `${baseUrl}/Patient?identifier=https://dhp.uz/fhir/core/sid/pid/uz/ni|${pinfl}`;
    const searchResponse = await fetch(searchUrl);
    const bundle = await searchResponse.json();

    if (bundle.total && bundle.total > 0) {
      console.log(`Patient found with PINFL ${pinfl}`);
      console.log(`Patient ID: ${bundle.entry[0].resource.id}`);
      return bundle.entry[0].resource;
    }

    console.log("Patient not found, creating new patient");

    // Create new patient
    const patient = {
      resourceType: "Patient",
      meta: {
        profile: ["https://dhp.uz/fhir/core/StructureDefinition/uz-core-patient"]
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
          system: "https://dhp.uz/fhir/core/sid/pid/uz/ni",
          value: pinfl
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
      birthDate: "1985-05-15",
      telecom: [
        {
          system: "phone",
          value: "+998901234567",
          use: "mobile"
        }
      ]
    };

    const createResponse = await fetch(`${baseUrl}/Patient`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/fhir+json'
      },
      body: JSON.stringify(patient)
    });

    if (createResponse.status === 201) {
      const data = await createResponse.json();
      console.log(`Patient created with ID: ${data.id}`);
      return data;
    } else {
      throw new Error(`Error: ${createResponse.status}`);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

findOrCreatePatient();
</code></pre>
    </div>
    <div class="tab-pane" id="java">
<pre><code class="language-java">import ca.uhn.fhir.context.FhirContext;
import ca.uhn.fhir.rest.client.api.IGenericClient;
import ca.uhn.fhir.rest.gclient.TokenClientParam;
import org.hl7.fhir.r5.model.*;

// Creating FHIR context and client
FhirContext ctx = FhirContext.forR5();
IGenericClient client = ctx.newRestfulGenericClient("https://playground.dhp.uz/fhir");

String pinfl = "12345678901234";
String system = "https://dhp.uz/fhir/core/sid/pid/uz/ni";

// Search for existing patient by PINFL
Bundle results = client.search()
    .forResource(Patient.class)
    .where(new TokenClientParam("identifier")
        .exactly()
        .systemAndCode(system, pinfl))
    .returnBundle(Bundle.class)
    .execute();

if (results.hasEntry()) {
    Patient existingPatient = (Patient) results.getEntry().get(0).getResource();
    System.out.println("Patient found with ID: " + existingPatient.getIdElement().getIdPart());
} else {
    System.out.println("Patient not found, creating new patient");

    // Create new patient
    Patient patient = new Patient();

    // Setting profile
    patient.getMeta()
        .addProfile("https://dhp.uz/fhir/core/StructureDefinition/uz-core-patient");

    // Setting language
    patient.setLanguage("uz");

    // Adding PINFL identifier
    Identifier identifier = patient.addIdentifier();
    identifier.setUse(Identifier.IdentifierUse.OFFICIAL);
    identifier.setSystem(system);
    identifier.setValue(pinfl);
    CodeableConcept idType = new CodeableConcept();
    idType.addCoding()
        .setSystem("http://terminology.hl7.org/CodeSystem/v2-0203")
        .setCode("NI");
    identifier.setType(idType);

    // Setting status
    patient.setActive(true);

    // Adding name
    HumanName name = patient.addName();
    name.setUse(HumanName.NameUse.OFFICIAL);
    name.setFamily("Karimov");
    name.addGiven("Alisher");
    name.addGiven("Akbarovich");

    // Setting gender and birth date
    patient.setGender(Enumerations.AdministrativeGender.MALE);
    patient.setBirthDate(new java.text.SimpleDateFormat("yyyy-MM-dd").parse("1985-05-15"));

    // Adding phone
    ContactPoint phone = patient.addTelecom();
    phone.setSystem(ContactPoint.ContactPointSystem.PHONE);
    phone.setValue("+998901234567");
    phone.setUse(ContactPoint.ContactPointUse.MOBILE);

    // Creating on server
    MethodOutcome outcome = client.create()
        .resource(patient)
        .execute();

    IdType id = (IdType) outcome.getId();
    System.out.println("Patient created with ID: " + id.getIdPart());
}
</code></pre>
    </div>
    <div class="tab-pane" id="csharp">
<pre><code class="language-csharp">using Hl7.Fhir.Model;
using Hl7.Fhir.Rest;
using System;
using System.Linq;

// Creating FHIR client
var client = new FhirClient("https://playground.dhp.uz/fhir");

string pinfl = "12345678901234";
string system = "https://dhp.uz/fhir/core/sid/pid/uz/ni";

// Search for existing patient by PINFL
var query = new SearchParams()
    .Where($"identifier={system}|{pinfl}");
var results = client.Search&lt;Patient&gt;(query);

if (results.Entry.Any())
{
    var existingPatient = (Patient)results.Entry.First().Resource;
    Console.WriteLine($"Patient found with ID: {existingPatient.Id}");
}
else
{
    Console.WriteLine("Patient not found, creating new patient");

    // Create new patient
    var patient = new Patient
    {
        Meta = new Meta
        {
            Profile = new[] { "https://dhp.uz/fhir/core/StructureDefinition/uz-core-patient" }
        },
        Language = "uz",
        Identifier = new List&lt;Identifier&gt;
        {
            new Identifier
            {
                Use = Identifier.IdentifierUse.Official,
                System = system,
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
                Value = pinfl
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
        BirthDate = "1985-05-15",
        Telecom = new List&lt;ContactPoint&gt;
        {
            new ContactPoint
            {
                System = ContactPoint.ContactPointSystem.Phone,
                Value = "+998901234567",
                Use = ContactPoint.ContactPointUse.Mobile
            }
        }
    };

    // Creating on server
    var createdPatient = client.Create(patient);
    Console.WriteLine($"Patient created with ID: {createdPatient.Id}");
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

type Patient struct {
    ResourceType string        `json:"resourceType"`
    ID           string        `json:"id,omitempty"`
    Meta         *Meta         `json:"meta,omitempty"`
    Language     string        `json:"language,omitempty"`
    Identifier   []Identifier  `json:"identifier,omitempty"`
    Active       bool          `json:"active"`
    Name         []HumanName   `json:"name,omitempty"`
    Gender       string        `json:"gender,omitempty"`
    BirthDate    string        `json:"birthDate,omitempty"`
    Telecom      []ContactPoint `json:"telecom,omitempty"`
}

type Bundle struct {
    ResourceType string        `json:"resourceType"`
    Total        int           `json:"total"`
    Entry        []BundleEntry `json:"entry,omitempty"`
}

type BundleEntry struct {
    Resource Patient `json:"resource"`
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

type ContactPoint struct {
    System string `json:"system"`
    Value  string `json:"value"`
    Use    string `json:"use,omitempty"`
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
    pinfl := "12345678901234"
    system := "https://dhp.uz/fhir/core/sid/pid/uz/ni"

    // Search for existing patient
    searchURL := fmt.Sprintf("%s/Patient?identifier=%s|%s",
        baseURL,
        url.QueryEscape(system),
        pinfl)

    resp, err := http.Get(searchURL)
    if err != nil {
        panic(err)
    }
    defer resp.Body.Close()

    body, _ := io.ReadAll(resp.Body)
    var bundle Bundle
    json.Unmarshal(body, &bundle)

    if bundle.Total > 0 {
        fmt.Printf("Patient found with ID: %s\n", bundle.Entry[0].Resource.ID)
        return
    }

    fmt.Println("Patient not found, creating new patient")

    // Create new patient
    patient := Patient{
        ResourceType: "Patient",
        Meta: &Meta{
            Profile: []string{"https://dhp.uz/fhir/core/StructureDefinition/uz-core-patient"},
        },
        Language: "uz",
        Identifier: []Identifier{
            {
                Use:    "official",
                System: system,
                Type: &CodeableConcept{
                    Coding: []Coding{
                        {
                            System: "http://terminology.hl7.org/CodeSystem/v2-0203",
                            Code:   "NI",
                        },
                    },
                },
                Value: pinfl,
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
        Gender:    "male",
        BirthDate: "1985-05-15",
        Telecom: []ContactPoint{
            {
                System: "phone",
                Value:  "+998901234567",
                Use:    "mobile",
            },
        },
    }

    // Serialize to JSON
    jsonData, err := json.Marshal(patient)
    if err != nil {
        panic(err)
    }

    // Send POST request
    createResp, err := http.Post(
        baseURL+"/Patient",
        "application/fhir+json",
        bytes.NewBuffer(jsonData),
    )
    if err != nil {
        panic(err)
    }
    defer createResp.Body.Close()

    if createResp.StatusCode == 201 {
        body, _ := io.ReadAll(createResp.Body)
        var createdPatient Patient
        json.Unmarshal(body, &createdPatient)
        fmt.Printf("Patient created with ID: %s\n", createdPatient.ID)
    } else {
        fmt.Printf("Error: %d\n", createResp.StatusCode)
    }
}
</code></pre>
    </div>
  </div>
</div>
