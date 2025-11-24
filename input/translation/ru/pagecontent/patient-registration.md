# Регистрация пациентов

## Обзор

Цель: Создание записей пациентов с соответствующими идентификаторами (ПИНФЛ), поиск и сопоставление пациентов, обработка дубликатов.

- Ресурсы: Patient
- Навыки: Поиск и сопоставление, логика обнаружения дубликатов
- Базовый URL: `https://playground.dhp.uz/fhir`
  - **Примечание:** Это временный URL, который будет заменён на финальный ближе к коннектафону
- Профиль: [uz-core-patient](https://dhp.uz/fhir/core/en/StructureDefinition-uz-core-patient.html)

**Обратная связь:** Поделитесь своим опытом, проблемами и успехами в [документе коннектафона](https://docs.google.com/document/d/1PdQ8zBI9xkISP3tAqIK8-TGMql3kVVZ4UNoHVYqCy4Y/edit?usp=sharing).

## Профиль uz-core-patient

**Примечание**: В настоящее время валидация на сервере отключена, но ожидается, что она будет включена к коннектафону. Клиентские приложения должны следовать правилам профиля для обеспечения совместимости и качества данных.

### Обязательные элементы

В этом профиле нет обязательных элементов с минимальной кардинальностью больше 0. Все элементы являются опциональными, хотя Must Support элементы должны быть заполнены, когда данные доступны.

### Must-Support элементы

UZ Core профили: Элементы, отмеченные как Must Support, должны быть заполнены при обмене данными между системами, работающими в Узбекистане.

Когда данные не могут быть заполнены, потому что они недоступны в исходной системе, элемент может остаться пустым — при условии, что правила кардинальности это позволяют. Однако, когда требования кардинальности обязывают включение, системы должны использовать расширение Data Absent Reason, а не оставлять элемент пустым.

#### Элементы профиля

- **identifier**: Идентификаторы пациента
  - **pinfl**: Персональный идентификационный номер (ПИНФЛ) - национальный идентификатор (`system`: `https://dhp.uz/fhir/core/sid/pid/uz/ni`)
- **active**: Активна ли данная запись пациента
- **name**: Имя пациента
  - **use**: Использование имени (official, usual и т.д.)
  - **text**: Полное имя как оно отображается
  - **family**: Фамилия
  - **given**: Имена
  - **suffix**: Суффикс имени
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
- **address**: Адреса пациента двух типов:
  - **uzAddress**: Адреса в Узбекистане (код страны "UZ") с поддержкой махалли. **Необходимо использовать кодированные значения** из официальных реестров для административных подразделений: [state](https://dhp.uz/fhir/core/en/ValueSet-state-vs.html), [district](https://dhp.uz/fhir/core/en/ValueSet-regions-vs.html), [city/mahalla](https://dhp.uz/fhir/core/en/ValueSet-mahalla-vs.html)
  - **i18nAddress**: Международные адреса (не Узбекистан). Административные подразделения используют свободный текст без обязательных наборов значений
- **maritalStatus**: Семейное положение (married, single, divorced и т.д.)
- **multipleBirth[x]**: Является ли пациент частью многоплодных родов
- **photo**: Фотография пациента
- **contact**: Контактное лицо (экстренный контакт, член семьи и т.д.)
- **communication**: Языки для общения
  - **language**: Код языка (uz, ru, kaa и т.д.)
  - **preferred**: Предпочитаемый язык для общения
- **generalPractitioner**: Назначенный основной врач пациента
- **managingOrganization**: Организация, которая является хранителем записи пациента
- **link**: Ссылка на другой ресурс Patient (для разрешения дубликатов)

### Дифференциация пола

Когда пол пациента установлен как "other", профиль требует расширение `gender-other`:

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

Для адресов в Узбекистане необходимо использовать кодированные значения из официальных реестров:
- Поле `state` должно использовать коды из [state valueset](https://dhp.uz/fhir/core/en/ValueSet-state-vs.html)
- Поле `district` должно использовать коды из [regions valueset](https://dhp.uz/fhir/core/en/ValueSet-regions-vs.html)
- Поле `city` должно использовать коды из [mahalla valueset](https://dhp.uz/fhir/core/en/ValueSet-mahalla-vs.html)

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

## CRUD операции

### Create Patient (Создание)

- HTTP метод: POST
- Endpoint: `/Patient`
- Заголовки: `Content-Type: application/fhir+json`

Создание нового пациента. Сервер присваивает уникальный ID и возвращает Location header.

Минимальный пример:
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
      "family": "Каримов",
      "given": ["Алишер", "Акбарович"]
    }
  ],
  "gender": "male",
  "birthDate": "1985-05-15"
}
```

Ответ: HTTP 201 Created с Location header и созданным ресурсом.

### Read Patient (Чтение)

- HTTP метод: GET
- Endpoint: `/Patient/[id]`

Получение конкретного пациента по ID.

Ответ: HTTP 200 OK с ресурсом Patient или HTTP 404 Not Found.

### Update Patient (Обновление)

- HTTP метод: PUT
- Endpoint: `/Patient/[id]`
- Заголовки:
  - `Content-Type: application/fhir+json`
  - `If-Match: W/"[versionId]"` (обязательно для предотвращения конфликтов)

Полное обновление пациента. Необходимо отправить весь ресурс, включая элемент `id`. Заголовок `If-Match` обязателен и должен содержать версию ресурса из элемента `meta.versionId` для предотвращения конфликтов при одновременном редактировании (оптимистичная блокировка).

Пример запроса:
```
PUT /Patient/existing-id
If-Match: W/"2"
Content-Type: application/fhir+json
```

Пример тела запроса:
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
      "family": "Каримов",
      "given": ["Алишер", "Акбарович"]
    }
  ],
  "gender": "male",
  "birthDate": "1985-05-15"
}
```

Ответ: HTTP 200 OK с обновлённым ресурсом.

### Delete Patient (Удаление)

- HTTP метод: DELETE
- Endpoint: `/Patient/[id]`

Удаление пациента.

Ответ: HTTP 200 OK с OperationOutcome при успешном удалении. При попытке прочитать удалённый ресурс сервер вернёт HTTP 410 Gone.

## Операции поиска

- HTTP метод: GET
- Endpoint: `/Patient?[параметры]`

Все поддерживаемые параметры поиска можно найти в capability statement по адресу [DHPCapabilityStatement](https://dhp.uz/fhir/core/en/CapabilityStatement-DHPCapabilityStatement.html) или запросив endpoint [/metadata](https://playground.dhp.uz/fhir/metadata).

### Параметры поиска

| Параметр | Тип | Описание | Пример |
|----------|-----|----------|--------|
| `_id` | token | Поиск по ID | `?_id=123` |
| `identifier` | token | Поиск по идентификатору | `?identifier=https://dhp.uz/fhir/core/sid/pid/uz/ni\|12345678901234` |
| `name` | string | Поиск по имени (частичное совпадение) | `?name=Каримов` |
| `given` | string | Поиск по имени | `?given=Алишер` |
| `family` | string | Поиск по фамилии | `?family=Каримов` |
| `telecom` | token | Поиск по контактным данным | `?telecom=%2B998901234567` |
| `phone` | token | Поиск по номеру телефона | `?phone=%2B998901234567` |
| `email` | token | Поиск по email | `?email=patient@example.com` |
| `address` | string | Поиск по адресу | `?address=Toshkent` |
| `address-city` | string | Поиск по городу | `?address-city=Toshkent` |
| `address-country` | string | Поиск по стране | `?address-country=UZ` |
| `address-postalcode` | string | Поиск по почтовому индексу | `?address-postalcode=100084` |
| `address-state` | string | Поиск по региону | `?address-state=Toshkent` |
| `gender` | token | Поиск по полу | `?gender=male` |
| `birthdate` | date | Поиск по дате рождения | `?birthdate=1985-05-15` |
| `active` | token | Фильтр по статусу | `?active=true` |
| `deceased` | token | Фильтр по статусу смерти | `?deceased=false` |
| `organization` | reference | Поиск по управляющей организации | `?organization=Organization/123` |
| `general-practitioner` | reference | Поиск по основному врачу | `?general-practitioner=Practitioner/456` |

### Распространённые шаблоны поиска

**Найти пациента по ПИНФЛ:**
```
GET /Patient?identifier=https://dhp.uz/fhir/core/sid/pid/uz/ni|12345678901234
```

**Найти пациентов по имени:**
```
GET /Patient?name=Каримов
```

**Найти пациентов по номеру телефона:**
```
GET /Patient?phone=%2B998901234567
```

**Найти пациентов по дате рождения:**
```
GET /Patient?birthdate=1985-05-15
```

**Найти пациентов в определённом городе:**
```
GET /Patient?address-city=Toshkent&active=true
```

**Комбинировать несколько критериев поиска:**
```
GET /Patient?family=Каримов&birthdate=1985-05-15&gender=male
```

### Модификаторы и префиксы

Комбинирование параметров (логическое И):
```
GET /Patient?family=Каримов&address-city=Toshkent&active=true
```

Множественные значения (логическое ИЛИ):
```
GET /Patient?gender=male,female
```

Сравнения дат:
```
GET /Patient?birthdate=gt1980-01-01&birthdate=lt1990-12-31
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
      "url": "https://playground.dhp.uz/fhir/Patient?name=Каримов&_page=1"
    },
    {
      "relation": "next",
      "url": "https://playground.dhp.uz/fhir/Patient?name=Каримов&_page=2"
    }
  ],
  "entry": [...]
}
```

Используйте `Bundle.link` с `relation="next"` для получения следующей страницы.

**Известная проблема**: Поле `Bundle.total` может возвращать `0`, даже когда результаты присутствуют. Чтобы подсчитать пациентов на текущей странице, отфильтруйте `Bundle.entry` по `resourceType == "Patient"` (ответ может содержать ресурсы `OperationOutcome`).

## Сопоставление пациентов и обнаружение дубликатов

### Поиск перед созданием

Перед созданием нового пациента выполните поиск потенциальных совпадений, чтобы избежать дубликатов:

1. **Поиск по ПИНФЛ** (наиболее точное совпадение):
   ```
   GET /Patient?identifier=https://dhp.uz/fhir/core/sid/pid/uz/ni|12345678901234
   ```

2. **Поиск по демографическим данным**, если ПИНФЛ недоступен:
   ```
   GET /Patient?family=Каримов&given=Алишер&birthdate=1985-05-15
   ```

3. **Поиск по номеру телефона**:
   ```
   GET /Patient?phone=%2B998901234567
   ```

### Логика сопоставления

Реализуйте логику сопоставления на основе доступных данных:

**Критерии сильного совпадения** (вероятно, тот же пациент):
- Одинаковый ПИНФЛ
- Одинаковое полное имя + дата рождения + пол
- Одинаковый номер телефона + дата рождения + пол

**Критерии слабого совпадения** (возможный дубликат - требуется проверка):
- Похожее имя (нечёткое совпадение) + та же дата рождения
- Тот же номер телефона + похожая дата рождения
- Тот же адрес + похожее имя

### Обработка дубликатов с помощью Patient.link

Когда дубликаты идентифицированы, используйте элемент `link` для связывания ресурсов пациентов:

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
        "display": "Дубликат записи"
      },
      "type": "replaced-by"
    }
  ]
}
```

Типы связей:
- **replaced-by**: Эта запись заменена связанной записью
- **replaces**: Эта запись заменяет связанную запись
- **refer**: Эту запись следует рассматривать вместе со связанной записью
- **seealso**: Эта запись возможно относится к тому же пациенту, что и связанная запись

### Процесс разрешения дубликатов

1. **Идентифицировать потенциальные дубликаты** через поиск
2. **Проверить совпадения** вручную или с помощью бизнес-правил
3. **Выбрать основную запись** (обычно ту, которая содержит наиболее полные данные или была создана раньше)
4. **Обновить дублирующиеся записи**:
   - Установить `active: false` на дубликате
   - Добавить элемент `link`, указывающий на основную запись с типом "replaced-by"
5. **Опционально объединить данные** из дубликата в основную запись перед деактивацией

Пример отметки дубликата:
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
        "display": "Основная запись пациента"
      },
      "type": "replaced-by"
    }
  ]
}
```

