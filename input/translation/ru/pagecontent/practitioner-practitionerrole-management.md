# Управление медицинскими работниками

## Обзор

Цель: Получение существующих записей Practitioner и PractitionerRole, их интеграция в программное обеспечение, обновление и создание по мере необходимости, назначение ролей в организациях, управление квалификациями.

- Ресурсы: Practitioner, PractitionerRole
- Навыки: GET/POST/PUT/DELETE операции, поиск, ссылки, идентификаторы
- Базовый URL: `https://playground.dhp.uz/fhir`
- Профили:
  - [uz-core-practitioner](https://dhp.uz/fhir/core/en/StructureDefinition-uz-core-practitioner.html)
  - [uz-core-practitionerrole](https://dhp.uz/fhir/core/en/StructureDefinition-uz-core-practitionerrole.html)

**Обратная связь:** Поделитесь своим опытом, проблемами и успехами в [документе коннектафона](https://docs.google.com/document/d/1PdQ8zBI9xkISP3tAqIK8-TGMql3kVVZ4UNoHVYqCy4Y/edit?usp=sharing).

## Профиль uz-core-practitioner

**Примечание**: В настоящее время валидация на сервере отключена, но клиентские приложения должны следовать правилам профиля для обеспечения совместимости и качества данных.

### Обязательные элементы

В этом профиле нет обязательных элементов с минимальной кардинальностью больше 0. Все элементы являются опциональными, хотя Must Support элементы должны быть заполнены, когда данные доступны.

### Must-Support элементы

UZ Core профили: Элементы, отмеченные как Must Support, должны быть заполнены при обмене данными между системами, работающими в Узбекистане.

Когда данные не могут быть заполнены, потому что они недоступны в исходной системе, элемент может остаться пустым — при условии, что правила кардинальности это позволяют. Однако, когда требования кардинальности обязывают включение, системы должны использовать расширение Data Absent Reason, а не оставлять элемент пустым.

#### Элементы профиля

- **identifier**: Идентификаторы практикующего специалиста (nationalId из системы ARGOS)
- **active**: Статус практики
- **name**: Имя практикующего специалиста
  - **use**: Использование имени (official, usual и т.д.)
  - **text**: Полное имя как оно отображается
  - **family**: Фамилия
  - **given**: Имена
  - **suffix**: Суффикс имени (например, Jr., MD)
  - **period**: Период времени, когда имя было/есть в использовании
- **telecom**: Контактные данные (телефон, email и т.д.)
  - **system**: Тип контакта (phone, email, fax и т.д.)
  - **value**: Фактическое значение контакта
  - **use**: Назначение (home, work, mobile и т.д.)
  - **rank**: Порядок предпочтения
  - **period**: Период времени, когда контакт действителен/был действителен
- **gender**: Административный пол (male, female, other, unknown)
  - Когда gender = "other", должно быть включено расширение **gender-other** (`https://dhp.uz/fhir/core/StructureDefinition/gender-other`) для дифференциации пола
- **birthDate**: Дата рождения
- **deceased[x]**: Индикатор смерти (boolean) или дата/время смерти
- **address**: Адреса практикующего специалиста двух типов:
  - **uzAddress**: Адреса в Узбекистане (код страны "UZ") с поддержкой махалли. **Необходимо использовать кодированные значения** из официальных реестров для административных подразделений (state, district, city/mahalla)
  - **i18nAddress**: Международные адреса (не Узбекистан). Административные подразделения используют свободный текст без обязательных наборов значений
- **photo**: Фотография практикующего специалиста
- **qualification**: Квалификации, полученные практикующим специалистом
  - **identifier**: Идентификатор квалификации
  - **code**: Код квалификации (обязательный)
  - **period**: Период действия квалификации
  - **issuer**: Организация, выдавшая квалификацию

### Дифференциация пола

Когда пол практикующего специалиста установлен как "other", профиль требует расширение `gender-other`:

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
              "display": "Сменил пол на мужчину"
            }
          ]
        }
      }
    ]
  }
}
```

### Типы адресов

Для подробного руководства по работе с адресами см. [Работа с адресами](https://dhp.uz/fhir/core/ru/fhir-basics.html#working-with-addresses).

**Узбекский адрес (uzAddress):**
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

**Международный адрес (i18nAddress):**
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

## Профиль uz-core-practitionerrole

Ресурс PractitionerRole описывает конкретный набор ролей, специальностей, услуг и мест, где практикующий специалист может оказывать услуги.

### Ключевые элементы

- **identifier**: Бизнес-идентификаторы для этой роли
- **active**: Активна ли эта запись роли практикующего специалиста
- **period**: Период времени, в течение которого практикующему специалисту разрешено выполнять эти роли
- **practitioner**: Ссылка на ресурс Practitioner
- **organization**: Ссылка на организацию, где выполняются роли
- **code**: Роли, которые этот практикующий специалист уполномочен выполнять
- **specialty**: Специфическая специальность практикующего специалиста
- **location**: Место(а), где этот практикующий специалист оказывает помощь
- **telecom**: Контактные данные, специфичные для этой роли
- **endpoint**: Технические конечные точки, обеспечивающие доступ к услугам, работающим для роли

### Отношения Practitioner-Organization

PractitionerRole связывает практикующих специалистов с организациями, где они работают:

```json
{
  "resourceType": "PractitionerRole",
  "id": "example",
  "language": "uz",
  "active": true,
  "practitioner": {
    "reference": "Practitioner/123",
    "display": "Д-р Алишер Каримов"
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

## CRUD операции

### Create Practitioner (Создание)

- HTTP метод: POST
- Endpoint: `/Practitioner`
- Заголовки: `Content-Type: application/fhir+json`

Создание нового практикующего специалиста. Сервер присваивает уникальный ID и возвращает Location header.

Минимальный пример:
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
      "family": "Каримов",
      "given": ["Алишер", "Акбарович"]
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

Ответ: HTTP 201 Created с Location header и созданным ресурсом.

### Create PractitionerRole (Создание)

- HTTP метод: POST
- Endpoint: `/PractitionerRole`
- Заголовки: `Content-Type: application/fhir+json`

Создание новой роли практикующего специалиста, связывающей практикующего специалиста с организацией.

Пример:
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
    "display": "Д-р Алишер Каримов"
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

Ответ: HTTP 201 Created с Location header и созданным ресурсом.

### Read Practitioner (Чтение)

- HTTP метод: GET
- Endpoint: `/Practitioner/[id]`

Получение конкретного практикующего специалиста по ID. В системе уже загружено много практикующих специалистов из системы Argos HRM.

Ответ: HTTP 200 OK с ресурсом Practitioner или HTTP 404 Not Found.

### Read PractitionerRole (Чтение)

- HTTP метод: GET
- Endpoint: `/PractitionerRole/[id]`

Получение конкретной роли практикующего специалиста по ID.

Ответ: HTTP 200 OK с ресурсом PractitionerRole или HTTP 404 Not Found.

### Update Practitioner (Обновление)

- HTTP метод: PUT
- Endpoint: `/Practitioner/[id]`
- Заголовки:
  - `Content-Type: application/fhir+json`
  - `If-Match: W/"[versionId]"` (обязателен для предотвращения конфликтов)

Полное обновление практикующего специалиста. Необходимо отправить весь ресурс, включая элемент `id`. Заголовок `If-Match` обязателен и должен содержать версию ресурса из элемента `meta.versionId` для предотвращения конфликтов при одновременном редактировании (оптимистическая блокировка).

Пример запроса:
```
PUT /Practitioner/existing-id
If-Match: W/"2"
Content-Type: application/fhir+json
```

Пример тела запроса:
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
      "family": "Каримов",
      "given": ["Алишер", "Акбарович"]
    }
  ],
  "gender": "male",
  "qualification": [...]
}
```

Ответ: HTTP 200 OK с обновленным ресурсом.

### Update PractitionerRole (Обновление)

- HTTP метод: PUT
- Endpoint: `/PractitionerRole/[id]`
- Заголовки:
  - `Content-Type: application/fhir+json`
  - `If-Match: W/"[versionId]"` (обязателен для предотвращения конфликтов)

Полное обновление роли практикующего специалиста. Необходимо отправить весь ресурс, включая элемент `id`. Заголовок `If-Match` обязателен для оптимистической блокировки.

Ответ: HTTP 200 OK с обновленным ресурсом.

### Delete Practitioner (Удаление)

- HTTP метод: DELETE
- Endpoint: `/Practitioner/[id]`

Удаление практикующего специалиста.

Ответ: HTTP 200 OK с OperationOutcome при успешном удалении. При попытке чтения удаленного ресурса сервер вернет HTTP 410 Gone.

### Delete PractitionerRole (Удаление)

- HTTP метод: DELETE
- Endpoint: `/PractitionerRole/[id]`

Удаление роли практикующего специалиста.

Ответ: HTTP 200 OK с OperationOutcome при успешном удалении. При попытке чтения удаленного ресурса сервер вернет HTTP 410 Gone.

## Операции поиска

- HTTP метод: GET
- Endpoint: `/Practitioner?[parameters]` или `/PractitionerRole?[parameters]`

Все поддерживаемые параметры поиска можно найти в capability statement по адресу [DHPCapabilityStatement](https://dhp.uz/fhir/core/en/CapabilityStatement-DHPCapabilityStatement.html) или запросом к [/metadata](https://playground.dhp.uz/fhir/metadata) endpoint.

### Параметры поиска Practitioner

| Параметр | Тип | Описание | Пример |
|----------|-----|----------|--------|
| `_id` | token | Поиск по ID | `?_id=123` |
| `identifier` | token | Поиск по идентификатору | `?identifier=https://dhp.uz/fhir/core/sid/pro/uz/argos\|12345` |
| `name` | string | Поиск по имени (частичное совпадение) | `?name=Каримов` |
| `given` | string | Поиск по имени | `?given=Алишер` |
| `family` | string | Поиск по фамилии | `?family=Каримов` |
| `telecom` | token | Поиск по контактным данным | `?telecom=%2B998901234567` |
| `phone` | token | Поиск по номеру телефона | `?phone=%2B998901234567` |
| `email` | token | Поиск по email | `?email=doctor@example.com` |
| `address` | string | Поиск по адресу | `?address=Toshkent` |
| `address-city` | string | Поиск по городу | `?address-city=Toshkent` |
| `address-country` | string | Поиск по стране | `?address-country=UZ` |
| `address-postalcode` | string | Поиск по почтовому индексу | `?address-postalcode=100084` |
| `address-state` | string | Поиск по региону | `?address-state=Toshkent` |
| `gender` | token | Поиск по полу | `?gender=male` |
| `birthdate` | date | Поиск по дате рождения | `?birthdate=1980-05-15` |
| `active` | token | Фильтр по статусу | `?active=true` |
| `deceased` | token | Фильтр по статусу умерших | `?deceased=false` |
| `qualification-code` | token | Поиск по квалификации | `?qualification-code=MD` |

