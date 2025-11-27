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
<pre><code class="language-python">import requests
from datetime import datetime, timedelta

class DHPClient:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.sso_url = "https://sso.dhp.uz"
        self.fhir_url = "https://playground.dhp.uz/fhir"
        self.access_token = None
        self.token_expires_at = None

    def get_access_token(self) -> str:
        """Получить действительный токен доступа, обновив при необходимости."""
        if self.access_token and self.token_expires_at:
            if datetime.now() < self.token_expires_at - timedelta(seconds=60):
                return self.access_token

        response = requests.post(
            f"{self.sso_url}/oauth/token",
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        response.raise_for_status()

        token_data = response.json()
        self.access_token = token_data["access_token"]
        expires_in = token_data.get("expires_in", 3600)
        self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)

        return self.access_token

    def request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Выполнить аутентифицированный запрос к FHIR API."""
        token = self.get_access_token()
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {token}"
        headers["Accept"] = "application/fhir+json"

        url = f"{self.fhir_url}/{endpoint}"
        response = requests.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()

        return response.json()


# Пример использования
client = DHPClient(
    client_id="your_client_id",
    client_secret="your_client_secret"
)

# Поиск пациентов
patients = client.request("GET", "Patient", params={"_count": 5})
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
<pre><code class="language-java">import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Instant;
import java.time.Duration;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

public class DHPClient {
    private final String clientId;
    private final String clientSecret;
    private final String ssoUrl = "https://sso.dhp.uz";
    private final String fhirUrl = "https://playground.dhp.uz/fhir";
    private final HttpClient httpClient;

    private String accessToken;
    private Instant tokenExpiresAt;

    public DHPClient(String clientId, String clientSecret) {
        this.clientId = clientId;
        this.clientSecret = clientSecret;
        this.httpClient = HttpClient.newHttpClient();
    }

    public String getAccessToken() throws Exception {
        // Вернуть кэшированный токен, если он ещё действителен
        if (accessToken != null && tokenExpiresAt != null) {
            if (Instant.now().isBefore(tokenExpiresAt.minus(Duration.ofSeconds(60)))) {
                return accessToken;
            }
        }

        String requestBody = String.format(
            "grant_type=client_credentials&client_id=%s&client_secret=%s",
            clientId, clientSecret
        );

        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(ssoUrl + "/oauth/token"))
            .header("Content-Type", "application/x-www-form-urlencoded")
            .POST(HttpRequest.BodyPublishers.ofString(requestBody))
            .build();

        HttpResponse&lt;String&gt; response = httpClient.send(
            request, HttpResponse.BodyHandlers.ofString()
        );

        if (response.statusCode() != 200) {
            throw new RuntimeException("Ошибка аутентификации: " + response.statusCode());
        }

        JsonObject tokenData = JsonParser.parseString(response.body()).getAsJsonObject();
        accessToken = tokenData.get("access_token").getAsString();
        int expiresIn = tokenData.has("expires_in")
            ? tokenData.get("expires_in").getAsInt()
            : 3600;
        tokenExpiresAt = Instant.now().plus(Duration.ofSeconds(expiresIn));

        return accessToken;
    }

    public String request(String method, String endpoint) throws Exception {
        String token = getAccessToken();

        HttpRequest.Builder builder = HttpRequest.newBuilder()
            .uri(URI.create(fhirUrl + "/" + endpoint))
            .header("Authorization", "Bearer " + token)
            .header("Accept", "application/fhir+json");

        if ("GET".equals(method)) {
            builder.GET();
        }

        HttpResponse&lt;String&gt; response = httpClient.send(
            builder.build(), HttpResponse.BodyHandlers.ofString()
        );

        if (response.statusCode() != 200) {
            throw new RuntimeException("Ошибка API запроса: " + response.statusCode());
        }

        return response.body();
    }

    public static void main(String[] args) throws Exception {
        DHPClient client = new DHPClient("your_client_id", "your_client_secret");

        String patientsJson = client.request("GET", "Patient?_count=5");
        JsonObject patients = JsonParser.parseString(patientsJson).getAsJsonObject();

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
<pre><code class="language-csharp">using System;
using System.Net.Http;
using System.Text.Json;
using System.Threading.Tasks;

public class DHPClient
{
    private readonly string _clientId;
    private readonly string _clientSecret;
    private readonly string _ssoUrl = "https://sso.dhp.uz";
    private readonly string _fhirUrl = "https://playground.dhp.uz/fhir";
    private readonly HttpClient _httpClient;

    private string _accessToken;
    private DateTime? _tokenExpiresAt;

    public DHPClient(string clientId, string clientSecret)
    {
        _clientId = clientId;
        _clientSecret = clientSecret;
        _httpClient = new HttpClient();
    }

    public async Task&lt;string&gt; GetAccessTokenAsync()
    {
        // Вернуть кэшированный токен, если он ещё действителен
        if (_accessToken != null && _tokenExpiresAt.HasValue)
        {
            if (DateTime.UtcNow < _tokenExpiresAt.Value.AddSeconds(-60))
            {
                return _accessToken;
            }
        }

        var content = new FormUrlEncodedContent(new[]
        {
            new KeyValuePair&lt;string, string&gt;("grant_type", "client_credentials"),
            new KeyValuePair&lt;string, string&gt;("client_id", _clientId),
            new KeyValuePair&lt;string, string&gt;("client_secret", _clientSecret)
        });

        var response = await _httpClient.PostAsync($"{_ssoUrl}/oauth/token", content);
        response.EnsureSuccessStatusCode();

        var json = await response.Content.ReadAsStringAsync();
        var tokenData = JsonDocument.Parse(json).RootElement;

        _accessToken = tokenData.GetProperty("access_token").GetString();
        var expiresIn = tokenData.TryGetProperty("expires_in", out var exp)
            ? exp.GetInt32()
            : 3600;
        _tokenExpiresAt = DateTime.UtcNow.AddSeconds(expiresIn);

        return _accessToken;
    }

    public async Task&lt;JsonDocument&gt; RequestAsync(string method, string endpoint)
    {
        var token = await GetAccessTokenAsync();

        var request = new HttpRequestMessage(new HttpMethod(method), $"{_fhirUrl}/{endpoint}");
        request.Headers.Add("Authorization", $"Bearer {token}");
        request.Headers.Add("Accept", "application/fhir+json");

        var response = await _httpClient.SendAsync(request);
        response.EnsureSuccessStatusCode();

        var json = await response.Content.ReadAsStringAsync();
        return JsonDocument.Parse(json);
    }

    public static async Task Main(string[] args)
    {
        var client = new DHPClient("your_client_id", "your_client_secret");

        var patients = await client.RequestAsync("GET", "Patient?_count=5");
        var root = patients.RootElement;

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
    "net/url"
    "strings"
    "sync"
    "time"
)

type DHPClient struct {
    ClientID     string
    ClientSecret string
    SSOUrl       string
    FHIRUrl      string

    accessToken    string
    tokenExpiresAt time.Time
    mu             sync.Mutex
}

type TokenResponse struct {
    AccessToken string `json:"access_token"`
    TokenType   string `json:"token_type"`
    ExpiresIn   int    `json:"expires_in"`
}

func NewDHPClient(clientID, clientSecret string) *DHPClient {
    return &DHPClient{
        ClientID:     clientID,
        ClientSecret: clientSecret,
        SSOUrl:       "https://sso.dhp.uz",
        FHIRUrl:      "https://playground.dhp.uz/fhir",
    }
}

func (c *DHPClient) GetAccessToken() (string, error) {
    c.mu.Lock()
    defer c.mu.Unlock()

    // Вернуть кэшированный токен, если он ещё действителен
    if c.accessToken != "" && time.Now().Before(c.tokenExpiresAt.Add(-60*time.Second)) {
        return c.accessToken, nil
    }

    data := url.Values{}
    data.Set("grant_type", "client_credentials")
    data.Set("client_id", c.ClientID)
    data.Set("client_secret", c.ClientSecret)

    resp, err := http.Post(
        c.SSOUrl+"/oauth/token",
        "application/x-www-form-urlencoded",
        strings.NewReader(data.Encode()),
    )
    if err != nil {
        return "", err
    }
    defer resp.Body.Close()

    if resp.StatusCode != 200 {
        return "", fmt.Errorf("ошибка аутентификации: %d", resp.StatusCode)
    }

    body, err := io.ReadAll(resp.Body)
    if err != nil {
        return "", err
    }

    var tokenResp TokenResponse
    if err := json.Unmarshal(body, &tokenResp); err != nil {
        return "", err
    }

    c.accessToken = tokenResp.AccessToken
    expiresIn := tokenResp.ExpiresIn
    if expiresIn == 0 {
        expiresIn = 3600
    }
    c.tokenExpiresAt = time.Now().Add(time.Duration(expiresIn) * time.Second)

    return c.accessToken, nil
}

func (c *DHPClient) Request(method, endpoint string) (map[string]interface{}, error) {
    token, err := c.GetAccessToken()
    if err != nil {
        return nil, err
    }

    req, err := http.NewRequest(method, c.FHIRUrl+"/"+endpoint, nil)
    if err != nil {
        return nil, err
    }

    req.Header.Set("Authorization", "Bearer "+token)
    req.Header.Set("Accept", "application/fhir+json")

    resp, err := http.DefaultClient.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    if resp.StatusCode != 200 {
        return nil, fmt.Errorf("ошибка API запроса: %d", resp.StatusCode)
    }

    body, err := io.ReadAll(resp.Body)
    if err != nil {
        return nil, err
    }

    var result map[string]interface{}
    if err := json.Unmarshal(body, &result); err != nil {
        return nil, err
    }

    return result, nil
}

func main() {
    client := NewDHPClient("your_client_id", "your_client_secret")

    patients, err := client.Request("GET", "Patient?_count=5")
    if err != nil {
        fmt.Printf("Ошибка: %v\n", err)
        return
    }

    total := 0
    if t, ok := patients["total"].(float64); ok {
        total = int(t)
    }
    fmt.Printf("Найдено %d пациентов\n", total)

    if entries, ok := patients["entry"].([]interface{}); ok {
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
