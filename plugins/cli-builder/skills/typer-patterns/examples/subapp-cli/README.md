# Sub-Application CLI Example

Multi-level CLI with organized command groups.

## Features

- Three sub-apps: db, server, user
- Shared context via callback
- Global options (--config, --verbose)
- Clean command hierarchy
- Logical command grouping

## Usage

```bash
# Show main help
python cli.py --help

# Show sub-app help
python cli.py db --help
python cli.py server --help
python cli.py user --help

# Database commands
python cli.py db init
python cli.py db migrate --steps 5
python cli.py db seed

# Server commands
python cli.py server start --port 8080
python cli.py server stop
python cli.py server restart

# User commands
python cli.py user create alice --email alice@example.com
python cli.py user create bob --email bob@example.com --admin
python cli.py user list
python cli.py user delete alice

# Global options
python cli.py --verbose db migrate
python cli.py --config prod.yaml server start
```

## Command Structure

```
cli.py
├── db
│   ├── init       - Initialize database
│   ├── migrate    - Run migrations
│   └── seed       - Seed test data
├── server
│   ├── start      - Start server
│   ├── stop       - Stop server
│   └── restart    - Restart server
└── user
    ├── create     - Create user
    ├── delete     - Delete user
    └── list       - List users
```

## Key Patterns

1. **Sub-App Creation**: `db_app = typer.Typer()`
2. **Adding Sub-Apps**: `app.add_typer(db_app, name="db")`
3. **Global Callback**: `@app.callback()` for shared options
4. **Context Sharing**: `ctx.obj` for passing data to sub-commands
5. **Command Organization**: Group related commands in sub-apps

## Benefits

- Clear command hierarchy
- Easier navigation with help text
- Logical grouping of functionality
- Shared configuration across commands
- Scalable structure for large CLIs