### Параметры поиска PractitionerRole

| Параметр | Тип | Описание | Пример |
|----------|-----|----------|--------|
| `_id` | token | Поиск по ID | `?_id=456` |
| `identifier` | token | Поиск по идентификатору | `?identifier=system\|value` |
| `practitioner` | reference | Поиск по практикующему специалисту | `?practitioner=Practitioner/123` |
| `organization` | reference | Поиск по организации | `?organization=Organization/789` |
| `location` | reference | Поиск по месту | `?location=Location/101` |
| `role` | token | Поиск по роли | `?role=doctor` |
| `specialty` | token | Поиск по специальности | `?specialty=394814009` |
| `active` | token | Фильтр по статусу | `?active=true` |
| `date` | date | Поиск по периоду | `?date=2024` |
| `service` | reference | Поиск по услуге | `?service=HealthcareService/202` |
| `endpoint` | reference | Поиск по endpoint | `?endpoint=Endpoint/303` |
| `telecom` | token | Поиск по контакту | `?telecom=phone\|%2B998901234567` |
| `phone` | token | Поиск по телефону | `?phone=%2B998901234567` |

### Распространенные шаблоны поиска

**Найти практикующих специалистов по имени:**
```
GET /Practitioner?name=Каримов
```

**Найти практикующих специалистов в конкретном городе:**
```
GET /Practitioner?address-city=Toshkent&active=true
```

