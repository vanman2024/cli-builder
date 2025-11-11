# CLI Patterns Examples Index

Comprehensive examples demonstrating urfave/cli patterns in production-ready applications.

## Example Applications

### 1. Database CLI Tool (`db-cli/`)

**Purpose**: Complete database management CLI with categories, hooks, and connection handling.

**Features**:
- Command categories (Schema, Data, Admin)
- Before hook for connection validation
- After hook for cleanup
- Required and optional flags
- Environment variable fallbacks

**Commands**:
- `migrate` - Run migrations with direction and steps
- `rollback` - Rollback last migration
- `seed` - Seed database with test data
- `backup` - Create database backup
- `restore` - Restore from backup
- `status` - Check database status
- `vacuum` - Optimize database

**Key Patterns**:
```go
// Connection validation in Before hook
Before: func(c *cli.Context) error {
    conn := c.String("connection")
    // Validate connection
    return nil
}

// Cleanup in After hook
After: func(c *cli.Context) error {
    // Close connections
    return nil
}
```

---

### 2. Deployment CLI Tool (`deploy-cli/`)

**Purpose**: Deployment automation with context management and environment validation.

**Features**:
- Context management with shared state
- Environment validation
- Confirmation prompts for destructive actions
- AWS region configuration
- Build, deploy, and monitor workflows

**Commands**:
- `build` - Build application with tags
- `test` - Run test suite
- `deploy` - Deploy to environment (with confirmation)
- `rollback` - Rollback to previous version
- `logs` - View deployment logs
- `status` - Check deployment status

**Key Patterns**:
```go
// Shared context across commands
type DeployContext struct {
    Environment string
    AWSRegion   string
    Verbose     bool
}

// Store context in Before hook
ctx := &DeployContext{...}
c.App.Metadata["ctx"] = ctx

// Retrieve in command
ctx := c.App.Metadata["ctx"].(*DeployContext)
```

---

### 3. API Client CLI Tool (`api-cli/`)

**Purpose**: REST API client with HTTP client sharing and authentication.

**Features**:
- HTTP client sharing via context
- Authentication in Before hook
- Multiple HTTP methods (GET, POST, PUT, DELETE)
- Request timeout configuration
- Token masking for security

**Commands**:
- `get` - GET request with headers
- `post` - POST request with data
- `put` - PUT request with data
- `delete` - DELETE request
- `auth-test` - Test authentication

**Key Patterns**:
```go
// HTTP client in context
type APIContext struct {
    BaseURL    string
    Token      string
    HTTPClient *http.Client
}

// Initialize in Before hook
client := &http.Client{Timeout: timeout}
ctx := &APIContext{
    HTTPClient: client,
    ...
}

// Use in commands
ctx := c.App.Metadata["ctx"].(*APIContext)
resp, err := ctx.HTTPClient.Get(url)
```

---

## Pattern Summary

### Context Management
All three examples demonstrate different context patterns:
- **db-cli**: Connection validation and cleanup
- **deploy-cli**: Shared deployment configuration
- **api-cli**: HTTP client and authentication sharing

### Before/After Hooks
- **Before**: Setup, validation, authentication, connection establishment
- **After**: Cleanup, resource release, connection closing

### Command Categories
Organized command groups for better UX:
- **db-cli**: Schema, Data, Admin
- **deploy-cli**: Build, Deploy, Monitor
- **api-cli**: No categories (simple HTTP verbs)

### Flag Patterns
- Required flags: `--connection`, `--env`, `--token`
- Environment variables: All support env var fallbacks
- Aliases: Short forms (-v, -e, -t)
- Multiple values: StringSlice for headers
- Custom types: Duration for timeouts

### Error Handling
All examples demonstrate:
- Validation in Before hooks
- Proper error returns
- User-friendly error messages
- Exit code handling

## Running the Examples

### Database CLI
```bash
export DATABASE_URL="postgres://user:pass@localhost/mydb"
cd examples/db-cli
go build -o dbctl .
./dbctl migrate
./dbctl backup --output backup.sql
```

### Deployment CLI
```bash
export DEPLOY_ENV=staging
export AWS_REGION=us-east-1
cd examples/deploy-cli
go build -o deploy .
./deploy build --tag v1.0.0
./deploy deploy
```

### API Client CLI
```bash
export API_URL=https://api.example.com
export API_TOKEN=your_token_here
cd examples/api-cli
go build -o api .
./api get /users
./api post /users '{"name":"John"}'
```

## Learning Path

**Beginner**:
1. Start with `db-cli` - demonstrates basic categories and hooks
2. Study Before/After hook patterns
3. Learn flag types and validation

**Intermediate**:
4. Study `deploy-cli` - context management and shared state
5. Learn environment validation
6. Understand confirmation prompts

**Advanced**:
7. Study `api-cli` - HTTP client sharing and authentication
8. Learn complex context patterns
9. Understand resource lifecycle management

## Cross-Language Comparison

Each example can be implemented in other languages:
- **TypeScript**: Use commander.js (see templates/)
- **Python**: Use click or typer (see templates/)
- **Ruby**: Use thor
- **Rust**: Use clap

The patterns translate directly across languages with similar CLI frameworks.
