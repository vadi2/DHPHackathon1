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

3. **Handle token errors**: If you receive a 401 response, your token may have expired. Refresh the token and retry the request.

## Refreshing your access token

When your access token expires, you can obtain a new one using the refresh token.

**How the refresh token is delivered:**
- The refresh token is returned as an HTTP-only cookie in the response from the initial `/oauth/token` request
- It cannot be accessed by JavaScript (protection against XSS attacks)
- It is automatically included in subsequent requests to the SSO server
- You must ensure your HTTP client is configured to handle cookies

### Refresh request

- HTTP method: POST
- Endpoint: `https://sso.dhp.uz/jwt/refresh`
- No request body required
- Credentials: `include` (to send the HTTP-only cookie)

### Expected responses

**Success (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

**Invalid or expired refresh token (401 Unauthorized):**
```json
{
  "error": "invalid_token",
  "error_description": "Refresh token is invalid or expired"
}
```

If the refresh token is expired, you need to re-authenticate using the client credentials flow.

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
<pre><code class="language-python"># pip install requests-oauthlib fhir.resources
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from fhir.resources.bundle import Bundle

SSO_URL = "https://sso.dhp.uz"
FHIR_URL = "https://playground.dhp.uz/fhir"
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"

# Create OAuth2 session with client credentials
client = BackendApplicationClient(client_id=CLIENT_ID)
oauth = OAuth2Session(client=client)

# Fetch token (session will auto-refresh when needed)
oauth.fetch_token(
    token_url=f"{SSO_URL}/oauth/token",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

# Make authenticated request
response = oauth.get(f"{FHIR_URL}/Patient", params={"_count": 5})
response.raise_for_status()

# Parse response using fhir.resources
bundle = Bundle.model_validate(response.json())

print(f"Found {bundle.total or 0} patients")

for entry in bundle.entry or []:
    patient = entry.resource
    family = patient.name[0].family if patient.name else "Unknown"
    print(f"  - {family}")
</code></pre>
    </div>
    <div class="tab-pane" id="javascript">
<pre><code class="language-javascript">// npm install simple-oauth2
const { ClientCredentials } = require('simple-oauth2');

const SSO_URL = 'https://sso.dhp.uz';
const FHIR_URL = 'https://playground.dhp.uz/fhir';

// Configure OAuth2 client
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
    // Get access token
    const tokenResult = await oauth2.getToken({});
    const accessToken = tokenResult.token.access_token;

    // Make authenticated request
    const response = await fetch(`${FHIR_URL}/Patient?_count=5`, {
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Accept': 'application/fhir+json'
      }
    });

    const patients = await response.json();
    console.log(`Found ${patients.total || 0} patients`);

    for (const entry of patients.entry || []) {
      const patient = entry.resource;
      const name = patient.name?.[0] || {};
      console.log(`  - ${name.family || 'Unknown'}`);
    }
  } catch (error) {
    console.error('Error:', error.message);
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
        // Get OAuth2 token
        OAuth20Service oauth = new ServiceBuilder("your_client_id")
            .apiSecret("your_client_secret")
            .build(new DHPApi());
        String accessToken = oauth.getAccessTokenClientCredentialsGrant().getAccessToken();

        // Create HAPI FHIR client with bearer token
        FhirContext ctx = FhirContext.forR5();
        IGenericClient client = ctx.newRestfulGenericClient(FHIR_URL);
        client.registerInterceptor(new BearerTokenAuthInterceptor(accessToken));

        // Search for patients using HAPI FHIR
        Bundle results = client.search()
            .forResource(Patient.class)
            .count(5)
            .returnBundle(Bundle.class)
            .execute();

        System.out.println("Found " + results.getTotal() + " patients");

        for (Bundle.BundleEntryComponent entry : results.getEntry()) {
            Patient patient = (Patient) entry.getResource();
            String family = patient.hasName()
                ? patient.getNameFirstRep().getFamily()
                : "Unknown";
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

// Get OAuth2 token
var httpClient = new HttpClient();
var tokenResponse = await httpClient.RequestClientCredentialsTokenAsync(new ClientCredentialsTokenRequest
{
    Address = $"{ssoUrl}/oauth/token",
    ClientId = "your_client_id",
    ClientSecret = "your_client_secret"
});

if (tokenResponse.IsError)
{
    Console.WriteLine($"Error: {tokenResponse.Error}");
    return;
}

// Create Firely FHIR client with bearer token
var settings = new FhirClientSettings { PreferredFormat = ResourceFormat.Json };
var client = new FhirClient(fhirUrl, settings);
client.RequestHeaders.Add("Authorization", $"Bearer {tokenResponse.AccessToken}");

// Search for patients using Firely SDK
var results = await client.SearchAsync&lt;Patient&gt;(new[] { "_count=5" });

Console.WriteLine($"Found {results.Total} patients");

foreach (var entry in results.Entry)
{
    var patient = (Patient)entry.Resource;
    var family = patient.Name.FirstOrDefault()?.Family ?? "Unknown";
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
    // Configure OAuth2 client credentials
    config := &clientcredentials.Config{
        ClientID:     "your_client_id",
        ClientSecret: "your_client_secret",
        TokenURL:     "https://sso.dhp.uz/oauth/token",
    }

    // Create HTTP client with automatic token management
    client := config.Client(context.Background())

    // Make authenticated request
    resp, err := client.Get(fhirURL + "/Patient?_count=5")
    if err != nil {
        fmt.Printf("Error: %v\n", err)
        return
    }
    defer resp.Body.Close()

    body, err := io.ReadAll(resp.Body)
    if err != nil {
        fmt.Printf("Error reading response: %v\n", err)
        return
    }

    var result map[string]interface{}
    if err := json.Unmarshal(body, &result); err != nil {
        fmt.Printf("Error parsing JSON: %v\n", err)
        return
    }

    total := 0
    if t, ok := result["total"].(float64); ok {
        total = int(t)
    }
    fmt.Printf("Found %d patients\n", total)

    if entries, ok := result["entry"].([]interface{}); ok {
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
