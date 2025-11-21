# Сценарий 1: Управление организациями

## Обзор

Цель: Получение существующих организаций и подразделений, их интеграция в программное обеспечение, обновление и создание по мере необходимости.

- Ресурсы: Organization
- Навыки: GET/POST/PUT/DELETE операции, поиск, ссылки, идентификаторы
- Базовый URL: `https://playground.dhp.uz/fhir`
- Профиль: [uz-core-organization](https://dhp.uz/fhir/core/en/StructureDefinition-uz-core-organization.html)

## Профиль uz-core-organization

### Обязательные элементы

- **name** (1..1): Название организации на узбекском языке

#### Переводы названия

Для добавления переводов названия на русский и каракалпакский языки используйте стандартное расширение [translation](http://hl7.org/fhir/R5/extension-translation.html). Расширение применяется к элементу `_name`:

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

Коды языков:
- `uz` - узбекский (основной язык для поля `name`)
- `ru` - русский
- `kaa` - каракалпакский

### Must-Support элементы

UZ Core профили: Элементы, отмеченные как Must Support, должны быть заполнены при обмене данными между системами, работающими в Узбекистане.

Когда данные не могут быть заполнены, потому что они недоступны в исходной системе, элемент может остаться пустым — при условии, что правила кардинальности это позволяют. Однако, когда требования кардинальности обязывают включение, системы должны использовать расширение Data Absent Reason, а не оставлять элемент пустым.

#### Элементы профиля

- **identifier**: Идентификаторы организации
  - **taxId**: Налоговый идентификатор (`system`: `https://dhp.uz/fhir/core/sid/org/uz/soliq`)
  - **argosId**: Идентификатор ARGOS (`system`: `https://dhp.uz/fhir/core/sid/org/uz/argos`)
- **active**: Статус активности
- **type**: Тип организации. Элемент использует множественные системы кодирования для классификации организаций по разным измерениям:
  - Группа номенклатуры (nomenclatureGroup) - институциональная группировка
  - Группа организационных услуг (organizationalServiceGroup) - классификация по предоставляемым услугам
  - Организационная структура (organizationalStructure) - структурная классификация
  - Тип организации (organizationType) - основной тип учреждения
  - Специализация (specialization) - медицинская специализация
  - Группа подчинения (subordinationGroup) - административная подчинённость
  - Статус без юридического лица (withoutLegalStatus) - юридический статус

  Допустимые коды для каждого измерения можно найти в соответствующих наборах значений (ValueSets), привязанных к каждому срезу (slice) в [профиле uz-core-organization](https://dhp.uz/fhir/core/en/StructureDefinition-uz-core-organization.html).
- **partOf**: Ссылка на родительскую организацию

## CRUD операции

### Create (Создание)

- HTTP метод: POST
- Endpoint: `/Organization`
- Заголовки: `Content-Type: application/fhir+json`

Создание новой организации. Сервер присваивает уникальный ID и возвращает Location header.

Минимальный пример:
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

Ответ: HTTP 201 Created с Location header и созданным ресурсом.

### Read (Чтение)

- HTTP метод: GET
- Endpoint: `/Organization/[id]`

Получение конкретной организации по ID.

Ответ: HTTP 200 OK с ресурсом Organization или HTTP 404 Not Found.

### Update (Обновление)

- HTTP метод: PUT
- Endpoint: `/Organization/[id]`
- Заголовки:
  - `Content-Type: application/fhir+json`
  - `If-Match: W/"[versionId]"` (обязательно для предотвращения конфликтов)

Полное обновление организации. Необходимо отправить весь ресурс, включая элемент `id`. Заголовок `If-Match` обязателен и должен содержать версию ресурса из элемента `meta.versionId`, чтобы предотвратить конфликты при одновременном редактировании (optimistic locking).

Пример запроса:
```
PUT /Organization/existing-id
If-Match: W/"2"
Content-Type: application/fhir+json
```

Пример тела запроса:
```json
{
  "resourceType": "Organization",
  "id": "existing-id",
  "meta": {
    "profile": ["https://dhp.uz/fhir/core/StructureDefinition/uz-core-organization"]
  },
  "identifier": [...],
  "active": true,
  "name": "Обновлённое название"
}
```

Ответ: HTTP 200 OK с обновлённым ресурсом.

### Delete (Удаление)

- HTTP метод: DELETE
- Endpoint: `/Organization/[id]`

Удаление организации.

Ответ: HTTP 200 OK с OperationOutcome при успешном удалении. При попытке прочитать удалённый ресурс сервер вернёт HTTP 410 Gone.

## Поиск

- HTTP метод: GET
- Endpoint: `/Organization?[параметры]`

### Параметры поиска

| Параметр | Тип | Описание | Пример |
|----------|-----|----------|--------|
| `_id` | token | Поиск по ID | `?_id=123` |
| `identifier` | token | Поиск по идентификатору | `?identifier=https://dhp.uz/fhir/core/sid/org/uz/soliq\|123456789` |
| `name` | string | Поиск по названию (частичное совпадение) | `?name=Fergana` |
| `name:exact` | string | Точное совпадение имени | `?name:exact=Fergana` |
| `type` | token | Поиск по типу организации | `?type=prov` |
| `active` | token | Фильтр по статусу | `?active=true` |
| `partof` | reference | Поиск подразделений | `?partof=Organization/parent-id` |

### Модификаторы и префиксы

Комбинирование параметров (логическое AND):
```
GET /Organization?name=Hospital&active=true
```

Множественные значения (логическое OR):
```
GET /Organization?type=prov,dept
```

### Пагинация

Результаты поиска возвращаются в Bundle с пагинацией (20 записей на страницу):

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

Используйте `Bundle.link` с `relation="next"` для получения следующей страницы.

**Известная проблема**: Поле `Bundle.total` может возвращать `0` даже при наличии результатов. Для подсчёта организаций на текущей странице фильтруйте `Bundle.entry` по `resourceType == "Organization"` (в ответе могут быть ресурсы `OperationOutcome`).

## Иерархия организаций

Подразделения связываются с родительскими организациями через элемент `partOf`:

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

Получить все подразделения организации:
```
GET /Organization?partof=Organization/parent-org-id
```

## Пакетные операции

Используйте Bundle типа "transaction" или "batch" для выполнения нескольких операций:

Endpoint: `/` (корневой)

```json
{
  "resourceType": "Bundle",
  "type": "transaction",
  "entry": [
    {
      "request": {
        "method": "POST",
        "url": "Organization"
      },
      "resource": {
        "resourceType": "Organization",
        ...
      }
    },
    {
      "request": {
        "method": "PUT",
        "url": "Organization/existing-id"
      },
      "resource": {
        "resourceType": "Organization",
        "id": "existing-id",
        ...
      }
    }
  ]
}
```

- **transaction**: Атомарное выполнение (всё или ничего)
- **batch**: Независимое выполнение каждой операции

## Обработка ошибок

### Коды ответов

| Код | Описание |
|-----|----------|
| 200 | OK - успешное получение/обновление/удаление |
| 201 | Created - успешное создание |
| 400 | Bad Request - невалидный JSON |
| 404 | Not Found - ресурс не найден |
| 409 | Conflict - конфликт версий |
| 410 | Gone - ресурс был удалён |
| 412 | Precondition Failed - не передан заголовок If-Match или версия не совпадает |
| 422 | Unprocessable Entity - не прошёл валидацию профиля |

### OperationOutcome

При ошибках сервер возвращает OperationOutcome:

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

## Примеры организаций в системе

Типы организаций:
- **prov** (Healthcare Provider): Медицинские учреждения
- **dept** (Department): Отделения и кабинеты

Примеры из системы:
- Fergana District Department of Sanitary-Epidemiological Safety
- Yashnobod District Medical Union - Family Polyclinic #32
- Endoscopy Cabinet (подразделение)
- Bacteriology Laboratory (подразделение)

## Полезные ссылки

- [FHIR Organization Resource](http://hl7.org/fhir/R5/organization.html)
- [uz-core-organization Profile](https://dhp.uz/fhir/core/en/StructureDefinition-uz-core-organization.html)
- [FHIR RESTful API](http://hl7.org/fhir/R5/http.html)
- [FHIR Search](http://hl7.org/fhir/R5/search.html)

---

## Примеры кода

{% include code-tabs-style.html %}

Ниже представлены примеры создания новой организации на различных языках программирования:

<div class="code-tabs">
  <ul class="nav nav-tabs" role="tablist">
    <li class="active">
      <a href="#python" data-toggle="tab">Python</a>
    </li>
    <li>
      <a href="#javascript" data-toggle="tab">JavaScript</a>
    </li>
    <li>
      <a href="#java" data-toggle="tab">Java</a>
    </li>
    <li>
      <a href="#curl" data-toggle="tab">cURL</a>
    </li>
  </ul>
  <div class="tab-content">
    <div class="tab-pane active" id="python">
<pre><code class="language-python">import requests
from fhir.resources.organization import Organization
from fhir.resources.identifier import Identifier
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.meta import Meta

# FHIR сервер базовый URL
base_url = "https://playground.dhp.uz/fhir"

# Создание новой организации с использованием fhir.resources
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

# Отправка POST запроса
response = requests.post(
    f"{base_url}/Organization",
    headers={"Content-Type": "application/fhir+json"},
    data=organization.json()
)

if response.status_code == 201:
    created_org = response.json()
    print(f"Организация создана с ID: {created_org['id']}")
else:
    print(f"Ошибка: {response.status_code}")
    print(response.text)
</code></pre>
    </div>
    <div class="tab-pane" id="javascript">
<pre><code class="language-javascript">// Используя fetch API
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

// Создание организации
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
  throw new Error(`Ошибка: ${response.status}`);
})
.then(data =&gt; {
  console.log(`Организация создана с ID: ${data.id}`);
})
.catch(error =&gt; {
  console.error('Ошибка:', error);
});
</code></pre>
    </div>
    <div class="tab-pane" id="java">
<pre><code class="language-java">import ca.uhn.fhir.context.FhirContext;
import ca.uhn.fhir.rest.client.api.IGenericClient;
import org.hl7.fhir.r5.model.*;

// Создание FHIR контекста и клиента
FhirContext ctx = FhirContext.forR5();
IGenericClient client = ctx.newRestfulGenericClient("https://playground.dhp.uz/fhir");

// Создание организации
Organization organization = new Organization();

// Установка профиля
organization.getMeta()
    .addProfile("https://dhp.uz/fhir/core/StructureDefinition/uz-core-organization");

// Добавление идентификатора
Identifier taxId = organization.addIdentifier();
taxId.setSystem("https://dhp.uz/fhir/core/sid/org/uz/soliq");
taxId.setValue("123456789");
CodeableConcept taxType = new CodeableConcept();
taxType.addCoding()
    .setSystem("http://terminology.hl7.org/CodeSystem/v2-0203")
    .setCode("TAX");
taxId.setType(taxType);

// Установка статуса
organization.setActive(true);

// Добавление типа
CodeableConcept orgType = new CodeableConcept();
orgType.addCoding()
    .setSystem("http://terminology.hl7.org/CodeSystem/organization-type")
    .setCode("prov")
    .setDisplay("Healthcare Provider");
organization.addType(orgType);

// Установка названия
organization.setName("Yangi tibbiyot muassasasi");

// Создание на сервере
MethodOutcome outcome = client.create()
    .resource(organization)
    .execute();

// Получение ID созданной организации
IdType id = (IdType) outcome.getId();
System.out.println("Организация создана с ID: " + id.getIdPart());
</code></pre>
    </div>
    <div class="tab-pane" id="curl">
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
  </div>
</div>