**Найти все роли для конкретного практикующего специалиста:**
```
GET /PractitionerRole?practitioner=Practitioner/123
```

**Найти всех практикующих специалистов, работающих в конкретной организации:**
```
GET /PractitionerRole?organization=Organization/789
```

**Найти практикующих специалистов по квалификации:**
```
GET /Practitioner?qualification-code=http://terminology.hl7.org/CodeSystem/v2-0360|MD
```

**Найти активных специалистов определенного типа:**
```
GET /PractitionerRole?specialty=https://terminology.dhp.uz/fhir/core/CodeSystem/profession-specialization-cs|419772000&active=true
```

### Модификаторы и префиксы

Комбинирование параметров (логическое И):
```
GET /Practitioner?family=Каримов&address-city=Toshkent&active=true
```

Множественные значения (логическое ИЛИ):
```
GET /Practitioner?gender=male,female
```

Сравнения дат:
```
GET /Practitioner?birthdate=gt1980-01-01&birthdate=lt1990-12-31
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
      "url": "https://playground.dhp.uz/fhir/Practitioner?name=Каримов&_page=1"
    },
    {
      "relation": "next",
      "url": "https://playground.dhp.uz/fhir/Practitioner?name=Каримов&_page=2"
    }
  ],
  "entry": [...]
}
```

