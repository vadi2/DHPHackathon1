# Основы терминологии

## Обзор

Цель: Научиться искать и получать ресурсы терминологии (CodeSystem, ValueSet, ConceptMap), понимать управление версиями и использовать операции FHIR терминологии для поддержки кодированных данных в ваших приложениях.

- Ресурсы: CodeSystem, ValueSet, ConceptMap
- Навыки: Параметры поиска, фильтрация, операции терминологии ($expand, $validate-code, $lookup), управление версиями
- Базовый URL: `https://playground.dhp.uz/fhir`
  - **Примечание:** Это временный URL, который будет заменён на финальный ближе к коннектафону
- Полезные ссылки:
  - [FHIR Terminology Service](http://hl7.org/fhir/R5/terminology-service.html)
  - [uz-core Артефакты](https://dhp.uz/fhir/core/en/artifacts.html)
  - [FHIR CodeSystem Resource](http://hl7.org/fhir/R5/codesystem.html)
  - [FHIR ValueSet Resource](http://hl7.org/fhir/R5/valueset.html)
  - [FHIR ConceptMap Resource](http://hl7.org/fhir/R5/conceptmap.html)

**Обратная связь:** Поделитесь своим опытом, проблемами и успехами в [документе коннектафона](https://docs.google.com/document/d/1PdQ8zBI9xkISP3tAqIK8-TGMql3kVVZ4UNoHVYqCy4Y/edit?usp=sharing).

## Понимание терминологии FHIR

FHIR предоставляет три основных ресурса для работы с терминологией. Понимание того, когда и как использовать каждый из них, имеет решающее значение для создания совместимых медицинских приложений.

### CodeSystem (Система кодов)

**CodeSystem** определяет набор кодов с их значениями. Думайте о нём как о словаре медицинских кодов.

**Пример:** CodeSystem [`position-and-profession-cs`](https://dhp.uz/fhir/core/en/CodeSystem-position-and-profession-cs.html) содержит коды для медицинских профессий:
- Код `2211.1` означает "Врач общей практики"
- Код `2212` означает "Врач-специалист"
- Код `3221` означает "Медсестра"

Ключевые элементы:
- **url**: Канонический идентификатор, который никогда не меняется (например, `https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs`)
- **version**: Бизнес-версия (например, `1.0.0`)
- **concept**: Массив кодов с их свойствами
- **property**: Дополнительная информация о кодах (например, статус, родительский код)
- **content**: Указывает, присутствуют ли все коды (`complete`) или нет (`not-present`)

### ValueSet (Набор значений)

**ValueSet** — это выборка кодов из одной или нескольких CodeSystem для конкретной цели. В то время как CodeSystem определяет все возможные коды, ValueSet определяет, какие коды разрешены в определённом контексте.

**Пример:** ValueSet [`position-and-profession-vs`](https://dhp.uz/fhir/core/en/ValueSet-position-and-profession-vs.html) может включать только коды лицензированных медицинских работников, исключая административный персонал.

Ключевые элементы:
- **url**: Канонический идентификатор
- **version**: Бизнес-версия
- **compose**: Определяет, как построен ValueSet
  - **include**: Какие коды включить и из каких CodeSystem
  - **exclude**: Какие коды исключить
  - **filter**: Правила для выбора кодов
- **expansion**: Фактический список кодов (может генерироваться по требованию)

**Типичные случаи использования:**
- Заполнение выпадающих списков в формах
- Валидация пользовательского ввода
- Определение допустимых значений для кодированных полей в профилях

### ConceptMap (Карта концепций)

**ConceptMap** определяет отображения между кодами в разных CodeSystem. Это необходимо, когда нужно транслировать данные между различными системами кодирования.

**Пример:** ConceptMap [`iso-3166-alpha3-to-alpha2-cs`](https://dhp.uz/fhir/core/en/ConceptMap-iso-3166-alpha3-to-alpha2-cs.html) переводит между 3-буквенными и 2-буквенными кодами стран ISO:
- `UZB` (3-буквенный код) → `UZ` (2-буквенный код)
- `ABW` (Аруба 3-буквенный) → `AW` (Аруба 2-буквенный)

Ключевые элементы:
- **sourceCanonical**: URL исходной CodeSystem или ValueSet
- **targetCanonical**: URL целевой CodeSystem или ValueSet
- **group**: Содержит фактические отображения
  - **element**: Индивидуальные отображения кодов
  - **equivalence**: Тип отображения (эквивалентное, шире, уже и т.д.)

**Типичные случаи использования:**
- Конвертация данных при обмене с международными системами
- Одновременная поддержка нескольких стандартов кодирования
- Миграция со старых систем кодов на новые

### Управление версиями

Каждый ресурс терминологии может иметь несколько версий. Понимание версий критически важно для:
- **Согласованности**: Обеспечение того, что один и тот же код означает одно и то же со временем
- **Соответствия**: Некоторые регуляции требуют конкретные версии
- **Совместимости**: Разные системы могут использовать разные версии

Два типа версий:
1. **Бизнес-версия** (элемент `version`): Семантическая версия, например `1.0.0`, `2.1.0`
2. **Техническая версия** (`meta.versionId`): Присвоенная сервером версия для каждого обновления ресурса

**Лучшая практика:** Всегда указывайте версию в продакшн-системах для обеспечения согласованного значения кодов.

## Операции чтения

### Чтение CodeSystem

- HTTP метод: GET
- Endpoint: `/CodeSystem?url=[canonical-url]`

Получение конкретного CodeSystem по его каноническому URL. Это рекомендуемый подход, так как канонические URL являются глобально уникальными идентификаторами, которые остаются стабильными на разных серверах.

Пример:
```
GET /CodeSystem?url=https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs
```

Ответ: HTTP 200 OK с Bundle, содержащим ресурс CodeSystem в `entry[0].resource`.

**Понимание ответа:**

Ответ представляет собой Bundle с ресурсом CodeSystem в `entry[0].resource`:

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

### Чтение ValueSet

- HTTP метод: GET
- Endpoint: `/ValueSet?url=[canonical-url]`

Получение конкретного ValueSet по его каноническому URL. Это рекомендуемый подход, так как канонические URL являются глобально уникальными идентификаторами, которые остаются стабильными на разных серверах.

Пример:
```
GET /ValueSet?url=https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs
```

Ответ: HTTP 200 OK с Bundle, содержащим ресурс ValueSet в `entry[0].resource`.

**Понимание ответа:**

Ответ представляет собой Bundle с ресурсом ValueSet в `entry[0].resource`:

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

**Примечание:** Ответ показывает, как определён ValueSet (compose), но может не содержать фактический список кодов. Чтобы получить коды, используйте операцию `$expand` (см. ниже).

### Чтение ConceptMap

- HTTP метод: GET
- Endpoint: `/ConceptMap?url=[canonical-url]`

Получение конкретного ConceptMap по его каноническому URL. Это рекомендуемый подход, так как канонические URL являются глобально уникальными идентификаторами, которые остаются стабильными на разных серверах.

Пример:
```
GET /ConceptMap?url=https://terminology.dhp.uz/fhir/core/ConceptMap/iso-3166-alpha3-to-alpha2-cs
```

Ответ: HTTP 200 OK с Bundle, содержащим ресурс ConceptMap, показывающий отображения между системами кодов в `entry[0].resource`.

## Операции поиска

- HTTP метод: GET
- Endpoint: `/CodeSystem?[параметры]`, `/ValueSet?[параметры]`, `/ConceptMap?[параметры]`

### Параметры поиска CodeSystem

| Параметр | Тип | Описание | Пример |
|----------|-----|----------|--------|
| `url` | uri | Поиск по каноническому URL | `?url=https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs` |
| `name` | string | Поиск по имени | `?name=position` |
| `title` | string | Поиск по заголовку | `?title=profession` |
| `status` | token | Фильтр по статусу | `?status=active` |
| `version` | token | Поиск по версии | `?version=0.3.0` |
| `publisher` | string | Поиск по издателю | `?publisher=Digital Health Platform` |
| `content` | token | Тип содержимого | `?content=complete` |
| `system` | uri | Поиск конкретной системы | `?system=http://snomed.info/sct` |

### Параметры поиска ValueSet

| Параметр | Тип | Описание | Пример |
|----------|-----|----------|--------|
| `url` | uri | Поиск по каноническому URL | `?url=https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs` |
| `name` | string | Поиск по имени | `?name=position` |
| `title` | string | Поиск по заголовку | `?title=profession` |
| `status` | token | Фильтр по статусу | `?status=active` |
| `version` | token | Поиск по версии | `?version=0.3.0` |
| `publisher` | string | Поиск по издателю | `?publisher=Digital Health Platform` |
| `context` | token | Поиск по контексту использования | `?context=practitioner` |
| `expansion` | uri | Поиск по идентификатору расширения | `?expansion=urn:uuid:...` |

### Параметры поиска ConceptMap

| Параметр | Тип | Описание | Пример |
|----------|-----|----------|--------|
| `url` | uri | Поиск по каноническому URL | `?url=https://terminology.dhp.uz/fhir/core/ConceptMap/iso-3166-alpha3-to-alpha2-cs` |
| `name` | string | Поиск по имени | `?name=iso` |
| `status` | token | Фильтр по статусу | `?status=active` |
| `title` | string | Поиск по заголовку | `?title=alpha` |
| `publisher` | string | Поиск по издателю | `?publisher=Uzinfocom` |
| `source-scope-uri` | uri | Исходная система или ValueSet | `?source-scope-uri=urn:iso:std:iso:3166` |
| `target-scope-uri` | uri | Целевая система или ValueSet | `?target-scope-uri=urn:iso:std:iso:3166` |

### Типичные шаблоны поиска

**Найти все CodeSystem в системе:**
```
GET /CodeSystem?_summary=true&_count=20
```

**Найти CodeSystem по издателю:**
```
GET /CodeSystem?publisher=Health Level Seven
```

**Найти активные ValueSet:**
```
GET /ValueSet?status=active
```

**Найти ConceptMap для кодов стран ISO 3166:**
```
GET /ConceptMap?source-scope-uri=urn:iso:std:iso:3166
```

### Пагинация

Результаты поиска возвращаются в Bundle с пагинацией (20 записей на страницу). Используйте `Bundle.link` с `relation="next"` для получения следующей страницы.

## Операции терминологии

FHIR определяет несколько операций специально для работы с терминологией. Эти операции необходимы для создания приложений, использующих кодированные данные.

### Операция $expand

Операция `$expand` расширяет ValueSet, возвращая фактический список кодов. Это наиболее часто используемая операция терминологии.

**Когда использовать:**
- Построение выпадающих списков или элементов управления выбором
- Получение всех допустимых кодов для поля
- Проверка доступных кодов

**Endpoint:** `/ValueSet/$expand` или `/ValueSet/[id]/$expand`

**Параметры:**
- `url`: Канонический URL ValueSet (обязателен, если не используется ID)
- `valueSetVersion`: Конкретная версия для расширения
- `count`: Максимальное количество возвращаемых кодов
- `offset`: Смещение для пагинации
- `filter`: Текстовый фильтр для сопоставления отображаемых имён кодов

**Пример 1: Базовое расширение**
```
GET /ValueSet/$expand?url=https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs
```

Ответ:
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

**Пример 2: Расширение с ограничением количества**
```
GET /ValueSet/$expand?url=https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs&count=10
```

Это возвращает только первые 10 кодов.

**Пример 3: Расширение по ID**
```
GET /ValueSet/position-and-profession-vs/$expand
```

### Операция $validate-code

Операция `$validate-code` проверяет, является ли код валидным в ValueSet. Это необходимо для валидации данных.

**Когда использовать:**
- Валидация пользовательского ввода перед сохранением
- Проверка валидности кодов в полученных данных
- Обеспечение качества данных

**Endpoint:** `/ValueSet/$validate-code` или `/ValueSet/[id]/$validate-code`

**Параметры:**
- `url`: Канонический URL ValueSet (обязателен, если не используется ID)
- `code`: Код для валидации (обязателен)
- `system`: Система, из которой происходит код (обязательна)
- `display`: Строка отображения (опционально, также может быть валидирована)
- `valueSetVersion`: Конкретная версия для валидации

**Пример 1: Валидный код**
```
GET /ValueSet/$validate-code?url=https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs&code=2211.1&system=https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs
```

Ответ:
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

**Пример 2: Невалидный код**
```
GET /ValueSet/$validate-code?url=https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs&code=INVALID&system=https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs
```

Ответ:
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

### Операция $lookup

Операция `$lookup` получает детали о конкретном коде в CodeSystem.

**Когда использовать:**
- Получение отображаемого имени для кода
- Извлечение определения и свойств кода
- Показ детальной информации о выбранных кодах

**Endpoint:** `/CodeSystem/$lookup`

**Параметры:**
- `system`: URL CodeSystem (обязателен)
- `code`: Код для поиска (обязателен)
- `version`: Конкретная версия CodeSystem

**Пример:**
```
GET /CodeSystem/$lookup?system=https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs&code=2211.1
```

Ответ:
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

## Управление версиями на практике

### Понимание элементов версии

Каждый ресурс терминологии имеет два идентификатора версии:

1. **Бизнес-версия** (элемент `version`):
   - Семантическая версия (например, `1.0.0`, `2.1.0`)
   - Устанавливается автором терминологии
   - Указывает версию содержимого
   - Должна быть указана при использовании терминологии в продакшн

2. **Техническая версия** (`meta.versionId`):
   - Присвоенная сервером версия (например, `1`, `2`, `3`)
   - Изменяется с каждым обновлением ресурса
   - Используется для оптимистичной блокировки (заголовок If-Match)
   - Обычно не используется для выбора версии

### Поиск по версии

**Получить конкретную версию:**
```
GET /CodeSystem?url=https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs&version=0.3.0
```

### Использование версий в операциях

**Расширить конкретную версию ValueSet:**
```
GET /ValueSet/$expand?url=https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs&valueSetVersion=0.3.0
```

**Валидировать против конкретной версии:**
```
GET /ValueSet/$validate-code?url=https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs&valueSetVersion=0.3.0&code=2211.1&system=https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs
```

**Искать в конкретной версии:**
```
GET /CodeSystem/$lookup?system=https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs&version=0.3.0&code=2211.1
```

## Работа с ConceptMap

ConceptMap позволяет транслировать между различными системами кодирования. Это необходимо при интеграции с системами, использующими разные терминологии.

### Когда нужны ConceptMap?

- Обмен данными с международными системами (например, отображение UZ кодов на SNOMED или LOINC)
- Одновременная поддержка нескольких стандартов кодирования
- Миграция со старых систем кодов на новые
- Создание отчётов, агрегирующих данные из разных систем кодирования

### Поиск релевантных ConceptMap

**Найти все доступные ConceptMap:**
```
GET /ConceptMap?status=active
```

**Найти ConceptMap для конкретной исходной системы:**
```
GET /ConceptMap?source-uri=https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs
```

**Найти ConceptMap для кодов стран ISO 3166:**
```
GET /ConceptMap?source-scope-uri=urn:iso:std:iso:3166
```

### Использование операции $translate

Операция `$translate` транслирует код из одной системы в другую с использованием ConceptMap.

**Endpoint:** `/ConceptMap/$translate` или `/ConceptMap/[id]/$translate`

**Параметры:**
- `url`: Канонический URL ConceptMap
- `source`: Исходный ValueSet (опционально)
- `system`: URL исходной CodeSystem (обязателен)
- `code`: Код для трансляции (обязателен)
- `target`: Целевой ValueSet или CodeSystem
- `reverse`: Обратная трансляция (использовать цель как источник)

**Пример: Транслировать код страны ISO 3166**

Используя GET:
```
GET /ConceptMap/$translate?url=https://terminology.dhp.uz/fhir/core/ConceptMap/iso-3166-alpha3-to-alpha2-cs&system=urn:iso:std:iso:3166&code=UZB&target=urn:iso:std:iso:3166
```

Используя POST (рекомендуется для сложных запросов):
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

Ответ:
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

## Практический workflow интеграции

Давайте рассмотрим полный сценарий: создание формы регистрации врача, которая правильно использует терминологию.

### Сценарий: Форма регистрации врача

**Требования:**
- Пользователь должен выбрать свою лицензию/сертификат из выпадающего списка
- Только валидные сертификаты должны быть доступны для выбора
- Отображение должно показывать название сертификата на языке пользователя

**Ресурсы, используемые в этом сценарии:**
- [Набор значений лицензий, сертификатов и степеней](https://dhp.uz/fhir/core/en/ValueSet-license-certificate-vs.html)

**Шаг 1: Найти соответствующий ValueSet**

Сначала определите, какой ValueSet определяет допустимые сертификаты, просмотрев [страницу артефактов терминологии uz-core](https://dhp.uz/fhir/core/en/artifacts.html#4).

Со страницы артефактов получаем URL ValueSet: `https://terminology.dhp.uz/fhir/core/ValueSet/license-certificate-vs`

**Шаг 2: Расширить ValueSet для заполнения выпадающего списка**

```
GET /ValueSet/$expand?url=https://terminology.dhp.uz/fhir/core/ValueSet/license-certificate-vs&count=100
```

Ответ даёт нам все коды для заполнения выпадающего списка:
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

**Шаг 3: Пользователь выбирает сертификат**

Пользователь выбирает "Doctor of Medicine" (код: `MD`)

**Шаг 4: Искать отображаемые имена для других языков (опционально)**

Если нужно показать сертификат на нескольких языках:

```
GET /CodeSystem/$lookup?system=http://terminology.hl7.org/CodeSystem/v2-0360&code=MD
```

Это возвращает все доступные обозначения (переводы).

**Шаг 5: Сохранить в ресурсе Practitioner**

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

### Советы по реализации

1. **Кэшируйте результаты расширения**: Расширение ValueSet может быть медленным. Кэшируйте результаты и обновляйте периодически или при изменении версий.

2. **Обрабатывайте пагинацию**: Если ValueSet большой, расширение может быть пагинированным. Реализуйте правильную обработку пагинации.

3. **Используйте привязку версий**: В продакшн привязывайтесь к конкретным версиям ValueSet для обеспечения согласованности.

4. **Обрабатывайте отсутствующие коды gracefully**: Если код не найден во время поиска, обработайте это gracefully, а не падайте с ошибкой.

## Обработка ошибок

### Типичные ошибки и как их обрабатывать

**Ошибка 1: Код не найден в ValueSet**

Запрос:
```
GET /ValueSet/$validate-code?url=https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs&code=INVALID&system=https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs
```

Ответ:
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

**Обработка:** Показать пользователю понятное сообщение об ошибке и попросить выбрать валидный код из списка.

**Ошибка 2: ValueSet не найден**

Запрос:
```
GET /ValueSet/$expand?url=https://terminology.dhp.uz/fhir/core/ValueSet/nonexistent-vs
```

Ответ:
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

**Обработка:** Проверьте URL ValueSet на опечатки. Убедитесь, что ValueSet существует на сервере. Используйте поиск для нахождения доступных ValueSet.

**Ошибка 3: Версия не найдена**

Запрос:
```
GET /CodeSystem?url=https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs&version=99.99.99
```

Ответ:
```json
{
  "resourceType": "Bundle",
  "type": "searchset",
  "total": 0,
  "entry": []
}
```

**Обработка:** Проверьте номер версии. Ищите без версии, чтобы найти доступные версии. Рассмотрите возможность откатиться к последней версии, если конкретная версия не найдена.

**Ошибка 4: Расширение слишком большое**

Запрос:
```
GET /ValueSet/$expand?url=http://hl7.org/fhir/ValueSet/all-languages
```

Ответ:
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

**Обработка:** Используйте параметры `count` и `offset` для пагинации по большим расширениям. Рассмотрите использование фильтров для сужения результатов.

**Ошибка 5: Неверная система**

Запрос:
```
GET /ValueSet/$validate-code?url=https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs&code=2211.1&system=http://wrong-system.com
```

Ответ:
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

**Обработка:** Убедитесь, что используете правильный URL CodeSystem. Система должна соответствовать одной из систем, включённых в ValueSet.

### Коды ответов

| Код | Описание |
|-----|----------|
| 200 | OK - успешная операция |
| 400 | Bad Request - неверные параметры |
| 404 | Not Found - ресурс не найден |
| 410 | Gone - ресурс был удалён |
| 422 | Unprocessable Entity - операция не может быть обработана |
| 500 | Internal Server Error - ошибка сервера |

## Прогрессивные упражнения для обучения

Выполняйте эти упражнения по порядку, от базовых к продвинутым.

### Упражнения для начинающих

**Упражнение 1: Прочитать CodeSystem**

Задача: Получить CodeSystem position-and-profession и изучить её структуру.

```
GET /CodeSystem/position-and-profession-cs
```

Вопросы для изучения:
- Сколько концептов определено?
- Каков номер версии?
- Полное или частичное содержимое?

**Упражнение 2: Поиск ValueSet**

Задача: Найти все ValueSet, доступные в системе.

```
GET /ValueSet?_summary=true&_count=20
```

Вопросы для изучения:
- Сколько всего ValueSet?
- Какие из них относятся к врачам?
- Какие узбекские, а какие международные?

**Упражнение 3: Расширить простой ValueSet**

Задача: Расширить ValueSet gender-other, чтобы увидеть все возможные значения.

```
GET /ValueSet/$expand?url=https://terminology.dhp.uz/fhir/core/ValueSet/gender-other-vs
```

Вопросы для изучения:
- Сколько кодов в этом ValueSet?
- Что означают разные коды?

**Упражнение 4: Валидировать код**

Задача: Проверить, валиден ли код "2211.1" в ValueSet position-and-profession.

```
GET /ValueSet/$validate-code?url=https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs&code=2211.1&system=https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs
```

Вопросы для изучения:
- Валиден ли код?
- Какое отображаемое имя возвращается?
- Попробуйте с невалидным кодом типа "INVALID" - что происходит?

### Упражнения среднего уровня

**Упражнение 5: Поиск ValueSet по контексту**

Задача: Найти все ValueSet, используемые в контексте врачей.

```
GET /ValueSet?context=practitioner
```

Вопросы для изучения:
- Какие ValueSet специфичны для врачей?
- Можете ли вы найти ValueSet для специализаций врачей?

**Упражнение 6: Использовать $lookup для получения деталей кода**

Задача: Найти детальную информацию о коде "2211.1".

```
GET /CodeSystem/$lookup?system=https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs&code=2211.1
```

Вопросы для изучения:
- Какие обозначения (переводы) доступны?
- Есть ли определение для кода?
- Определены ли какие-либо свойства?

**Упражнение 7: Работа с версиями**

Задача: Найти все версии CodeSystem position-and-profession.

```
GET /CodeSystem?url=https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs&_sort=-version
```

Вопросы для изучения:
- Сколько версий существует?
- Какая последняя версия?
- Попробуйте расширить ValueSet с конкретной версией - работает ли это?

**Упражнение 8: Использовать фильтры в расширении**

Задача: Расширить ValueSet position-and-profession, но отфильтровать, чтобы показать только коды, содержащие "nurse".

```
GET /ValueSet/$expand?url=https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs&filter=nurse
```

Вопросы для изучения:
- Сколько кодов соответствует фильтру?
- Попробуйте разные термины фильтра - какие результаты получаете?
- Попробуйте комбинировать filter с параметром `count`

### Продвинутые упражнения

**Упражнение 9: Найти и использовать ConceptMap**

Задача: Найти ConceptMap, которая отображает между узбекскими кодами и международной терминологией.

```
GET /ConceptMap?source-uri:contains=terminology.dhp.uz
```

Затем транслировать код:
```
GET /ConceptMap/$translate?url=[url-from-search]&system=[source-system]&code=[code]
```

Вопросы для изучения:
- Какие ConceptMap доступны?
- Можете ли вы успешно транслировать код?
- Какие типы эквивалентности используются в отображениях?

**Упражнение 10: Построить форму с поддержкой терминологии**

Задача: Спроектировать и реализовать полный flow для кодированного поля:

1. Поиск подходящего ValueSet
2. Расширить его для получения кодов для выпадающего списка
3. Валидировать выбор пользователя
4. Искать отображаемые имена на нескольких языках
5. Сохранить кодированные данные в ресурсе FHIR

Вопросы для изучения:
- Как обрабатывать большие ValueSet (>100 кодов)?
- Как эффективно кэшировать результаты расширения?
- Как обрабатывать ошибки на каждом шаге?

## Полезные ссылки

**Документация FHIR:**
- [FHIR Terminology Service](http://hl7.org/fhir/R5/terminology-service.html)
- [FHIR CodeSystem Resource](http://hl7.org/fhir/R5/codesystem.html)
- [FHIR ValueSet Resource](http://hl7.org/fhir/R5/valueset.html)
- [FHIR ConceptMap Resource](http://hl7.org/fhir/R5/conceptmap.html)

**Узбекская терминология:**
- [Система кодов должностей и профессий](https://dhp.uz/fhir/core/en/CodeSystem-position-and-profession-cs.html) - Медицинские должности и профессии
- [Набор значений должностей и профессий](https://dhp.uz/fhir/core/en/ValueSet-position-and-profession-vs.html) - Допустимые медицинские профессии
- [uz-core Артефакты](https://dhp.uz/fhir/core/en/artifacts.html) - Все ресурсы терминологии uz-core
- [DHPCapabilityStatement](https://dhp.uz/fhir/core/en/CapabilityStatement-DHPCapabilityStatement.html)

---

## Примеры кода

{% include code-tabs-style.html %}

Ниже приведены примеры расширения ValueSet и валидации кода на различных языках программирования:

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
<pre><code class="language-bash"># Расширить ValueSet
curl -X GET "https://playground.dhp.uz/fhir/ValueSet/\$expand?url=https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs" \
  -H "Accept: application/fhir+json"

# Валидировать код
curl -X GET "https://playground.dhp.uz/fhir/ValueSet/\$validate-code?url=https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs&code=2211.1&system=https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs" \
  -H "Accept: application/fhir+json"

# Искать код
curl -X GET "https://playground.dhp.uz/fhir/CodeSystem/\$lookup?system=https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs&code=2211.1" \
  -H "Accept: application/fhir+json"
</code></pre>
    </div>
    <div class="tab-pane" id="python">
<pre><code class="language-python">import requests
from typing import List, Dict

# Базовый URL FHIR сервера
base_url = "https://playground.dhp.uz/fhir"

def expand_valueset(valueset_url: str) -> List[Dict]:
    """Расширить ValueSet для получения всех кодов."""
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
    """Валидировать, находится ли код в ValueSet."""
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
    """Искать детали о коде."""
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

# Пример использования
valueset_url = "https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs"
codesystem_url = "https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs"

# Расширить ValueSet
print("Расширение ValueSet...")
codes = expand_valueset(valueset_url)
for code in codes[:5]:  # Показать первые 5
    print(f"  {code['code']}: {code['display']}")

# Валидировать код
print("\nВалидация кода '2211.1'...")
is_valid = validate_code(valueset_url, "2211.1", codesystem_url)
print(f"  Валиден: {is_valid}")

# Искать детали кода
print("\nПоиск кода '2211.1'...")
details = lookup_code(codesystem_url, "2211.1")
print(f"  Детали: {details}")
</code></pre>
    </div>
    <div class="tab-pane" id="javascript">
<pre><code class="language-javascript">// Используя fetch API
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

// Пример использования
const valueSetUrl = "https://terminology.dhp.uz/fhir/core/ValueSet/position-and-profession-vs";
const codeSystemUrl = "https://terminology.dhp.uz/fhir/core/CodeSystem/position-and-profession-cs";

(async () => {
  // Расширить ValueSet
  console.log("Расширение ValueSet...");
  const codes = await expandValueSet(valueSetUrl);
  codes.slice(0, 5).forEach(code => {
    console.log(`  ${code.code}: ${code.display}`);
  });

  // Валидировать код
  console.log("\nВалидация кода '2211.1'...");
  const isValid = await validateCode(valueSetUrl, "2211.1", codeSystemUrl);
  console.log(`  Валиден: ${isValid}`);

  // Искать детали кода
  console.log("\nПоиск кода '2211.1'...");
  const details = await lookupCode(codeSystemUrl, "2211.1");
  console.log("  Детали:", details);
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
        // Создать параметры для операции $expand
        Parameters params = new Parameters();
        params.addParameter("url", new UriType(valueSetUrl));

        // Выполнить операцию $expand
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
        // Создать параметры для операции $validate-code
        Parameters params = new Parameters();
        params.addParameter("url", new UriType(valueSetUrl));
        params.addParameter("code", new CodeType(code));
        params.addParameter("system", new UriType(system));

        // Выполнить операцию $validate-code
        Parameters result = client
            .operation()
            .onType(ValueSet.class)
            .named("$validate-code")
            .withParameters(params)
            .returnResourceType(Parameters.class)
            .execute();

        // Извлечь результат
        for (Parameters.ParametersParameterComponent param : result.getParameter()) {
            if ("result".equals(param.getName())) {
                return param.getValue() instanceof BooleanType &&
                       ((BooleanType) param.getValue()).booleanValue();
            }
        }

        return false;
    }

    public static Parameters lookupCode(String system, String code) {
        // Создать параметры для операции $lookup
        Parameters params = new Parameters();
        params.addParameter("system", new UriType(system));
        params.addParameter("code", new CodeType(code));

        // Выполнить операцию $lookup
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

        // Расширить ValueSet
        System.out.println("Расширение ValueSet...");
        List&lt;ValueSet.ValueSetExpansionContainsComponent&gt; codes = expandValueSet(valueSetUrl);
        codes.stream().limit(5).forEach(code ->
            System.out.println("  " + code.getCode() + ": " + code.getDisplay())
        );

        // Валидировать код
        System.out.println("\nВалидация кода '2211.1'...");
        boolean isValid = validateCode(valueSetUrl, "2211.1", codeSystemUrl);
        System.out.println("  Валиден: " + isValid);

        // Искать детали кода
        System.out.println("\nПоиск кода '2211.1'...");
        Parameters details = lookupCode(codeSystemUrl, "2211.1");
        System.out.println("  Детали: " + ctx.newJsonParser().encodeResourceToString(details));
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

        // Расширить ValueSet
        Console.WriteLine("Расширение ValueSet...");
        var codes = ExpandValueSet(valueSetUrl);
        foreach (var code in codes.Take(5))
        {
            Console.WriteLine($"  {code.Code}: {code.Display}");
        }

        // Валидировать код
        Console.WriteLine("\nВалидация кода '2211.1'...");
        var isValid = ValidateCode(valueSetUrl, "2211.1", codeSystemUrl);
        Console.WriteLine($"  Валиден: {isValid}");

        // Искать детали кода
        Console.WriteLine("\nПоиск кода '2211.1'...");
        var details = LookupCode(codeSystemUrl, "2211.1");
        Console.WriteLine("  Детали успешно получены");
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

type Contains struct {
    System  string `json:"system"`
    Code    string `json:"code"`
    Display string `json:"display"`
}

type ValueSetExpansion struct {
    Contains []Contains `json:"contains"`
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

func expandValueSet(valueSetURL string) ([]Contains, error) {
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

    // Расширить ValueSet
    fmt.Println("Расширение ValueSet...")
    codes, err := expandValueSet(valueSetURL)
    if err != nil {
        fmt.Printf("Ошибка: %v\n", err)
        return
    }

    for i, code := range codes {
        if i >= 5 {
            break
        }
        fmt.Printf("  %s: %s\n", code.Code, code.Display)
    }

    // Валидировать код
    fmt.Println("\nВалидация кода '2211.1'...")
    isValid, err := validateCode(valueSetURL, "2211.1", codeSystemURL)
    if err != nil {
        fmt.Printf("Ошибка: %v\n", err)
        return
    }
    fmt.Printf("  Валиден: %v\n", isValid)

    // Искать детали кода
    fmt.Println("\nПоиск кода '2211.1'...")
    details, err := lookupCode(codeSystemURL, "2211.1")
    if err != nil {
        fmt.Printf("Ошибка: %v\n", err)
        return
    }
    fmt.Println("  Детали успешно получены")
    _ = details // Использовать детали по необходимости
}
</code></pre>
    </div>
  </div>
</div>