## Обработка ошибок

### Коды ответов

| Код | Описание |
|-----|----------|
| 200 | OK - успешное получение/обновление/удаление |
| 201 | Created - успешное создание |
| 400 | Bad Request - неверный JSON |
| 404 | Not Found - ресурс не найден |
| 409 | Conflict - конфликт версий |
| 410 | Gone - ресурс был удалён |
| 412 | Precondition Failed - заголовок If-Match не предоставлен или несоответствие версий |
| 422 | Unprocessable Entity - ошибка валидации профиля |

### OperationOutcome

При ошибках сервер возвращает OperationOutcome:

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

## Полезные ссылки

- [FHIR Patient Resource](http://hl7.org/fhir/R5/patient.html)
- [uz-core-patient Profile](https://dhp.uz/fhir/core/en/StructureDefinition-uz-core-patient.html)
- [FHIR RESTful API](http://hl7.org/fhir/R5/http.html)
- [FHIR Search](http://hl7.org/fhir/R5/search.html)
- [Patient Matching](http://hl7.org/fhir/R5/patient.html#matching)

---

## Примеры кода

{% include code-tabs-style.html %}

Ниже приведены примеры создания и поиска пациентов на различных языках программирования:

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
<pre><code class="language-bash"># Поиск существующего пациента по ПИНФЛ перед созданием
curl "https://playground.dhp.uz/fhir/Patient?identifier=https://dhp.uz/fhir/core/sid/pid/uz/ni|12345678901234"

# Если не найден, создать нового пациента
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
      "family": "Каримов",
      "given": ["Алишер", "Акбарович"]
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

# Базовый URL FHIR сервера
base_url = "https://playground.dhp.uz/fhir"
pinfl = "12345678901234"

# Поиск существующего пациента по ПИНФЛ
search_url = f"{base_url}/Patient?identifier=https://dhp.uz/fhir/core/sid/pid/uz/ni|{pinfl}"
response = requests.get(search_url)

if response.status_code == 200:
    bundle = response.json()
    if bundle.get('total', 0) > 0:
        print(f"Пациент найден с ПИНФЛ {pinfl}")
        existing_patient = bundle['entry'][0]['resource']
        print(f"ID пациента: {existing_patient['id']}")
    else:
        print("Пациент не найден, создание нового пациента")

        # Создание нового пациента
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
                    family="Каримов",
                    given=["Алишер", "Акбарович"]
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

        # Отправка POST запроса
        create_response = requests.post(
            f"{base_url}/Patient",
            headers={"Content-Type": "application/fhir+json"},
            data=patient.json()
        )

        if create_response.status_code == 201:
            created_patient = create_response.json()
            print(f"Пациент создан с ID: {created_patient['id']}")
        else:
            print(f"Ошибка: {create_response.status_code}")
            print(create_response.text)
</code></pre>
    </div>
    <div class="tab-pane" id="javascript">
<pre><code class="language-javascript">// Использование fetch API
const baseUrl = "https://playground.dhp.uz/fhir";
const pinfl = "12345678901234";

// Поиск существующего пациента по ПИНФЛ
async function findOrCreatePatient() {
  try {
    // Поиск пациента
    const searchUrl = `${baseUrl}/Patient?identifier=https://dhp.uz/fhir/core/sid/pid/uz/ni|${pinfl}`;
    const searchResponse = await fetch(searchUrl);
    const bundle = await searchResponse.json();

    if (bundle.total && bundle.total > 0) {
      console.log(`Пациент найден с ПИНФЛ ${pinfl}`);
      console.log(`ID пациента: ${bundle.entry[0].resource.id}`);
      return bundle.entry[0].resource;
    }

    console.log("Пациент не найден, создание нового пациента");

    // Создание нового пациента
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
          family: "Каримов",
          given: ["Алишер", "Акбарович"]
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
      console.log(`Пациент создан с ID: ${data.id}`);
      return data;
    } else {
      throw new Error(`Ошибка: ${createResponse.status}`);
    }
  } catch (error) {
    console.error('Ошибка:', error);
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

// Создание FHIR контекста и клиента
FhirContext ctx = FhirContext.forR5();
IGenericClient client = ctx.newRestfulGenericClient("https://playground.dhp.uz/fhir");

String pinfl = "12345678901234";
String system = "https://dhp.uz/fhir/core/sid/pid/uz/ni";

// Поиск существующего пациента по ПИНФЛ
Bundle results = client.search()
    .forResource(Patient.class)
    .where(new TokenClientParam("identifier")
        .exactly()
        .systemAndCode(system, pinfl))
    .returnBundle(Bundle.class)
    .execute();

if (results.hasEntry()) {
    Patient existingPatient = (Patient) results.getEntry().get(0).getResource();
    System.out.println("Пациент найден с ID: " + existingPatient.getIdElement().getIdPart());
} else {
    System.out.println("Пациент не найден, создание нового пациента");

    // Создание нового пациента
    Patient patient = new Patient();

    // Установка профиля
    patient.getMeta()
        .addProfile("https://dhp.uz/fhir/core/StructureDefinition/uz-core-patient");

    // Установка языка
    patient.setLanguage("uz");

    // Добавление идентификатора ПИНФЛ
    Identifier identifier = patient.addIdentifier();
    identifier.setUse(Identifier.IdentifierUse.OFFICIAL);
    identifier.setSystem(system);
    identifier.setValue(pinfl);
    CodeableConcept idType = new CodeableConcept();
    idType.addCoding()
        .setSystem("http://terminology.hl7.org/CodeSystem/v2-0203")
        .setCode("NI");
    identifier.setType(idType);

    // Установка статуса
    patient.setActive(true);

    // Добавление имени
    HumanName name = patient.addName();
    name.setUse(HumanName.NameUse.OFFICIAL);
    name.setFamily("Каримов");
    name.addGiven("Алишер");
    name.addGiven("Акбарович");

    // Установка пола и даты рождения
    patient.setGender(Enumerations.AdministrativeGender.MALE);
    patient.setBirthDate(new java.text.SimpleDateFormat("yyyy-MM-dd").parse("1985-05-15"));

    // Добавление телефона
    ContactPoint phone = patient.addTelecom();
    phone.setSystem(ContactPoint.ContactPointSystem.PHONE);
    phone.setValue("+998901234567");
    phone.setUse(ContactPoint.ContactPointUse.MOBILE);

    // Создание на сервере
    MethodOutcome outcome = client.create()
        .resource(patient)
        .execute();

    IdType id = (IdType) outcome.getId();
    System.out.println("Пациент создан с ID: " + id.getIdPart());
}
</code></pre>
    </div>
    <div class="tab-pane" id="csharp">
<pre><code class="language-csharp">using Hl7.Fhir.Model;
using Hl7.Fhir.Rest;
using System;
using System.Linq;

// Создание FHIR клиента
var client = new FhirClient("https://playground.dhp.uz/fhir");

string pinfl = "12345678901234";
string system = "https://dhp.uz/fhir/core/sid/pid/uz/ni";

// Поиск существующего пациента по ПИНФЛ
var query = new SearchParams()
    .Where($"identifier={system}|{pinfl}");
var results = client.Search&lt;Patient&gt;(query);

if (results.Entry.Any())
{
    var existingPatient = (Patient)results.Entry.First().Resource;
    Console.WriteLine($"Пациент найден с ID: {existingPatient.Id}");
}
else
{
    Console.WriteLine("Пациент не найден, создание нового пациента");

    // Создание нового пациента
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
                Family = "Каримов",
                Given = new[] { "Алишер", "Акбарович" }
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

    // Создание на сервере
    var createdPatient = client.Create(patient);
    Console.WriteLine($"Пациент создан с ID: {createdPatient.Id}");
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

    // Поиск существующего пациента
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
        fmt.Printf("Пациент найден с ID: %s\n", bundle.Entry[0].Resource.ID)
        return
    }

    fmt.Println("Пациент не найден, создание нового пациента")

    // Создание нового пациента
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
                Family: "Каримов",
                Given:  []string{"Алишер", "Акбарович"},
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

    // Сериализация в JSON
    jsonData, err := json.Marshal(patient)
    if err != nil {
        panic(err)
    }

    // Отправка POST запроса
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
        fmt.Printf("Пациент создан с ID: %s\n", createdPatient.ID)
    } else {
        fmt.Printf("Ошибка: %d\n", createResp.StatusCode)
    }
}
</code></pre>
    </div>
  </div>
</div>
