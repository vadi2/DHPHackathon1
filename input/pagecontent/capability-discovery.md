# Discovering server capabilities

## Overview

Goal: Learn how to retrieve and use the CapabilityStatement to understand what resources and operations are available on the server, enabling your application to adapt dynamically.

- Resources: CapabilityStatement
- Skills: GET requests, JSON navigation
- Base URL: `https://playground.dhp.uz/fhir`
  - **Note:** This is a temporary URL that will be replaced with the final one closer to the connectathon
- Useful links:
  - [FHIR CapabilityStatement](http://hl7.org/fhir/R5/capabilitystatement.html)
  - [DHPCapabilityStatement](https://dhp.uz/fhir/core/en/CapabilityStatement-DHPCapabilityStatement.html)

**Feedback:** Share your experience, issues and successes in the [connectathon document](https://docs.google.com/document/d/1PdQ8zBI9xkISP3tAqIK8-TGMql3kVVZ4UNoHVYqCy4Y/edit?usp=sharing).

## What is a CapabilityStatement?

A CapabilityStatement describes what a FHIR server can do. It tells you:
- Which FHIR resources are supported (Patient, Practitioner, ValueSet, etc.)
- What operations you can perform (read, search, create, update, delete)
- Which search parameters are available
- Which operations are supported ($expand, $validate-code, etc.)

This is essential for building adaptive applications that work with different FHIR servers.

## Retrieving the CapabilityStatement

### Basic request

- HTTP method: GET
- Endpoint: `/metadata`

Example:
```
GET /metadata
```

This returns the server's CapabilityStatement in JSON format.

### Key elements in the response

**1. Server information:**
```json
{
  "resourceType": "CapabilityStatement",
  "status": "active",
  "date": "2025-11-10T11:23:12+05:00",
  "kind": "instance",
  "fhirVersion": "5.0.0",
  "implementation": {
    "description": "FHIR R5 Server",
    "url": "https://playground.dhp.uz/fhir"
  }
}
```

**2. Supported resources:**
```json
{
  "rest": [
    {
      "mode": "server",
      "resource": [
        {
          "type": "ValueSet",
          "profile": "http://hl7.org/fhir/StructureDefinition/ValueSet",
          "interaction": [
            { "code": "read" },
            { "code": "search-type" }
          ]
        }
      ]
    }
  ]
}
```

**3. Supported operations:**
```json
{
  "resource": [
    {
      "type": "ValueSet",
      "operation": [
        {
          "name": "expand",
          "definition": "http://hl7.org/fhir/OperationDefinition/ValueSet-expand"
        },
        {
          "name": "validate-code",
          "definition": "http://hl7.org/fhir/OperationDefinition/ValueSet-validate-code"
        }
      ]
    }
  ]
}
```

## Using the CapabilityStatement

### Check if a resource is supported

Before using a resource, check if it's supported:

```javascript
function isResourceSupported(capability, resourceType) {
  const rest = capability.rest.find(r => r.mode === 'server');
  return rest.resource.some(r => r.type === resourceType);
}

// Usage
if (isResourceSupported(capability, 'ValueSet')) {
  // You can use ValueSet resources
}
```

### Check if an operation is supported

Before calling an operation, verify it's available:

```javascript
function isOperationSupported(capability, resourceType, operationName) {
  const rest = capability.rest.find(r => r.mode === 'server');
  const resource = rest.resource.find(r => r.type === resourceType);

  if (!resource || !resource.operation) return false;

  return resource.operation.some(op => op.name === operationName);
}

// Usage
if (isOperationSupported(capability, 'ValueSet', 'expand')) {
  // You can use $expand operation
}
```

### Get available search parameters

Find out which search parameters you can use:

```javascript
function getSearchParams(capability, resourceType) {
  const rest = capability.rest.find(r => r.mode === 'server');
  const resource = rest.resource.find(r => r.type === resourceType);

  if (!resource || !resource.searchParam) return [];

  return resource.searchParam.map(sp => sp.name);
}

// Usage
const params = getSearchParams(capability, 'ValueSet');
console.log('Available search params:', params);
// Output: ['url', 'name', 'status', 'version', ...]
```

## Practical example

Here's a complete example of fetching and using the CapabilityStatement:

```javascript
async function checkServerCapabilities() {
  // Fetch CapabilityStatement
  const response = await fetch('https://playground.dhp.uz/fhir/metadata');
  const capability = await response.json();

  console.log('Server:', capability.implementation?.description || 'Unknown');
  console.log('FHIR Version:', capability.fhirVersion);

  // Check terminology support
  const hasValueSet = isResourceSupported(capability, 'ValueSet');
  const hasExpand = isOperationSupported(capability, 'ValueSet', 'expand');
  const hasValidate = isOperationSupported(capability, 'ValueSet', 'validate-code');

  console.log('ValueSet resource:', hasValueSet ? '✓' : '✗');
  console.log('$expand operation:', hasExpand ? '✓' : '✗');
  console.log('$validate-code operation:', hasValidate ? '✓' : '✗');

  // Enable/disable features in your app
  if (hasExpand) {
    enableValueSetExpansion();
  }

  if (hasValidate) {
    enableCodeValidation();
  }
}
```

## Best practices

1. **Cache the CapabilityStatement**: The capabilities don't change often. Cache the response and refresh periodically.

2. **Graceful degradation**: If an operation isn't supported, provide alternative functionality or clear error messages.

3. **Check on startup**: Retrieve the CapabilityStatement when your application starts to configure available features.

4. **Version awareness**: Check the `fhirVersion` field to ensure compatibility with your application.

---

## Code examples

{% include code-tabs-style.html %}

Below are examples of fetching and using the CapabilityStatement in various programming languages:

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
<pre><code class="language-bash"># Fetch CapabilityStatement
curl "https://playground.dhp.uz/fhir/metadata" \
  -H "Accept: application/fhir+json"

# You can pipe to jq to extract specific information
curl -s "https://playground.dhp.uz/fhir/metadata" | jq '.fhirVersion'

# Check if ValueSet resource is supported
curl -s "https://playground.dhp.uz/fhir/metadata" | \
  jq '.rest[].resource[] | select(.type=="ValueSet") | .type'

# Get all operations for ValueSet
curl -s "https://playground.dhp.uz/fhir/metadata" | \
  jq '.rest[].resource[] | select(.type=="ValueSet") | .operation[].name'
</code></pre>
    </div>
    <div class="tab-pane" id="python">
<pre><code class="language-python">import requests
from typing import List, Dict, Optional

base_url = "https://playground.dhp.uz/fhir"

def get_capability_statement() -> Dict:
    """Fetch the server's CapabilityStatement."""
    response = requests.get(
        f"{base_url}/metadata",
        headers={"Accept": "application/fhir+json"}
    )
    response.raise_for_status()
    return response.json()

def is_resource_supported(capability: Dict, resource_type: str) -> bool:
    """Check if a resource type is supported."""
    for rest in capability.get("rest", []):
        if rest.get("mode") == "server":
            for resource in rest.get("resource", []):
                if resource.get("type") == resource_type:
                    return True
    return False

def is_operation_supported(capability: Dict, resource_type: str,
                          operation_name: str) -> bool:
    """Check if an operation is supported for a resource."""
    for rest in capability.get("rest", []):
        if rest.get("mode") == "server":
            for resource in rest.get("resource", []):
                if resource.get("type") == resource_type:
                    operations = resource.get("operation", [])
                    return any(op.get("name") == operation_name
                             for op in operations)
    return False

def get_search_parameters(capability: Dict, resource_type: str) -> List[str]:
    """Get available search parameters for a resource."""
    for rest in capability.get("rest", []):
        if rest.get("mode") == "server":
            for resource in rest.get("resource", []):
                if resource.get("type") == resource_type:
                    return [sp.get("name")
                           for sp in resource.get("searchParam", [])]
    return []

# Example usage
capability = get_capability_statement()

print(f"Server: {capability.get('implementation', {}).get('description', 'Unknown')}")
print(f"FHIR Version: {capability.get('fhirVersion')}")
print()

# Check resource support
print("Resource Support:")
print(f"  ValueSet: {is_resource_supported(capability, 'ValueSet')}")
print(f"  CodeSystem: {is_resource_supported(capability, 'CodeSystem')}")
print(f"  ConceptMap: {is_resource_supported(capability, 'ConceptMap')}")
print()

# Check operation support
print("ValueSet Operations:")
print(f"  $expand: {is_operation_supported(capability, 'ValueSet', 'expand')}")
print(f"  $validate-code: {is_operation_supported(capability, 'ValueSet', 'validate-code')}")
print()

# Get search parameters
params = get_search_parameters(capability, 'ValueSet')
print(f"ValueSet search parameters: {', '.join(params[:5])}...")
</code></pre>
    </div>
    <div class="tab-pane" id="javascript">
<pre><code class="language-javascript">const baseUrl = 'https://playground.dhp.uz/fhir';

async function getCapabilityStatement() {
  const response = await fetch(`${baseUrl}/metadata`, {
    headers: { 'Accept': 'application/fhir+json' }
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return await response.json();
}

function isResourceSupported(capability, resourceType) {
  const rest = capability.rest?.find(r => r.mode === 'server');
  return rest?.resource?.some(r => r.type === resourceType) || false;
}

function isOperationSupported(capability, resourceType, operationName) {
  const rest = capability.rest?.find(r => r.mode === 'server');
  const resource = rest?.resource?.find(r => r.type === resourceType);

  if (!resource?.operation) return false;

  return resource.operation.some(op => op.name === operationName);
}

function getSearchParameters(capability, resourceType) {
  const rest = capability.rest?.find(r => r.mode === 'server');
  const resource = rest?.resource?.find(r => r.type === resourceType);

  return resource?.searchParam?.map(sp => sp.name) || [];
}

// Example usage
(async () => {
  try {
    const capability = await getCapabilityStatement();

    console.log('Server:', capability.implementation?.description || 'Unknown');
    console.log('FHIR Version:', capability.fhirVersion);
    console.log('');

    // Check resource support
    console.log('Resource Support:');
    console.log('  ValueSet:', isResourceSupported(capability, 'ValueSet'));
    console.log('  CodeSystem:', isResourceSupported(capability, 'CodeSystem'));
    console.log('  ConceptMap:', isResourceSupported(capability, 'ConceptMap'));
    console.log('');

    // Check operation support
    console.log('ValueSet Operations:');
    console.log('  $expand:', isOperationSupported(capability, 'ValueSet', 'expand'));
    console.log('  $validate-code:', isOperationSupported(capability, 'ValueSet', 'validate-code'));
    console.log('');

    // Get search parameters
    const params = getSearchParameters(capability, 'ValueSet');
    console.log('ValueSet search parameters:', params.slice(0, 5).join(', ') + '...');

  } catch (error) {
    console.error('Error:', error.message);
  }
})();
</code></pre>
    </div>
    <div class="tab-pane" id="java">
<pre><code class="language-java">import org.hl7.fhir.r5.model.CapabilityStatement;
import org.hl7.fhir.r5.model.CapabilityStatement.CapabilityStatementRestComponent;
import org.hl7.fhir.r5.model.CapabilityStatement.CapabilityStatementRestResourceComponent;
import org.hl7.fhir.r5.model.CapabilityStatement.ResourceInteractionComponent;
import ca.uhn.fhir.context.FhirContext;
import ca.uhn.fhir.rest.client.api.IGenericClient;

import java.util.ArrayList;
import java.util.List;

public class CapabilityExample {
    private static final String BASE_URL = "https://playground.dhp.uz/fhir";
    private static FhirContext ctx = FhirContext.forR5();
    private static IGenericClient client = ctx.newRestfulGenericClient(BASE_URL);

    public static CapabilityStatement getCapabilityStatement() {
        return client.capabilities().ofType(CapabilityStatement.class).execute();
    }

    public static boolean isResourceSupported(CapabilityStatement capability, String resourceType) {
        for (CapabilityStatementRestComponent rest : capability.getRest()) {
            if (rest.getMode().toCode().equals("server")) {
                for (CapabilityStatementRestResourceComponent resource : rest.getResource()) {
                    if (resource.getType().equals(resourceType)) {
                        return true;
                    }
                }
            }
        }
        return false;
    }

    public static boolean isOperationSupported(CapabilityStatement capability,
                                              String resourceType,
                                              String operationName) {
        for (CapabilityStatementRestComponent rest : capability.getRest()) {
            if (rest.getMode().toCode().equals("server")) {
                for (CapabilityStatementRestResourceComponent resource : rest.getResource()) {
                    if (resource.getType().equals(resourceType)) {
                        return resource.getOperation().stream()
                            .anyMatch(op -> op.getName().equals(operationName));
                    }
                }
            }
        }
        return false;
    }

    public static List&lt;String&gt; getSearchParameters(CapabilityStatement capability, String resourceType) {
        List&lt;String&gt; params = new ArrayList&lt;&gt;();
        for (CapabilityStatementRestComponent rest : capability.getRest()) {
            if (rest.getMode().toCode().equals("server")) {
                for (CapabilityStatementRestResourceComponent resource : rest.getResource()) {
                    if (resource.getType().equals(resourceType)) {
                        resource.getSearchParam().forEach(sp -> params.add(sp.getName()));
                        return params;
                    }
                }
            }
        }
        return params;
    }

    public static void main(String[] args) {
        CapabilityStatement capability = getCapabilityStatement();

        String serverDesc = capability.hasImplementation() ?
            capability.getImplementation().getDescription() : "Unknown";
        System.out.println("Server: " + serverDesc);
        System.out.println("FHIR Version: " + capability.getFhirVersion().toCode());
        System.out.println();

        // Check resource support
        System.out.println("Resource Support:");
        System.out.println("  ValueSet: " + isResourceSupported(capability, "ValueSet"));
        System.out.println("  CodeSystem: " + isResourceSupported(capability, "CodeSystem"));
        System.out.println("  ConceptMap: " + isResourceSupported(capability, "ConceptMap"));
        System.out.println();

        // Check operation support
        System.out.println("ValueSet Operations:");
        System.out.println("  $expand: " + isOperationSupported(capability, "ValueSet", "expand"));
        System.out.println("  $validate-code: " +
            isOperationSupported(capability, "ValueSet", "validate-code"));
        System.out.println();

        // Get search parameters
        List&lt;String&gt; params = getSearchParameters(capability, "ValueSet");
        System.out.println("ValueSet search parameters: " +
            String.join(", ", params.subList(0, Math.min(5, params.size()))) + "...");
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

class CapabilityExample
{
    private const string BaseUrl = "https://playground.dhp.uz/fhir";
    private static FhirClient client = new FhirClient(BaseUrl);

    static CapabilityStatement GetCapabilityStatement()
    {
        return client.CapabilityStatement();
    }

    static bool IsResourceSupported(CapabilityStatement capability, string resourceType)
    {
        var rest = capability.Rest.FirstOrDefault(r => r.Mode == CapabilityStatement.RestfulCapabilityMode.Server);
        if (rest == null) return false;

        return rest.Resource.Any(r => r.Type.ToString() == resourceType);
    }

    static bool IsOperationSupported(CapabilityStatement capability, string resourceType, string operationName)
    {
        var rest = capability.Rest.FirstOrDefault(r => r.Mode == CapabilityStatement.RestfulCapabilityMode.Server);
        if (rest == null) return false;

        var resource = rest.Resource.FirstOrDefault(r => r.Type.ToString() == resourceType);
        if (resource == null) return false;

        return resource.Operation.Any(op => op.Name == operationName);
    }

    static List&lt;string&gt; GetSearchParameters(CapabilityStatement capability, string resourceType)
    {
        var rest = capability.Rest.FirstOrDefault(r => r.Mode == CapabilityStatement.RestfulCapabilityMode.Server);
        if (rest == null) return new List&lt;string&gt;();

        var resource = rest.Resource.FirstOrDefault(r => r.Type.ToString() == resourceType);
        if (resource == null) return new List&lt;string&gt;();

        return resource.SearchParam.Select(sp => sp.Name).ToList();
    }

    static void Main(string[] args)
    {
        var capability = GetCapabilityStatement();

        var serverDesc = capability.Implementation?.Description ?? "Unknown";
        Console.WriteLine($"Server: {serverDesc}");
        Console.WriteLine($"FHIR Version: {capability.FhirVersion}");
        Console.WriteLine();

        // Check resource support
        Console.WriteLine("Resource Support:");
        Console.WriteLine($"  ValueSet: {IsResourceSupported(capability, "ValueSet")}");
        Console.WriteLine($"  CodeSystem: {IsResourceSupported(capability, "CodeSystem")}");
        Console.WriteLine($"  ConceptMap: {IsResourceSupported(capability, "ConceptMap")}");
        Console.WriteLine();

        // Check operation support
        Console.WriteLine("ValueSet Operations:");
        Console.WriteLine($"  $expand: {IsOperationSupported(capability, "ValueSet", "expand")}");
        Console.WriteLine($"  $validate-code: {IsOperationSupported(capability, "ValueSet", "validate-code")}");
        Console.WriteLine();

        // Get search parameters
        var params = GetSearchParameters(capability, "ValueSet");
        Console.WriteLine($"ValueSet search parameters: {string.Join(", ", params.Take(5))}...");
    }
}
</code></pre>
    </div>
    <div class="tab-pane" id="go">
<pre><code class="language-go">package main

import (
    "encoding/json"
    "fmt"
    "io"
    "net/http"
)

const baseURL = "https://playground.dhp.uz/fhir"

type CapabilityStatement struct {
    FhirVersion    string `json:"fhirVersion"`
    Implementation struct {
        Description string `json:"description"`
        URL         string `json:"url"`
    } `json:"implementation"`
    Rest []struct {
        Mode     string `json:"mode"`
        Resource []struct {
            Type        string `json:"type"`
            Operation   []struct {
                Name string `json:"name"`
            } `json:"operation"`
            SearchParam []struct {
                Name string `json:"name"`
            } `json:"searchParam"`
        } `json:"resource"`
    } `json:"rest"`
}

func getCapabilityStatement() (*CapabilityStatement, error) {
    resp, err := http.Get(baseURL + "/metadata")
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    body, err := io.ReadAll(resp.Body)
    if err != nil {
        return nil, err
    }

    var capability CapabilityStatement
    if err := json.Unmarshal(body, &capability); err != nil {
        return nil, err
    }

    return &capability, nil
}

func isResourceSupported(capability *CapabilityStatement, resourceType string) bool {
    for _, rest := range capability.Rest {
        if rest.Mode == "server" {
            for _, resource := range rest.Resource {
                if resource.Type == resourceType {
                    return true
                }
            }
        }
    }
    return false
}

func isOperationSupported(capability *CapabilityStatement, resourceType, operationName string) bool {
    for _, rest := range capability.Rest {
        if rest.Mode == "server" {
            for _, resource := range rest.Resource {
                if resource.Type == resourceType {
                    for _, op := range resource.Operation {
                        if op.Name == operationName {
                            return true
                        }
                    }
                }
            }
        }
    }
    return false
}

func getSearchParameters(capability *CapabilityStatement, resourceType string) []string {
    for _, rest := range capability.Rest {
        if rest.Mode == "server" {
            for _, resource := range rest.Resource {
                if resource.Type == resourceType {
                    params := make([]string, len(resource.SearchParam))
                    for i, sp := range resource.SearchParam {
                        params[i] = sp.Name
                    }
                    return params
                }
            }
        }
    }
    return []string{}
}

func main() {
    capability, err := getCapabilityStatement()
    if err != nil {
        fmt.Printf("Error: %v\n", err)
        return
    }

    fmt.Printf("Server: %s\n", capability.Implementation.Description)
    fmt.Printf("FHIR Version: %s\n\n", capability.FhirVersion)

    // Check resource support
    fmt.Println("Resource Support:")
    fmt.Printf("  ValueSet: %v\n", isResourceSupported(capability, "ValueSet"))
    fmt.Printf("  CodeSystem: %v\n", isResourceSupported(capability, "CodeSystem"))
    fmt.Printf("  ConceptMap: %v\n\n", isResourceSupported(capability, "ConceptMap"))

    // Check operation support
    fmt.Println("ValueSet Operations:")
    fmt.Printf("  $expand: %v\n", isOperationSupported(capability, "ValueSet", "expand"))
    fmt.Printf("  $validate-code: %v\n\n", isOperationSupported(capability, "ValueSet", "validate-code"))

    // Get search parameters
    params := getSearchParameters(capability, "ValueSet")
    if len(params) > 5 {
        fmt.Printf("ValueSet search parameters: %s...\n", params[:5])
    } else {
        fmt.Printf("ValueSet search parameters: %s\n", params)
    }
}
</code></pre>
    </div>
  </div>
</div>

---

## Exercise

**Task:** Retrieve the CapabilityStatement from the playground server and answer these questions:

1. What FHIR version does the server support?
2. Which terminology resources are supported? (CodeSystem, ValueSet, ConceptMap)
3. Which operations are available for ValueSet?
4. Can you search ValueSets by name?

```
GET https://playground.dhp.uz/fhir/metadata
```

Explore the response and write code to programmatically check these capabilities.
