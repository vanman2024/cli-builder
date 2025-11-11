# Real-World Clap CLI Example

A complete, production-ready CLI application demonstrating best practices.

## Project Structure

```
my-tool/
├── Cargo.toml
├── src/
│   ├── main.rs           # CLI definition and entry point
│   ├── commands/         # Command implementations
│   │   ├── mod.rs
│   │   ├── init.rs
│   │   ├── build.rs
│   │   └── deploy.rs
│   ├── config.rs         # Configuration management
│   └── utils.rs          # Helper functions
├── tests/
│   └── cli_tests.rs      # Integration tests
└── completions/          # Generated shell completions
```

## Cargo.toml

```toml
[package]
name = "my-tool"
version = "1.0.0"
edition = "2021"

[dependencies]
clap = { version = "4.5", features = ["derive", "env", "cargo"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
anyhow = "1.0"
tokio = { version = "1", features = ["full"] }
colored = "2.0"

[dev-dependencies]
assert_cmd = "2.0"
predicates = "3.0"
```

## main.rs - Complete CLI Definition

```rust
use clap::{Parser, Subcommand, ValueEnum};
use std::path::PathBuf;

mod commands;
mod config;
mod utils;

#[derive(Parser)]
#[command(name = "my-tool")]
#[command(author, version, about = "A production-ready CLI tool", long_about = None)]
#[command(propagate_version = true)]
struct Cli {
    /// Configuration file
    #[arg(
        short,
        long,
        env = "MY_TOOL_CONFIG",
        global = true,
        default_value = "config.json"
    )]
    config: PathBuf,

    /// Enable verbose output
    #[arg(short, long, global = true)]
    verbose: bool,

    /// Output format
    #[arg(short = 'F', long, value_enum, global = true, default_value_t = OutputFormat::Text)]
    format: OutputFormat,

    /// Log file path
    #[arg(long, env = "MY_TOOL_LOG", global = true)]
    log_file: Option<PathBuf>,

    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Initialize a new project
    Init {
        /// Project directory
        #[arg(default_value = ".")]
        path: PathBuf,

        /// Project name
        #[arg(short, long)]
        name: Option<String>,

        /// Project template
        #[arg(short, long, value_enum, default_value_t = Template::Default)]
        template: Template,

        /// Skip interactive prompts
        #[arg(short = 'y', long)]
        yes: bool,

        /// Git repository URL
        #[arg(short, long)]
        git: Option<String>,
    },

    /// Build the project
    Build {
        /// Build profile
        #[arg(short, long, value_enum, default_value_t = Profile::Debug)]
        profile: Profile,

        /// Number of parallel jobs
        #[arg(short, long, value_parser = clap::value_parser!(u8).range(1..=32), default_value_t = 4)]
        jobs: u8,

        /// Target directory
        #[arg(short, long, default_value = "target")]
        target: PathBuf,

        /// Clean before building
        #[arg(long)]
        clean: bool,

        /// Watch for changes
        #[arg(short, long)]
        watch: bool,
    },

    /// Deploy to environment
    Deploy {
        /// Target environment
        #[arg(value_enum)]
        environment: Environment,

        /// Deployment version/tag
        #[arg(short, long)]
        version: String,

        /// Dry run (don't actually deploy)
        #[arg(short = 'n', long)]
        dry_run: bool,

        /// Skip pre-deployment checks
        #[arg(long)]
        skip_checks: bool,

        /// Deployment timeout in seconds
        #[arg(short, long, default_value_t = 300)]
        timeout: u64,

        /// Rollback on failure
        #[arg(long)]
        rollback: bool,
    },

    /// Manage configuration
    Config {
        #[command(subcommand)]
        action: ConfigAction,
    },

    /// Generate shell completions
    Completions {
        /// Shell type
        #[arg(value_enum)]
        shell: Shell,

        /// Output directory
        #[arg(short, long, default_value = "completions")]
        output: PathBuf,
    },
}

#[derive(Subcommand)]
enum ConfigAction {
    /// Show current configuration
    Show,

    /// Set a configuration value
    Set {
        /// Configuration key
        key: String,

        /// Configuration value
        value: String,
    },

    /// Get a configuration value
    Get {
        /// Configuration key
        key: String,
    },

    /// Reset configuration to defaults
    Reset {
        /// Confirm reset
        #[arg(short = 'y', long)]
        yes: bool,
    },
}

#[derive(Copy, Clone, PartialEq, Eq, PartialOrd, Ord, ValueEnum)]
enum OutputFormat {
    Text,
    Json,
    Yaml,
}

#[derive(Copy, Clone, PartialEq, Eq, PartialOrd, Ord, ValueEnum)]
enum Template {
    Default,
    Minimal,
    Full,
}

#[derive(Copy, Clone, PartialEq, Eq, PartialOrd, Ord, ValueEnum)]
enum Profile {
    Debug,
    Release,
}

#[derive(Copy, Clone, PartialEq, Eq, PartialOrd, Ord, ValueEnum)]
enum Environment {
    Dev,
    Staging,
    Prod,
}

#[derive(Copy, Clone, PartialEq, Eq, PartialOrd, Ord, ValueEnum)]
enum Shell {
    Bash,
    Zsh,
    Fish,
    PowerShell,
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let cli = Cli::parse();

    // Initialize logging
    if let Some(log_file) = &cli.log_file {
        utils::init_file_logging(log_file, cli.verbose)?;
    } else {
        utils::init_console_logging(cli.verbose);
    }

    // Load configuration
    let config = config::load(&cli.config)?;

    // Execute command
    match &cli.command {
        Commands::Init {
            path,
            name,
            template,
            yes,
            git,
        } => {
            commands::init::execute(path, name.as_deref(), *template, *yes, git.as_deref()).await?;
        }

        Commands::Build {
            profile,
            jobs,
            target,
            clean,
            watch,
        } => {
            commands::build::execute(*profile, *jobs, target, *clean, *watch).await?;
        }

        Commands::Deploy {
            environment,
            version,
            dry_run,
            skip_checks,
            timeout,
            rollback,
        } => {
            commands::deploy::execute(
                *environment,
                version,
                *dry_run,
                *skip_checks,
                *timeout,
                *rollback,
            )
            .await?;
        }

        Commands::Config { action } => match action {
            ConfigAction::Show => config::show(&config, cli.format),
            ConfigAction::Set { key, value } => config::set(&cli.config, key, value)?,
            ConfigAction::Get { key } => config::get(&config, key, cli.format)?,
            ConfigAction::Reset { yes } => config::reset(&cli.config, *yes)?,
        },

        Commands::Completions { shell, output } => {
            commands::completions::generate(*shell, output)?;
        }
    }

    Ok(())
}
```

