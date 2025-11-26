# Обнаружение возможностей сервера

## Обзор

Цель: Научиться получать и использовать CapabilityStatement для понимания того, какие ресурсы и операции доступны на сервере, позволяя вашему приложению динамически адаптироваться.

- Ресурсы: CapabilityStatement
- Навыки: GET-запросы, навигация по JSON
- Базовый URL: `https://playground.dhp.uz/fhir`
- Полезные ссылки:
  - [FHIR CapabilityStatement](http://hl7.org/fhir/R5/capabilitystatement.html)
  - [DHPCapabilityStatement](https://dhp.uz/fhir/core/en/CapabilityStatement-DHPCapabilityStatement.html)

**Обратная связь:** Поделитесь своим опытом, проблемами и успехами в [документе коннектафона](https://docs.google.com/document/d/1PdQ8zBI9xkISP3tAqIK8-TGMql3kVVZ4UNoHVYqCy4Y/edit?usp=sharing).

## Что такое CapabilityStatement?

CapabilityStatement описывает, что может делать FHIR-сервер. Он сообщает вам:
- Какие ресурсы FHIR поддерживаются (Patient, Practitioner, ValueSet и т.д.)
- Какие операции вы можете выполнять (read, search, create, update, delete)
- Какие параметры поиска доступны
- Какие операции поддерживаются ($expand, $validate-code и т.д.)

Это необходимо для создания адаптивных приложений, которые работают с различными FHIR-серверами.

## Получение CapabilityStatement

### Базовый запрос

- HTTP метод: GET
- Endpoint: `/metadata`

Пример:
```
GET /metadata
```

Это возвращает CapabilityStatement сервера в формате JSON.

### Ключевые элементы в ответе

**1. Информация о сервере:**
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

**2. Поддерживаемые ресурсы:**
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

**3. Поддерживаемые операции:**
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

## Использование CapabilityStatement

### Проверить, поддерживается ли ресурс

Перед использованием ресурса проверьте, поддерживается ли он:

```javascript
function isResourceSupported(capability, resourceType) {
  const rest = capability.rest.find(r => r.mode === 'server');
  return rest.resource.some(r => r.type === resourceType);
}

// Использование
if (isResourceSupported(capability, 'ValueSet')) {
  // Вы можете использовать ресурсы ValueSet
}
```

### Проверить, поддерживается ли операция

Перед вызовом операции убедитесь, что она доступна:

```javascript
function isOperationSupported(capability, resourceType, operationName) {
  const rest = capability.rest.find(r => r.mode === 'server');
  const resource = rest.resource.find(r => r.type === resourceType);

  if (!resource || !resource.operation) return false;

  return resource.operation.some(op => op.name === operationName);
}

// Использование
if (isOperationSupported(capability, 'ValueSet', 'expand')) {
  // Вы можете использовать операцию $expand
}
```

### Получить доступные параметры поиска

Узнайте, какие параметры поиска вы можете использовать:

```javascript
function getSearchParams(capability, resourceType) {
  const rest = capability.rest.find(r => r.mode === 'server');
  const resource = rest.resource.find(r => r.type === resourceType);

  if (!resource || !resource.searchParam) return [];

  return resource.searchParam.map(sp => sp.name);
}

// Использование
const params = getSearchParams(capability, 'ValueSet');
console.log('Доступные параметры поиска:', params);
// Вывод: ['url', 'name', 'status', 'version', ...]
```

## Практический пример

Вот полный пример получения и использования CapabilityStatement:

```javascript
async function checkServerCapabilities() {
  // Получить CapabilityStatement
  const response = await fetch('https://playground.dhp.uz/fhir/metadata');
  const capability = await response.json();

  console.log('Сервер:', capability.implementation?.description || 'Неизвестно');
  console.log('Версия FHIR:', capability.fhirVersion);

  // Проверить поддержку терминологии
  const hasValueSet = isResourceSupported(capability, 'ValueSet');
  const hasExpand = isOperationSupported(capability, 'ValueSet', 'expand');
  const hasValidate = isOperationSupported(capability, 'ValueSet', 'validate-code');

  console.log('Ресурс ValueSet:', hasValueSet ? '✓' : '✗');
  console.log('Операция $expand:', hasExpand ? '✓' : '✗');
  console.log('Операция $validate-code:', hasValidate ? '✓' : '✗');

  // Включить/отключить функции в вашем приложении
  if (hasExpand) {
    enableValueSetExpansion();
  }

  if (hasValidate) {
    enableCodeValidation();
  }
}
```

## Лучшие практики

1. **Кэшируйте CapabilityStatement**: Возможности не меняются часто. Кэшируйте ответ и обновляйте периодически.

2. **Постепенная деградация**: Если операция не поддерживается, предоставьте альтернативную функциональность или понятные сообщения об ошибках.

3. **Проверяйте при запуске**: Получайте CapabilityStatement при запуске приложения для настройки доступных функций.

4. **Учитывайте версию**: Проверяйте поле `fhirVersion` для обеспечения совместимости с вашим приложением.

---

## Примеры кода

{% include code-tabs-style.html %}

Ниже приведены примеры получения и использования CapabilityStatement на различных языках программирования:

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
<pre><code class="language-bash"># Получить CapabilityStatement
curl "https://playground.dhp.uz/fhir/metadata" \
  -H "Accept: application/fhir+json"

# Можно использовать jq для извлечения конкретной информации
curl -s "https://playground.dhp.uz/fhir/metadata" | jq '.fhirVersion'

# Проверить, поддерживается ли ресурс ValueSet
curl -s "https://playground.dhp.uz/fhir/metadata" | \
  jq '.rest[].resource[] | select(.type=="ValueSet") | .type'

# Получить все операции для ValueSet
curl -s "https://playground.dhp.uz/fhir/metadata" | \
  jq '.rest[].resource[] | select(.type=="ValueSet") | .operation[].name'
</code></pre>
    </div>
    <div class="tab-pane" id="python">
<pre><code class="language-python">import requests
from typing import List, Dict, Optional

base_url = "https://playground.dhp.uz/fhir"

def get_capability_statement() -> Dict:
    """Получить CapabilityStatement сервера."""
    response = requests.get(
        f"{base_url}/metadata",
        headers={"Accept": "application/fhir+json"}
    )
    response.raise_for_status()
    return response.json()

def is_resource_supported(capability: Dict, resource_type: str) -> bool:
    """Проверить, поддерживается ли тип ресурса."""
    for rest in capability.get("rest", []):
        if rest.get("mode") == "server":
            for resource in rest.get("resource", []):
                if resource.get("type") == resource_type:
                    return True
    return False

def is_operation_supported(capability: Dict, resource_type: str,
                          operation_name: str) -> bool:
    """Проверить, поддерживается ли операция для ресурса."""
    for rest in capability.get("rest", []):
        if rest.get("mode") == "server":
            for resource in rest.get("resource", []):
                if resource.get("type") == resource_type:
                    operations = resource.get("operation", [])
                    return any(op.get("name") == operation_name
                             for op in operations)
    return False

def get_search_parameters(capability: Dict, resource_type: str) -> List[str]:
    """Получить доступные параметры поиска для ресурса."""
    for rest in capability.get("rest", []):
        if rest.get("mode") == "server":
            for resource in rest.get("resource", []):
                if resource.get("type") == resource_type:
                    return [sp.get("name")
                           for sp in resource.get("searchParam", [])]
    return []

# Пример использования
capability = get_capability_statement()

print(f"Сервер: {capability.get('implementation', {}).get('description', 'Неизвестно')}")
print(f"Версия FHIR: {capability.get('fhirVersion')}")
print()

# Проверить поддержку ресурсов
print("Поддержка ресурсов:")
print(f"  ValueSet: {is_resource_supported(capability, 'ValueSet')}")
print(f"  CodeSystem: {is_resource_supported(capability, 'CodeSystem')}")
print(f"  ConceptMap: {is_resource_supported(capability, 'ConceptMap')}")
print()

# Проверить поддержку операций
print("Операции ValueSet:")
print(f"  $expand: {is_operation_supported(capability, 'ValueSet', 'expand')}")
print(f"  $validate-code: {is_operation_supported(capability, 'ValueSet', 'validate-code')}")
print()

# Получить параметры поиска
params = get_search_parameters(capability, 'ValueSet')
print(f"Параметры поиска ValueSet: {', '.join(params[:5])}...")
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

// Пример использования
(async () => {
  try {
    const capability = await getCapabilityStatement();

    console.log('Сервер:', capability.implementation?.description || 'Неизвестно');
    console.log('Версия FHIR:', capability.fhirVersion);
    console.log('');

    // Проверить поддержку ресурсов
    console.log('Поддержка ресурсов:');
    console.log('  ValueSet:', isResourceSupported(capability, 'ValueSet'));
    console.log('  CodeSystem:', isResourceSupported(capability, 'CodeSystem'));
    console.log('  ConceptMap:', isResourceSupported(capability, 'ConceptMap'));
    console.log('');

    // Проверить поддержку операций
    console.log('Операции ValueSet:');
    console.log('  $expand:', isOperationSupported(capability, 'ValueSet', 'expand'));
    console.log('  $validate-code:', isOperationSupported(capability, 'ValueSet', 'validate-code'));
    console.log('');

    // Получить параметры поиска
    const params = getSearchParameters(capability, 'ValueSet');
    console.log('Параметры поиска ValueSet:', params.slice(0, 5).join(', ') + '...');

  } catch (error) {
    console.error('Ошибка:', error.message);
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

        // Проверить поддержку ресурсов
        System.out.println("Поддержка ресурсов:");
        System.out.println("  ValueSet: " + isResourceSupported(capability, "ValueSet"));
        System.out.println("  CodeSystem: " + isResourceSupported(capability, "CodeSystem"));
        System.out.println("  ConceptMap: " + isResourceSupported(capability, "ConceptMap"));
        System.out.println();

        // Проверить поддержку операций
        System.out.println("Операции ValueSet:");
        System.out.println("  $expand: " + isOperationSupported(capability, "ValueSet", "expand"));
        System.out.println("  $validate-code: " +
            isOperationSupported(capability, "ValueSet", "validate-code"));
        System.out.println();

        // Получить параметры поиска
        List&lt;String&gt; params = getSearchParameters(capability, "ValueSet");
        System.out.println("Параметры поиска ValueSet: " +
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

        // Проверить поддержку ресурсов
        Console.WriteLine("Поддержка ресурсов:");
        Console.WriteLine($"  ValueSet: {IsResourceSupported(capability, "ValueSet")}");
        Console.WriteLine($"  CodeSystem: {IsResourceSupported(capability, "CodeSystem")}");
        Console.WriteLine($"  ConceptMap: {IsResourceSupported(capability, "ConceptMap")}");
        Console.WriteLine();

        // Проверить поддержку операций
        Console.WriteLine("Операции ValueSet:");
        Console.WriteLine($"  $expand: {IsOperationSupported(capability, "ValueSet", "expand")}");
        Console.WriteLine($"  $validate-code: {IsOperationSupported(capability, "ValueSet", "validate-code")}");
        Console.WriteLine();

        // Получить параметры поиска
        var params = GetSearchParameters(capability, "ValueSet");
        Console.WriteLine($"Параметры поиска ValueSet: {string.Join(", ", params.Take(5))}...");
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
        fmt.Printf("Ошибка: %v\n", err)
        return
    }

    fmt.Printf("Сервер: %s\n", capability.Implementation.Description)
    fmt.Printf("Версия FHIR: %s\n\n", capability.FhirVersion)

    // Проверить поддержку ресурсов
    fmt.Println("Поддержка ресурсов:")
    fmt.Printf("  ValueSet: %v\n", isResourceSupported(capability, "ValueSet"))
    fmt.Printf("  CodeSystem: %v\n", isResourceSupported(capability, "CodeSystem"))
    fmt.Printf("  ConceptMap: %v\n\n", isResourceSupported(capability, "ConceptMap"))

    // Проверить поддержку операций
    fmt.Println("Операции ValueSet:")
    fmt.Printf("  $expand: %v\n", isOperationSupported(capability, "ValueSet", "expand"))
    fmt.Printf("  $validate-code: %v\n\n", isOperationSupported(capability, "ValueSet", "validate-code"))

    // Получить параметры поиска
    params := getSearchParameters(capability, "ValueSet")
    if len(params) > 5 {
        fmt.Printf("Параметры поиска ValueSet: %s...\n", params[:5])
    } else {
        fmt.Printf("Параметры поиска ValueSet: %s\n", params)
    }
}
</code></pre>
    </div>
  </div>
</div>

---

## Упражнение

**Задача:** Получите CapabilityStatement с сервера playground и ответьте на эти вопросы:

1. Какую версию FHIR поддерживает сервер?
2. Какие ресурсы терминологии поддерживаются? (CodeSystem, ValueSet, ConceptMap)
3. Какие операции доступны для ValueSet?
4. Можете ли вы искать ValueSet по имени?

```
GET https://playground.dhp.uz/fhir/metadata
```

Изучите ответ и напишите код для программной проверки этих возможностей.
