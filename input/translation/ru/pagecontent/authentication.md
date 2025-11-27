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

3. **Обрабатывайте ошибки токена**: Если вы получили ответ 401, возможно, ваш токен истёк. Запросите новый токен и повторите запрос.

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
<pre><code class="language-python"># pip install requests-oauthlib
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

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

# Выполнение аутентифицированного запроса - токен добавляется автоматически
response = oauth.get(f"{FHIR_URL}/Patient", params={"_count": 5})
response.raise_for_status()
patients = response.json()

print(f"Найдено {patients.get('total', 0)} пациентов")

for entry in patients.get("entry", []):
    patient = entry["resource"]
    name = patient.get("name", [{}])[0]
    print(f"  - {name.get('family', 'Неизвестно')}, {name.get('given', ['Неизвестно'])[0]}")
</code></pre>
    </div>
    <div class="tab-pane" id="javascript">
<pre><code class="language-javascript">class DHPClient {
  constructor(clientId, clientSecret) {
    this.clientId = clientId;
    this.clientSecret = clientSecret;
    this.ssoUrl = 'https://sso.dhp.uz';
    this.fhirUrl = 'https://playground.dhp.uz/fhir';
    this.accessToken = null;
    this.tokenExpiresAt = null;
  }

  async getAccessToken() {
    // Вернуть кэшированный токен, если он ещё действителен
    if (this.accessToken && this.tokenExpiresAt) {
      if (Date.now() < this.tokenExpiresAt - 60000) {
        return this.accessToken;
      }
    }

    const response = await fetch(`${this.ssoUrl}/oauth/token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: new URLSearchParams({
        grant_type: 'client_credentials',
        client_id: this.clientId,
        client_secret: this.clientSecret
      })
    });

    if (!response.ok) {
      throw new Error(`Ошибка аутентификации: ${response.status}`);
    }

    const tokenData = await response.json();
    this.accessToken = tokenData.access_token;
    const expiresIn = tokenData.expires_in || 3600;
    this.tokenExpiresAt = Date.now() + (expiresIn * 1000);

    return this.accessToken;
  }

  async request(method, endpoint, options = {}) {
    const token = await this.getAccessToken();

    const url = `${this.fhirUrl}/${endpoint}`;
    const response = await fetch(url, {
      method,
      ...options,
      headers: {
        'Authorization': `Bearer ${token}`,
        'Accept': 'application/fhir+json',
        ...options.headers
      }
    });

    if (!response.ok) {
      throw new Error(`Ошибка API запроса: ${response.status}`);
    }

    return await response.json();
  }
}

// Пример использования
(async () => {
  const client = new DHPClient('your_client_id', 'your_client_secret');

  try {
    // Поиск пациентов
    const patients = await client.request('GET', 'Patient?_count=5');
    console.log(`Найдено ${patients.total || 0} пациентов`);

    for (const entry of patients.entry || []) {
      const patient = entry.resource;
      const name = patient.name?.[0] || {};
      console.log(`  - ${name.family || 'Неизвестно'}, ${name.given?.[0] || 'Неизвестно'}`);
    }
  } catch (error) {
    console.error('Ошибка:', error.message);
  }
})();
</code></pre>
    </div>
    <div class="tab-pane" id="java">
<pre><code class="language-java">// Добавить в pom.xml: com.github.scribejava:scribejava-apis:8.3.3
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import com.github.scribejava.core.builder.ServiceBuilder;
import com.github.scribejava.core.builder.api.DefaultApi20;
import com.github.scribejava.core.model.OAuth2AccessToken;
import com.github.scribejava.core.oauth.OAuth20Service;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

public class DHPExample {
    static final String SSO_URL = "https://sso.dhp.uz";
    static final String FHIR_URL = "https://playground.dhp.uz/fhir";

    // Определение OAuth2 API для DHP
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
        // Создание OAuth2 сервиса
        OAuth20Service service = new ServiceBuilder("your_client_id")
            .apiSecret("your_client_secret")
            .build(new DHPApi());

        // Получение токена доступа через client credentials
        OAuth2AccessToken token = service.getAccessTokenClientCredentialsGrant();

        // Выполнение аутентифицированного запроса
        HttpClient httpClient = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(FHIR_URL + "/Patient?_count=5"))
            .header("Authorization", "Bearer " + token.getAccessToken())
            .header("Accept", "application/fhir+json")
            .GET()
            .build();

        HttpResponse&lt;String&gt; response = httpClient.send(
            request, HttpResponse.BodyHandlers.ofString()
        );

        JsonObject patients = JsonParser.parseString(response.body()).getAsJsonObject();

        int total = patients.has("total") ? patients.get("total").getAsInt() : 0;
        System.out.println("Найдено " + total + " пациентов");

        if (patients.has("entry")) {
            for (var entry : patients.getAsJsonArray("entry")) {
                JsonObject patient = entry.getAsJsonObject()
                    .getAsJsonObject("resource");
                if (patient.has("name")) {
                    JsonObject name = patient.getAsJsonArray("name")
                        .get(0).getAsJsonObject();
                    String family = name.has("family")
                        ? name.get("family").getAsString()
                        : "Неизвестно";
                    System.out.println("  - " + family);
                }
            }
        }
    }
}
</code></pre>
    </div>
    <div class="tab-pane" id="csharp">
<pre><code class="language-csharp">// Установка: dotnet add package IdentityModel
using System;
using System.Net.Http;
using System.Text.Json;
using System.Threading.Tasks;
using IdentityModel.Client;

const string ssoUrl = "https://sso.dhp.uz";
const string fhirUrl = "https://playground.dhp.uz/fhir";

var client = new HttpClient();

// Получение токена доступа
var tokenResponse = await client.RequestClientCredentialsTokenAsync(new ClientCredentialsTokenRequest
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

// Установка bearer-токена для последующих запросов
client.SetBearerToken(tokenResponse.AccessToken);

// Выполнение аутентифицированного запроса
var response = await client.GetAsync($"{fhirUrl}/Patient?_count=5");
response.EnsureSuccessStatusCode();

var json = await response.Content.ReadAsStringAsync();
var root = JsonDocument.Parse(json).RootElement;

var total = root.TryGetProperty("total", out var t) ? t.GetInt32() : 0;
Console.WriteLine($"Найдено {total} пациентов");

if (root.TryGetProperty("entry", out var entries))
{
    foreach (var entry in entries.EnumerateArray())
    {
        var patient = entry.GetProperty("resource");
        if (patient.TryGetProperty("name", out var names))
        {
            var name = names[0];
            var family = name.TryGetProperty("family", out var f)
                ? f.GetString()
                : "Неизвестно";
            Console.WriteLine($"  - {family}");
        }
    }
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
