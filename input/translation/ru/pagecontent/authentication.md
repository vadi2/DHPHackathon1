# Аутентификация через SSO

## Обзор

Цель: Научиться аутентифицировать ваше приложение на платформе DHP с использованием потока OAuth 2.0 client credentials для межсервисной интеграции.

- Навыки: OAuth 2.0, HTTP POST запросы, управление токенами
- URL SSO: `https://sso.dhp.uz`
- Базовый URL: `https://playground.dhp.uz/fhir`
- Полезные ссылки:
  - [Документация DHP SSO](https://wiki.dhp.uz/s/integration/doc/sso-ghGrj2qWmr)
  - [OAuth 2.0 Client Credentials](https://oauth.net/2/grant-types/client-credentials/)

**Обратная связь:** Поделитесь своим опытом, проблемами и успехами в [документе коннектафона](https://docs.google.com/document/d/1PdQ8zBI9xkISP3tAqIK8-TGMql3kVVZ4UNoHVYqCy4Y/edit?usp=sharing).

## Что такое client credentials grant?

Client credentials grant — это поток OAuth 2.0, предназначенный для серверных сервисов и межсистемной интеграции, где конечный пользователь не участвует. Ваше приложение аутентифицируется напрямую на сервере SSO, используя учётные данные, предоставленные администратором.

**Варианты использования:**
- Интеграция медицинских информационных систем (МИС)
- Фоновые задачи синхронизации данных
- Автоматизированные сервисы мониторинга
- Межсистемный обмен данными

## Процесс аутентификации

```
┌─────────────────┐                              ┌─────────────────┐
│  Ваше серверное │                              │   Сервер SSO    │
│  приложение     │                              │   DHP           │
└────────┬────────┘                              └────────┬────────┘
         │                                                │
         │  1. POST /oauth/token                          │
         │     grant_type=client_credentials              │
         │     client_id=ваш_client_id                    │
         │     client_secret=ваш_client_secret            │
         │ ─────────────────────────────────────────────► │
         │                                                │
         │  2. Ответ с токеном доступа                    │
         │     { "access_token": "...", ... }             │
         │ ◄───────────────────────────────────────────── │
         │                                                │
┌────────┴────────┐                              ┌────────┴────────┐
│  Ваше серверное │                              │   FHIR-сервер   │
│  приложение     │                              │   DHP           │
└────────┬────────┘                              └────────┬────────┘
         │                                                │
         │  3. API-запрос с Bearer-токеном                │
         │     Authorization: Bearer <access_token>       │
         │ ─────────────────────────────────────────────► │
         │                                                │
         │  4. Ответ API                                  │
         │ ◄───────────────────────────────────────────── │
         │                                                │
```

## Получение учётных данных

Перед аутентификацией вам необходимо получить:

1. **client_id**: уникальный идентификатор вашего приложения
2. **client_secret**: секретный ключ вашего приложения

Эти учётные данные предоставляются администратором DHP. Для коннектафона учётные данные будут распределены участникам.

**Важно:** Храните ваш `client_secret` в безопасности. Никогда не раскрывайте его в клиентском коде или публичных репозиториях.

## Получение токена доступа

### Запрос токена

- HTTP-метод: POST
- Endpoint: `https://sso.dhp.uz/oauth/token`
- Content-Type: `application/x-www-form-urlencoded`

**Параметры запроса:**

| Параметр | Значение | Описание |
|----------|----------|----------|
| grant_type | `client_credentials` | Тип гранта OAuth 2.0 |
| client_id | Ваш client ID | Идентификатор приложения |
| client_secret | Ваш client secret | Секрет приложения |

### Ожидаемые ответы

**Успех (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

**Неверные параметры (400 Bad Request):**
```json
{
  "error": "invalid_request",
  "error_description": "Missing required parameter"
}
```

**Неверные учётные данные (401 Unauthorized):**
```json
{
  "error": "invalid_client",
  "error_description": "Invalid client credentials"
}
```

## Использование токена доступа

После получения токена доступа включайте его в заголовок `Authorization` ваших запросов к FHIR API:

```
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Пример: получение пациента

```
GET https://playground.dhp.uz/fhir/Patient/123
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
Accept: application/fhir+json
```

## Лучшие практики управления токенами

1. **Кэшируйте токен**: Сохраняйте токен доступа и используйте его повторно до истечения срока действия. Не запрашивайте новый токен для каждого API-вызова.

2. **Отслеживайте срок действия**: Используйте значение `expires_in`, чтобы знать, когда обновлять токен. Запрашивайте новый токен до истечения текущего.

3. **Обрабатывайте ошибки токена**: Если вы получили ответ 401, возможно, ваш токен истёк. Обновите токен и повторите запрос.

## Обновление токена доступа

Когда срок действия токена доступа истекает, вы можете получить новый с помощью refresh-токена.

**Как доставляется refresh-токен:**
- Refresh-токен возвращается в виде HTTP-only cookie в ответе на первоначальный запрос `/oauth/token`
- Он недоступен для JavaScript (защита от XSS-атак)
- Он автоматически включается в последующие запросы к серверу SSO
- Убедитесь, что ваш HTTP-клиент настроен на работу с cookies

### Запрос на обновление

- HTTP-метод: POST
- Endpoint: `https://sso.dhp.uz/jwt/refresh`
- Тело запроса не требуется
- Credentials: `include` (для отправки HTTP-only cookie)

### Ожидаемые ответы

**Успех (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

**Недействительный или истёкший refresh-токен (401 Unauthorized):**
```json
{
  "error": "invalid_token",
  "error_description": "Refresh token is invalid or expired"
}
```

Если срок действия refresh-токена истёк, необходимо повторно аутентифицироваться с помощью потока client credentials.

---

## Примеры кода

{% include code-tabs-style.html %}

Ниже приведены примеры аутентификации и выполнения API-вызовов на различных языках программирования:

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
<pre><code class="language-bash"># Шаг 1: Получение токена доступа
TOKEN_RESPONSE=$(curl -s -X POST "https://sso.dhp.uz/oauth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=your_client_id" \
  -d "client_secret=your_client_secret")

# Извлечение токена доступа с помощью jq
ACCESS_TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.access_token')

echo "Access Token: $ACCESS_TOKEN"

# Шаг 2: Использование токена для вызова FHIR API
curl "https://playground.dhp.uz/fhir/Patient?_count=5" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Accept: application/fhir+json"
</code></pre>
    </div>
    <div class="tab-pane" id="python">
<pre><code class="language-python"># pip install requests-oauthlib fhir.resources
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from fhir.resources.bundle import Bundle

SSO_URL = "https://sso.dhp.uz"
FHIR_URL = "https://playground.dhp.uz/fhir"
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"

# Создание OAuth2 сессии с client credentials
client = BackendApplicationClient(client_id=CLIENT_ID)
oauth = OAuth2Session(client=client)

# Получение токена (сессия автоматически обновит при необходимости)
oauth.fetch_token(
    token_url=f"{SSO_URL}/oauth/token",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

# Выполнение аутентифицированного запроса
response = oauth.get(f"{FHIR_URL}/Patient", params={"_count": 5})
response.raise_for_status()

# Разбор ответа с помощью fhir.resources
bundle = Bundle.model_validate(response.json())

print(f"Найдено {bundle.total or 0} пациентов")

for entry in bundle.entry or []:
    patient = entry.resource
    family = patient.name[0].family if patient.name else "Неизвестно"
    print(f"  - {family}")
</code></pre>
    </div>
    <div class="tab-pane" id="javascript">
<pre><code class="language-javascript">// npm install simple-oauth2
const { ClientCredentials } = require('simple-oauth2');

const SSO_URL = 'https://sso.dhp.uz';
const FHIR_URL = 'https://playground.dhp.uz/fhir';

// Настройка OAuth2 клиента
const oauth2 = new ClientCredentials({
  client: {
    id: 'your_client_id',
    secret: 'your_client_secret'
  },
  auth: {
    tokenHost: SSO_URL,
    tokenPath: '/oauth/token'
  }
});

(async () => {
  try {
    // Получение токена доступа
    const tokenResult = await oauth2.getToken({});
    const accessToken = tokenResult.token.access_token;

    // Выполнение аутентифицированного запроса
    const response = await fetch(`${FHIR_URL}/Patient?_count=5`, {
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Accept': 'application/fhir+json'
      }
    });

    const patients = await response.json();
    console.log(`Найдено ${patients.total || 0} пациентов`);

    for (const entry of patients.entry || []) {
      const patient = entry.resource;
      const name = patient.name?.[0] || {};
      console.log(`  - ${name.family || 'Неизвестно'}`);
    }
  } catch (error) {
    console.error('Ошибка:', error.message);
  }
})();
</code></pre>
    </div>
    <div class="tab-pane" id="java">
<pre><code class="language-java">// pom.xml: ca.uhn.hapi.fhir:hapi-fhir-client:7.0.0, com.github.scribejava:scribejava-core:8.3.3
import ca.uhn.fhir.context.FhirContext;
import ca.uhn.fhir.rest.client.api.IGenericClient;
import ca.uhn.fhir.rest.client.interceptor.BearerTokenAuthInterceptor;
import org.hl7.fhir.r5.model.Bundle;
import org.hl7.fhir.r5.model.Patient;
import com.github.scribejava.core.builder.ServiceBuilder;
import com.github.scribejava.core.builder.api.DefaultApi20;
import com.github.scribejava.core.oauth.OAuth20Service;

public class DHPExample {
    static final String SSO_URL = "https://sso.dhp.uz";
    static final String FHIR_URL = "https://playground.dhp.uz/fhir";

    static class DHPApi extends DefaultApi20 {
        @Override
        public String getAccessTokenEndpoint() {
            return SSO_URL + "/oauth/token";
        }

        @Override
        protected String getAuthorizationBaseUrl() {
            return SSO_URL + "/oauth/authorize";
        }
    }

    public static void main(String[] args) throws Exception {
        // Получение OAuth2 токена
        OAuth20Service oauth = new ServiceBuilder("your_client_id")
            .apiSecret("your_client_secret")
            .build(new DHPApi());
        String accessToken = oauth.getAccessTokenClientCredentialsGrant().getAccessToken();

        // Создание HAPI FHIR клиента с bearer-токеном
        FhirContext ctx = FhirContext.forR5();
        IGenericClient client = ctx.newRestfulGenericClient(FHIR_URL);
        client.registerInterceptor(new BearerTokenAuthInterceptor(accessToken));

        // Поиск пациентов с использованием HAPI FHIR
        Bundle results = client.search()
            .forResource(Patient.class)
            .count(5)
            .returnBundle(Bundle.class)
            .execute();

        System.out.println("Найдено " + results.getTotal() + " пациентов");

        for (Bundle.BundleEntryComponent entry : results.getEntry()) {
            Patient patient = (Patient) entry.getResource();
            String family = patient.hasName()
                ? patient.getNameFirstRep().getFamily()
                : "Неизвестно";
            System.out.println("  - " + family);
        }
    }
}
</code></pre>
    </div>
    <div class="tab-pane" id="csharp">
<pre><code class="language-csharp">// dotnet add package Hl7.Fhir.R5
// dotnet add package IdentityModel
using Hl7.Fhir.Model;
using Hl7.Fhir.Rest;
using IdentityModel.Client;

const string ssoUrl = "https://sso.dhp.uz";
const string fhirUrl = "https://playground.dhp.uz/fhir";

// Получение OAuth2 токена
var httpClient = new HttpClient();
var tokenResponse = await httpClient.RequestClientCredentialsTokenAsync(new ClientCredentialsTokenRequest
{
    Address = $"{ssoUrl}/oauth/token",
    ClientId = "your_client_id",
    ClientSecret = "your_client_secret"
});

if (tokenResponse.IsError)
{
    Console.WriteLine($"Ошибка: {tokenResponse.Error}");
    return;
}

// Создание Firely FHIR клиента с bearer-токеном
var settings = new FhirClientSettings { PreferredFormat = ResourceFormat.Json };
var client = new FhirClient(fhirUrl, settings);
client.RequestHeaders.Add("Authorization", $"Bearer {tokenResponse.AccessToken}");

// Поиск пациентов с использованием Firely SDK
var results = await client.SearchAsync&lt;Patient&gt;(new[] { "_count=5" });

Console.WriteLine($"Найдено {results.Total} пациентов");

foreach (var entry in results.Entry)
{
    var patient = (Patient)entry.Resource;
    var family = patient.Name.FirstOrDefault()?.Family ?? "Неизвестно";
    Console.WriteLine($"  - {family}");
}
</code></pre>
    </div>
    <div class="tab-pane" id="go">
<pre><code class="language-go">package main

import (
    "context"
    "encoding/json"
    "fmt"
    "io"

    "golang.org/x/oauth2/clientcredentials"
)

const fhirURL = "https://playground.dhp.uz/fhir"

func main() {
    // Настройка OAuth2 client credentials
    config := &clientcredentials.Config{
        ClientID:     "your_client_id",
        ClientSecret: "your_client_secret",
        TokenURL:     "https://sso.dhp.uz/oauth/token",
    }

    // Создание HTTP-клиента с автоматическим управлением токенами
    client := config.Client(context.Background())

    // Выполнение аутентифицированного запроса
    resp, err := client.Get(fhirURL + "/Patient?_count=5")
    if err != nil {
        fmt.Printf("Ошибка: %v\n", err)
        return
    }
    defer resp.Body.Close()

    body, err := io.ReadAll(resp.Body)
    if err != nil {
        fmt.Printf("Ошибка чтения ответа: %v\n", err)
        return
    }

    var result map[string]interface{}
    if err := json.Unmarshal(body, &result); err != nil {
        fmt.Printf("Ошибка разбора JSON: %v\n", err)
        return
    }

    total := 0
    if t, ok := result["total"].(float64); ok {
        total = int(t)
    }
    fmt.Printf("Найдено %d пациентов\n", total)

    if entries, ok := result["entry"].([]interface{}); ok {
        for _, e := range entries {
            entry := e.(map[string]interface{})
            resource := entry["resource"].(map[string]interface{})
            if names, ok := resource["name"].([]interface{}); ok && len(names) > 0 {
                name := names[0].(map[string]interface{})
                family := "Неизвестно"
                if f, ok := name["family"].(string); ok {
                    family = f
                }
                fmt.Printf("  - %s\n", family)
            }
        }
    }
}
</code></pre>
    </div>
  </div>
</div>

---

## Упражнение

**Задание:** Аутентифицируйтесь на сервере SSO и выполните аутентифицированный запрос к FHIR API.

1. Используйте предоставленные вам `client_id` и `client_secret` для получения токена доступа
2. Проверьте токен, выполнив поиск организаций:
   ```
   GET https://playground.dhp.uz/fhir/Organization?_count=5
   Authorization: Bearer <ваш_токен_доступа>
   ```
3. Выполните поиск пациентов с использованием аутентифицированного запроса:
   ```
   GET https://playground.dhp.uz/fhir/Patient?_count=5
   Authorization: Bearer <ваш_токен_доступа>
   ```

**Проверка:** Если аутентификация прошла успешно, вы должны получить корректный JSON-ответ вместо ошибки 401 Unauthorized.
