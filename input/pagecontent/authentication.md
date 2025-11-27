# Authentication with SSO

## Overview

Goal: Learn how to authenticate your application with the DHP platform using OAuth 2.0 client credentials flow for backend service-to-service integration.

- Skills: OAuth 2.0, HTTP POST requests, token management
- SSO URL: `https://sso.dhp.uz`
- Base URL: `https://playground.dhp.uz/fhir`
- Useful links:
  - [DHP SSO Documentation](https://wiki.dhp.uz/s/integration/doc/sso-ghGrj2qWmr)
  - [OAuth 2.0 Client Credentials](https://oauth.net/2/grant-types/client-credentials/)

**Feedback:** Share your experience, issues and successes in the [connectathon document](https://docs.google.com/document/d/1PdQ8zBI9xkISP3tAqIK8-TGMql3kVVZ4UNoHVYqCy4Y/edit?usp=sharing).

## What is the client credentials grant?

The client credentials grant is an OAuth 2.0 flow designed for backend services and system-to-system integration where no end-user is involved. Your application authenticates directly with the SSO server using credentials provided by the administrator.

**Use cases:**
- Medical information systems (MIS) integration
- Background data synchronization tasks
- Automated monitoring services
- System-to-system data exchange

## Authentication flow

```
┌─────────────────┐                              ┌─────────────────┐
│  Your Backend   │                              │   DHP SSO       │
│  Application    │                              │   Server        │
└────────┬────────┘                              └────────┬────────┘
         │                                                │
         │  1. POST /oauth/token                          │
         │     grant_type=client_credentials              │
         │     client_id=your_client_id                   │
         │     client_secret=your_client_secret           │
         │ ─────────────────────────────────────────────► │
         │                                                │
         │  2. Access Token Response                      │
         │     { "access_token": "...", ... }             │
         │ ◄───────────────────────────────────────────── │
         │                                                │
┌────────┴────────┐                              ┌────────┴────────┐
│  Your Backend   │                              │   DHP FHIR      │
│  Application    │                              │   Server        │
└────────┬────────┘                              └────────┬────────┘
         │                                                │
         │  3. API Request with Bearer Token              │
         │     Authorization: Bearer <access_token>       │
         │ ─────────────────────────────────────────────► │
         │                                                │
         │  4. API Response                               │
         │ ◄───────────────────────────────────────────── │
         │                                                │
```

## Getting your credentials

Before you can authenticate, you need to obtain:

1. **client_id**: Your application's unique identifier
2. **client_secret**: Your application's secret key

These credentials are provided by the DHP administrator. For the connectathon, credentials will be distributed to participants.

**Important:** Keep your `client_secret` secure. Never expose it in client-side code or public repositories.

## Obtaining an access token

### Token request

- HTTP method: POST
- Endpoint: `https://sso.dhp.uz/oauth/token`
- Content-Type: `application/x-www-form-urlencoded`

**Request parameters:**

| Parameter | Value | Description |
|-----------|-------|-------------|
| grant_type | `client_credentials` | OAuth 2.0 grant type |
| client_id | Your client ID | Application identifier |
| client_secret | Your client secret | Application secret |

### Expected responses

**Success (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

**Invalid parameters (400 Bad Request):**
```json
{
  "error": "invalid_request",
  "error_description": "Missing required parameter"
}
```

**Invalid credentials (401 Unauthorized):**
```json
{
  "error": "invalid_client",
  "error_description": "Invalid client credentials"
}
```

## Using the access token

Once you have an access token, include it in the `Authorization` header of your FHIR API requests:

```
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Example: fetching a Patient

```
GET https://playground.dhp.uz/fhir/Patient/123
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
Accept: application/fhir+json
```

## Token management best practices

1. **Cache the token**: Store the access token and reuse it until it expires. Don't request a new token for every API call.

2. **Track expiration**: Use the `expires_in` value to know when to refresh. Request a new token before the current one expires.

3. **Handle token errors**: If you receive a 401 response, your token may have expired. Request a new token and retry the request.

---

## Code examples

{% include code-tabs-style.html %}

Below are examples of authenticating and making API calls in various programming languages:

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
<pre><code class="language-bash"># Step 1: Get access token
TOKEN_RESPONSE=$(curl -s -X POST "https://sso.dhp.uz/oauth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=your_client_id" \
  -d "client_secret=your_client_secret")

# Extract the access token using jq
ACCESS_TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.access_token')

echo "Access Token: $ACCESS_TOKEN"

# Step 2: Use the token to call the FHIR API
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
        """Get a valid access token, refreshing if necessary."""
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
        """Make an authenticated request to the FHIR API."""
        token = self.get_access_token()
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {token}"
        headers["Accept"] = "application/fhir+json"

        url = f"{self.fhir_url}/{endpoint}"
        response = requests.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()

        return response.json()


# Example usage
client = DHPClient(
    client_id="your_client_id",
    client_secret="your_client_secret"
)

# Search for patients
patients = client.request("GET", "Patient", params={"_count": 5})
print(f"Found {patients.get('total', 0)} patients")

for entry in patients.get("entry", []):
    patient = entry["resource"]
    name = patient.get("name", [{}])[0]
    print(f"  - {name.get('family', 'Unknown')}, {name.get('given', ['Unknown'])[0]}")
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
    // Return cached token if still valid
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
      throw new Error(`Authentication failed: ${response.status}`);
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
      throw new Error(`API request failed: ${response.status}`);
    }

    return await response.json();
  }
}

// Example usage
(async () => {
  const client = new DHPClient('your_client_id', 'your_client_secret');

  try {
    // Search for patients
    const patients = await client.request('GET', 'Patient?_count=5');
    console.log(`Found ${patients.total || 0} patients`);

    for (const entry of patients.entry || []) {
      const patient = entry.resource;
      const name = patient.name?.[0] || {};
      console.log(`  - ${name.family || 'Unknown'}, ${name.given?.[0] || 'Unknown'}`);
    }
  } catch (error) {
    console.error('Error:', error.message);
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
        // Return cached token if still valid
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
            throw new RuntimeException("Authentication failed: " + response.statusCode());
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
            throw new RuntimeException("API request failed: " + response.statusCode());
        }

        return response.body();
    }

    public static void main(String[] args) throws Exception {
        DHPClient client = new DHPClient("your_client_id", "your_client_secret");

        String patientsJson = client.request("GET", "Patient?_count=5");
        JsonObject patients = JsonParser.parseString(patientsJson).getAsJsonObject();

        int total = patients.has("total") ? patients.get("total").getAsInt() : 0;
        System.out.println("Found " + total + " patients");

        if (patients.has("entry")) {
            for (var entry : patients.getAsJsonArray("entry")) {
                JsonObject patient = entry.getAsJsonObject()
                    .getAsJsonObject("resource");
                if (patient.has("name")) {
                    JsonObject name = patient.getAsJsonArray("name")
                        .get(0).getAsJsonObject();
                    String family = name.has("family")
                        ? name.get("family").getAsString()
                        : "Unknown";
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
        // Return cached token if still valid
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
        Console.WriteLine($"Found {total} patients");

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
                        : "Unknown";
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

    // Return cached token if still valid
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
        return "", fmt.Errorf("authentication failed: %d", resp.StatusCode)
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
        return nil, fmt.Errorf("API request failed: %d", resp.StatusCode)
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
        fmt.Printf("Error: %v\n", err)
        return
    }

    total := 0
    if t, ok := patients["total"].(float64); ok {
        total = int(t)
    }
    fmt.Printf("Found %d patients\n", total)

    if entries, ok := patients["entry"].([]interface{}); ok {
        for _, e := range entries {
            entry := e.(map[string]interface{})
            resource := entry["resource"].(map[string]interface{})
            if names, ok := resource["name"].([]interface{}); ok && len(names) > 0 {
                name := names[0].(map[string]interface{})
                family := "Unknown"
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

## Exercise

**Task:** Authenticate with the SSO server and make an authenticated request to the FHIR API.

1. Use your provided `client_id` and `client_secret` to obtain an access token
2. Verify the token by searching for organizations:
   ```
   GET https://playground.dhp.uz/fhir/Organization?_count=5
   Authorization: Bearer <your_access_token>
   ```
3. Search for patients using the authenticated request:
   ```
   GET https://playground.dhp.uz/fhir/Patient?_count=5
   Authorization: Bearer <your_access_token>
   ```

**Verification:** If authentication is successful, you should receive a valid JSON response instead of a 401 Unauthorized error.
