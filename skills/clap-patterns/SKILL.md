---
name: clap-patterns
description: Modern type-safe Rust CLI patterns with Clap derive macros, Parser trait, Subcommand enums, validation, and value parsers. Use when building CLI applications, creating Clap commands, implementing type-safe Rust CLIs, or when user mentions Clap, CLI patterns, Rust command-line, derive macros, Parser trait, Subcommands, or command-line interfaces.
allowed-tools: Read, Write, Edit, Bash
---

# clap-patterns

Provides modern type-safe Rust CLI patterns using Clap 4.x with derive macros, Parser trait, Subcommand enums, custom validation, value parsers, and environment variable integration for building maintainable command-line applications.

## Core Patterns

### 1. Basic Parser with Derive Macros

Use derive macros for automatic CLI parsing with type safety:

```rust
use clap::Parser;

#[derive(Parser)]
#[command(name = "myapp")]
#[command(author, version, about, long_about = None)]
struct Cli {
    /// Input file path
    #[arg(short, long, value_name = "FILE")]
    input: std::path::PathBuf,

    /// Optional output file
    #[arg(short, long)]
    output: Option<std::path::PathBuf>,

    /// Verbose mode
    #[arg(short, long)]
    verbose: bool,

    /// Number of items to process
    #[arg(short, long, default_value_t = 10)]
    count: usize,
}

fn main() {
    let cli = Cli::parse();
    if cli.verbose {
        println!("Processing: {:?}", cli.input);
    }
}
```

### 2. Subcommand Enums

Organize complex CLIs with nested subcommands:

```rust
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "git")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Add files to staging
    Add {
        /// Files to add
        #[arg(value_name = "FILE")]
        files: Vec<String>,
    },
    /// Commit changes
    Commit {
        /// Commit message
        #[arg(short, long)]
        message: String,
    },
}
```

### 3. Value Parsers and Validation

Implement custom parsing and validation:

```rust
use clap::Parser;
use std::ops::RangeInclusive;

const PORT_RANGE: RangeInclusive<usize> = 1..=65535;

fn port_in_range(s: &str) -> Result<u16, String> {
    let port: usize = s
        .parse()
        .map_err(|_| format!("`{s}` isn't a valid port number"))?;
    if PORT_RANGE.contains(&port) {
        Ok(port as u16)
    } else {
        Err(format!("port not in range {}-{}", PORT_RANGE.start(), PORT_RANGE.end()))
    }
}

#[derive(Parser)]
struct Cli {
    /// Port to listen on
    #[arg(short, long, value_parser = port_in_range)]
    port: u16,
}
```

### 4. Environment Variable Integration

Support environment variables with fallback:

```rust
use clap::Parser;

#[derive(Parser)]
struct Cli {
    /// API key (or set API_KEY env var)
    #[arg(long, env = "API_KEY")]
    api_key: String,

    /// Database URL
    #[arg(long, env = "DATABASE_URL")]
    database_url: String,

    /// Optional log level
    #[arg(long, env = "LOG_LEVEL", default_value = "info")]
    log_level: String,
}
```

### 5. ValueEnum for Constrained Choices

Use ValueEnum for type-safe option selection:

```rust
use clap::{Parser, ValueEnum};

#[derive(Copy, Clone, PartialEq, Eq, PartialOrd, Ord, ValueEnum)]
enum Format {
    Json,
    Yaml,
    Toml,
}

#[derive(Parser)]
struct Cli {
    /// Output format
    #[arg(value_enum, short, long, default_value_t = Format::Json)]
    format: Format,
}
```

## Available Templates

The following Rust templates demonstrate Clap patterns:

- **basic-parser.rs**: Simple CLI with Parser derive macro
- **subcommands.rs**: Multi-level subcommand structure
- **value-parser.rs**: Custom validation with value parsers
- **env-variables.rs**: Environment variable integration
- **value-enum.rs**: Type-safe enums for options
- **builder-pattern.rs**: Manual builder API (for complex cases)
- **full-featured-cli.rs**: Complete CLI with all patterns

## Available Scripts

Helper scripts for Clap development:

- **generate-completions.sh**: Generate shell completions (bash, zsh, fish)
- **validate-cargo.sh**: Check Cargo.toml for correct Clap dependencies
- **test-cli.sh**: Test CLI with various argument combinations

## Usage Instructions

1. **Choose the appropriate template** based on your CLI complexity:
   - Simple single-command → `basic-parser.rs`
   - Multiple subcommands → `subcommands.rs`
   - Need validation → `value-parser.rs`
   - Environment config → `env-variables.rs`

2. **Add Clap to Cargo.toml**:
   ```toml
   [dependencies]
   clap = { version = "4.5", features = ["derive", "env"] }
   ```

3. **Implement your CLI** using the selected template as a starting point

4. **Generate completions** using the provided script for better UX

## Best Practices

- Use derive macros for most cases (cleaner, less boilerplate)
- Add help text with doc comments (shows in `--help`)
- Validate early with value parsers
- Use ValueEnum for constrained choices
- Support environment variables for sensitive data
- Provide sensible defaults with `default_value_t`
- Use PathBuf for file/directory arguments
- Add version and author metadata

## Common Patterns

### Multiple Values
```rust
#[arg(short, long, num_args = 1..)]
files: Vec<PathBuf>,
```

### Required Unless Present
```rust
#[arg(long, required_unless_present = "config")]
database_url: Option<String>,
```

### Conflicting Arguments
```rust
#[arg(long, conflicts_with = "json")]
yaml: bool,
```

### Global Arguments (for subcommands)
```rust
#[arg(global = true, short, long)]
verbose: bool,
```

## Testing Your CLI

Run the test script to validate your CLI:

```bash
bash scripts/test-cli.sh your-binary
```

This tests:
- Help output (`--help`)
- Version flag (`--version`)
- Invalid arguments
- Subcommand routing
- Environment variable precedence

## References

- Templates: `skills/clap-patterns/templates/`
- Scripts: `skills/clap-patterns/scripts/`
- Examples: `skills/clap-patterns/examples/`
- Clap Documentation: https://docs.rs/clap/latest/clap/