Используйте `Bundle.link` с `relation="next"` для получения следующей страницы.

**Известная проблема**: Поле `Bundle.total` может возвращать `0` даже при наличии результатов. Для подсчета практикующих специалистов на текущей странице фильтруйте `Bundle.entry` по `resourceType == "Practitioner"` (ответ может содержать ресурсы `OperationOutcome`).

## Рабочий процесс интеграции

### Типичный сценарий интеграции

1. **Поиск практикующих специалистов** в вашей организации:
   ```
   GET /PractitionerRole?organization=Organization/your-org-id
   ```

2. **Получение данных практикующего специалиста** для каждой роли:
   ```
   GET /Practitioner/practitioner-id
   ```

3. **Получение квалификаций** из ресурса Practitioner

4. **Получение дополнительных данных роли** при необходимости:
   ```
   GET /PractitionerRole/role-id
   ```

### Поиск практикующих специалистов и их организаций

Чтобы найти всех практикующих специалистов и места их работы:

```
GET /PractitionerRole?_include=PractitionerRole:practitioner&_include=PractitionerRole:organization
```

Это вернет ресурсы PractitionerRole вместе со ссылочными ресурсами Practitioner и Organization в одном Bundle.

## Обработка ошибок

### Коды ответа

| Код | Описание |
|-----|----------|
| 200 | OK - успешное получение/обновление/удаление |
| 201 | Created - успешное создание |
| 400 | Bad Request - недопустимые параметры поиска |
| 404 | Not Found - ресурс не найден |
| 409 | Conflict - конфликт версий |
| 410 | Gone - ресурс был удален |
| 412 | Precondition Failed - заголовок If-Match не предоставлен или несоответствие версий |
| 422 | Unprocessable Entity - неудачная валидация профиля |

### OperationOutcome

При ошибках сервер возвращает OperationOutcome:

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

## Примеры практикующих специалистов в системе

Система содержит практикующих специалистов, загруженных из системы Argos HRM, включая:
- Врачи с различными специальностями (общая практика, кардиология, педиатрия и т.д.)
- Медсестры
- Лабораторные специалисты
- Административный персонал
- Медицинские техники

Каждый практикующий специалист имеет:
- Национальный идентификатор из ARGOS
- Полное имя на узбекском языке (с возможными переводами на русский и каракалпакский)
- Контактную информацию
- Адрес (обычно в Узбекистане)
- Квалификации и специализации
- Связанные роли в медицинских организациях

## Полезные ссылки

