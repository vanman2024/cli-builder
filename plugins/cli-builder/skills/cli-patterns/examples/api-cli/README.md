# API Client CLI Tool Example

Complete REST API client CLI demonstrating:
- HTTP client sharing via context
- Authentication in Before hook
- Multiple HTTP methods (GET, POST, PUT, DELETE)
- Headers and request configuration
- Arguments handling

## Usage

```bash
# Set environment variables
export API_URL=https://api.example.com
export API_TOKEN=your_token_here

# GET request
api get /users
api get /users/123

# POST request
api post /users '{"name": "John", "email": "john@example.com"}'
api post /posts '{"title": "Hello", "body": "World"}' --content-type application/json

# PUT request
api put /users/123 '{"name": "Jane"}'

# DELETE request
api delete /users/123

# Test authentication
api auth-test

# Custom timeout
api --timeout 60s get /slow-endpoint

# Additional headers
api get /users -H "Accept:application/json" -H "X-Custom:value"
```

## Features Demonstrated

1. **Context Management**: Shared HTTPClient and auth across requests
2. **Before Hook**: Authenticates and sets up HTTP client
3. **Arguments**: Commands accept endpoint and data as arguments
4. **Required Flags**: --url and --token are required
5. **Environment Variables**: API_URL, API_TOKEN, API_TIMEOUT fallbacks
6. **Duration Flags**: --timeout uses time.Duration type
7. **Multiple Values**: --header can be specified multiple times
8. **Helper Functions**: maskToken() for secure token display

## HTTP Client Pattern

```go
type APIContext struct {
    BaseURL    string
    Token      string
    HTTPClient *http.Client
}

// Initialize in Before hook
client := &http.Client{Timeout: timeout}
ctx := &APIContext{...}
c.App.Metadata["ctx"] = ctx

// Use in commands
ctx := c.App.Metadata["ctx"].(*APIContext)
resp, err := ctx.HTTPClient.Get(url)
```