## Key Features Demonstrated

### 1. Global Arguments

Arguments available to all subcommands:

```rust
#[arg(short, long, global = true)]
verbose: bool,
```

### 2. Environment Variables

Fallback to environment variables:

```rust
#[arg(short, long, env = "MY_TOOL_CONFIG")]
config: PathBuf,
```

### 3. Validation

Numeric range validation:

```rust
#[arg(short, long, value_parser = clap::value_parser!(u8).range(1..=32))]
jobs: u8,
```

### 4. Type-Safe Enums

Constrained choices with ValueEnum:

```rust
#[derive(ValueEnum)]
enum Environment {
    Dev,
    Staging,
    Prod,
}
```

### 5. Nested Subcommands

Multi-level command structure:

```rust
Config {
    #[command(subcommand)]
    action: ConfigAction,
}
```

### 6. Default Values

Sensible defaults for all options:

```rust
#[arg(short, long, default_value = "config.json")]
config: PathBuf,
```

## Integration Tests

`tests/cli_tests.rs`:

```rust
use assert_cmd::Command;
use predicates::prelude::*;

#[test]
fn test_help() {
    let mut cmd = Command::cargo_bin("my-tool").unwrap();
    cmd.arg("--help")
        .assert()
        .success()
        .stdout(predicate::str::contains("A production-ready CLI tool"));
}

#[test]
fn test_version() {
    let mut cmd = Command::cargo_bin("my-tool").unwrap();
    cmd.arg("--version")
        .assert()
        .success()
        .stdout(predicate::str::contains("1.0.0"));
}

#[test]
fn test_init_command() {
    let mut cmd = Command::cargo_bin("my-tool").unwrap();
    cmd.arg("init")
        .arg("--name")
        .arg("test-project")
        .arg("--yes")
        .assert()
        .success();
}
```

## Building for Production

```bash
# Build release binary
cargo build --release

# Run tests
cargo test

# Generate completions
./target/release/my-tool completions bash
./target/release/my-tool completions zsh
./target/release/my-tool completions fish

# Install locally
cargo install --path .
```

## Distribution

### Cross-Platform Binaries

Use `cross` for cross-compilation:

```bash
cargo install cross
cross build --release --target x86_64-unknown-linux-gnu
cross build --release --target x86_64-pc-windows-gnu
cross build --release --target x86_64-apple-darwin
```

### Package for Distribution

```bash
# Linux/macOS tar.gz
tar czf my-tool-linux-x64.tar.gz -C target/release my-tool

# Windows zip
zip my-tool-windows-x64.zip target/release/my-tool.exe
```

## Best Practices Checklist

- ✓ Clear, descriptive help text
- ✓ Sensible default values
- ✓ Environment variable support
- ✓ Input validation
- ✓ Type-safe options (ValueEnum)
- ✓ Global arguments for common options
- ✓ Proper error handling (anyhow)
- ✓ Integration tests
- ✓ Shell completion generation
- ✓ Version information
- ✓ Verbose/quiet modes
- ✓ Configuration file support
- ✓ Dry-run mode for destructive operations

## Resources

- Full templates: `skills/clap-patterns/templates/`
- Validation examples: `examples/validation-examples.md`
- Test scripts: `scripts/test-cli.sh`