- [FHIR Practitioner Resource](http://hl7.org/fhir/R5/practitioner.html)
- [FHIR PractitionerRole Resource](http://hl7.org/fhir/R5/practitionerrole.html)
- [uz-core-practitioner Profile](https://dhp.uz/fhir/core/en/StructureDefinition-uz-core-practitioner.html)
- [uz-core-practitionerrole Profile](https://dhp.uz/fhir/core/en/StructureDefinition-uz-core-practitionerrole.html)
- [FHIR RESTful API](http://hl7.org/fhir/R5/http.html)
- [FHIR Search](http://hl7.org/fhir/R5/search.html)

---

## Примеры кода

{% include code-tabs-style.html %}

Ниже приведены примеры создания нового практикующего специалиста на различных языках программирования:

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
      "family": "Каримов",
      "given": ["Алишер", "Акбарович"]
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

# Базовый URL FHIR сервера
base_url = "https://playground.dhp.uz/fhir"

# Создание нового практикующего специалиста используя fhir.resources
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
            family="Каримов",
            given=["Алишер", "Акбарович"]
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

# Отправка POST запроса
response = requests.post(
    f"{base_url}/Practitioner",
    headers={"Content-Type": "application/fhir+json"},
    data=practitioner.json()
)

if response.status_code == 201:
    created_practitioner = response.json()
    print(f"Практикующий специалист создан с ID: {created_practitioner['id']}")
else:
    print(f"Ошибка: {response.status_code}")
    print(response.text)
</code></pre>
    </div>
    <div class="tab-pane" id="javascript">
<pre><code class="language-javascript">// Используя fetch API
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
      family: "Каримов",
      given: ["Алишер", "Акбарович"]
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

// Создание практикующего специалиста
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
  throw new Error(`Ошибка: ${response.status}`);
})
.then(data => {
  console.log(`Практикующий специалист создан с ID: ${data.id}`);
})
.catch(error => {
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

// Создание практикующего специалиста
Practitioner practitioner = new Practitioner();

// Установка профиля
practitioner.getMeta()
    .addProfile("https://dhp.uz/fhir/core/StructureDefinition/uz-core-practitioner");

// Установка языка
practitioner.setLanguage("uz");

// Добавление идентификатора
Identifier nationalId = practitioner.addIdentifier();
nationalId.setUse(Identifier.IdentifierUse.OFFICIAL);
nationalId.setSystem("https://dhp.uz/fhir/core/sid/pro/uz/argos");
nationalId.setValue("12345678");
CodeableConcept idType = new CodeableConcept();
idType.addCoding()
    .setSystem("http://terminology.hl7.org/CodeSystem/v2-0203")
    .setCode("NI");
nationalId.setType(idType);

// Установка статуса
practitioner.setActive(true);

// Добавление имени
HumanName name = practitioner.addName();
name.setUse(HumanName.NameUse.OFFICIAL);
name.setFamily("Каримов");
name.addGiven("Алишер");
name.addGiven("Акбарович");

// Установка пола
practitioner.setGender(Enumerations.AdministrativeGender.MALE);

// Добавление квалификации
Practitioner.PractitionerQualificationComponent qual = practitioner.addQualification();
CodeableConcept qualCode = new CodeableConcept();
qualCode.addCoding()
    .setSystem("http://terminology.hl7.org/CodeSystem/v2-0360")
    .setCode("MD")
    .setDisplay("Doctor of Medicine");
qual.setCode(qualCode);

// Создание на сервере
MethodOutcome outcome = client.create()
    .resource(practitioner)
    .execute();

// Получение ID созданного практикующего специалиста
IdType id = (IdType) outcome.getId();
System.out.println("Практикующий специалист создан с ID: " + id.getIdPart());
</code></pre>
    </div>
    <div class="tab-pane" id="csharp">
<pre><code class="language-csharp">using Hl7.Fhir.Model;
using Hl7.Fhir.Rest;
using System;

// Создание FHIR клиента
var client = new FhirClient("https://playground.dhp.uz/fhir");

// Создание практикующего специалиста
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
            Family = "Каримов",
            Given = new[] { "Алишер", "Акбарович" }
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

// Создание на сервере
var createdPractitioner = client.Create(practitioner);
Console.WriteLine($"Практикующий специалист создан с ID: {createdPractitioner.Id}");
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

    // Создание практикующего специалиста
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
                Family: "Каримов",
                Given:  []string{"Алишер", "Акбарович"},
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

    // Сериализация в JSON
    jsonData, err := json.Marshal(pract)
    if err != nil {
        panic(err)
    }

    // Отправка POST запроса
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
        fmt.Printf("Практикующий специалист создан с ID: %s\n", createdPract.ID)
    } else {
        fmt.Printf("Ошибка: %d\n", resp.StatusCode)
    }
}
</code></pre>
    </div>
  </div>
</div>
