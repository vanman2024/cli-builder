# Database CLI Tool Example

Complete database management CLI demonstrating:
- Command categories (Schema, Data, Admin)
- Before hook for connection validation
- After hook for cleanup
- Required and optional flags
- Environment variable fallbacks

## Usage

```bash
# Set connection string
export DATABASE_URL="postgres://user:pass@localhost/mydb"

# Run migrations
dbctl migrate
dbctl migrate --direction down --steps 2

# Rollback
dbctl rollback

# Seed database
dbctl seed --file seeds/test-data.sql

# Backup and restore
dbctl backup --output backups/db-$(date +%Y%m%d).sql
dbctl restore --input backups/db-20240101.sql

# Admin tasks
dbctl status
dbctl vacuum

# Verbose output
dbctl -v migrate
```

## Features Demonstrated

1. **Command Categories**: Schema, Data, Admin
2. **Global Flags**: --connection, --verbose
3. **Before Hook**: Validates connection before any command
4. **After Hook**: Closes connections after command completes
5. **Required Flags**: backup/restore require file paths
6. **Environment Variables**: DATABASE_URL fallback
7. **Flag Aliases**: -v for --verbose, -d for --direction
