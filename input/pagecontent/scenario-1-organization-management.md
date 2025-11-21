# Сценарий 1: Управление организациями

## Обзор

**Цель**: Получение существующих организаций и подразделений, их интеграция в программное обеспечение, обновление и создание по мере необходимости.

**Ресурсы**: Organization
**Навыки**: GET/POST/PUT/DELETE операции, поиск, ссылки, идентификаторы
**Базовый URL**: `https://playground.dhp.uz/fhir`
**Профиль**: [uz-core-organization](https://dhp.uz/fhir/core/en/StructureDefinition-uz-core-organization.html)

## Профиль uz-core-organization

### Обязательные элементы

- **name** (1..1): Название организации на узбекском языке

### Must-Support элементы

- **identifier**: Идентификаторы организации
  - **taxId**: Налоговый идентификатор (`system`: `https://soliq.uz`, `type.coding.code`: `TAX`)
  - **argosId**: Идентификатор ARGOS (`system`: `https://hrm.argos.uz`)
- **active**: Статус активности
- **type**: Классификации организации (nomenclatureGroup, organizationalServiceGroup, organizationalStructure, organizationType, specialization, subordinationGroup, withoutLegalStatus)
- **partOf**: Ссылка на родительскую организацию

## CRUD операции

### Create (Создание)

**HTTP метод**: POST
**Endpoint**: `/Organization`
**Заголовки**: `Content-Type: application/fhir+json`

Создание новой организации. Сервер присваивает уникальный ID и возвращает Location header.

**Минимальный пример**:
```json
{
  "resourceType": "Organization",
  "meta": {
    "profile": ["https://dhp.uz/fhir/core/StructureDefinition/uz-core-organization"]
  },
  "identifier": [
    {
      "system": "https://soliq.uz",
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
}
```

**Ответ**: HTTP 201 Created с Location header и созданным ресурсом.

#### Условное создание

Используйте заголовок `If-None-Exist` для предотвращения дублирования:

```
POST /Organization
If-None-Exist: identifier=https://soliq.uz|123456789
```

### Read (Чтение)

**HTTP метод**: GET
**Endpoint**: `/Organization/[id]`

Получение конкретной организации по ID.

**Ответ**: HTTP 200 OK с ресурсом Organization или HTTP 404 Not Found.

### Update (Обновление)

**HTTP метод**: PUT
**Endpoint**: `/Organization/[id]`
**Заголовки**: `Content-Type: application/fhir+json`

Полное обновление организации. Необходимо отправить весь ресурс, включая элемент `id`.

**Пример**:
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

**Ответ**: HTTP 200 OK с обновлённым ресурсом.

#### Условное обновление

Обновление по бизнес-идентификатору:

```
PUT /Organization?identifier=https://soliq.uz|123456789
```

### Delete (Удаление)

**HTTP метод**: DELETE
**Endpoint**: `/Organization/[id]`

Удаление организации. Обратите внимание на ограничения целостности данных (например, организацию нельзя удалить, если на неё ссылаются другие ресурсы).

**Ответ**: HTTP 204 No Content или HTTP 404 Not Found.

## Поиск

**HTTP метод**: GET
**Endpoint**: `/Organization?[параметры]`

### Параметры поиска

| Параметр | Тип | Описание | Пример |
|----------|-----|----------|--------|
| `_id` | token | Поиск по ID | `?_id=123` |
| `identifier` | token | Поиск по идентификатору | `?identifier=https://soliq.uz\|123456789` |
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

**Endpoint**: `/` (корневой)

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

**transaction**: Атомарное выполнение (всё или ничего)
**batch**: Независимое выполнение каждой операции

## Обработка ошибок

### Коды ответов

| Код | Описание |
|-----|----------|
| 200 | OK - успешное получение/обновление |
| 201 | Created - успешное создание |
| 204 | No Content - успешное удаление |
| 400 | Bad Request - невалидный JSON |
| 404 | Not Found - ресурс не найден |
| 409 | Conflict - конфликт версий |
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

- [FHIR Organization Resource](http://hl7.org/fhir/R4/organization.html)
- [uz-core-organization Profile](https://dhp.uz/fhir/core/en/StructureDefinition-uz-core-organization.html)
- [FHIR RESTful API](http://hl7.org/fhir/R4/http.html)
- [FHIR Search](http://hl7.org/fhir/R4/search.html)

---

См. также примеры кода для различных языков программирования.
