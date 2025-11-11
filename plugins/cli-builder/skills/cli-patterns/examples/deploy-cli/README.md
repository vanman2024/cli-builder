# Deployment CLI Tool Example

Complete deployment automation CLI demonstrating:
- Context management with shared state
- Environment validation in Before hook
- Command categories (Build, Deploy, Monitor)
- Confirmation prompts for destructive actions

## Usage

```bash
# Set environment variables
export DEPLOY_ENV=staging
export AWS_REGION=us-west-2

# Build application
deploy --env staging build
deploy -e production build --tag v1.2.3

# Run tests
deploy --env staging test

# Deploy
deploy --env staging deploy
deploy -e production deploy --auto-approve

# Rollback
deploy --env production rollback

# Monitor
deploy --env production logs --follow
deploy -e staging status
```

## Features Demonstrated

1. **Context Management**: Shared DeployContext across commands
2. **Environment Validation**: Before hook validates target environment
3. **Required Flags**: --env is required for all operations
4. **Confirmation Prompts**: Deploy asks for confirmation (unless --auto-approve)
5. **Command Categories**: Build, Deploy, Monitor
6. **Environment Variables**: DEPLOY_ENV, AWS_REGION fallbacks
7. **Shared State**: Context passed to all commands via metadata

## Context Pattern

```go
type DeployContext struct {
    Environment string
    AWSRegion   string
    Verbose     bool
}

// Store in Before hook
ctx := &DeployContext{...}
c.App.Metadata["ctx"] = ctx

// Retrieve in command
ctx := c.App.Metadata["ctx"].(*DeployContext)
```
