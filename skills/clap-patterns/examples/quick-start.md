# Clap Quick Start Guide

This guide will help you build your first Clap CLI application in minutes.

## Prerequisites

- Rust installed (1.70.0 or newer)
- Cargo (comes with Rust)

## Step 1: Create a New Project

```bash
cargo new my-cli
cd my-cli
```

## Step 2: Add Clap Dependency

Edit `Cargo.toml`:

```toml
[dependencies]
clap = { version = "4.5", features = ["derive"] }
```

## Step 3: Write Your First CLI

Replace `src/main.rs` with:

```rust
use clap::Parser;

/// Simple program to greet a person
#[derive(Parser)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Name of the person to greet
    #[arg(short, long)]
    name: String,

    /// Number of times to greet
    #[arg(short, long, default_value_t = 1)]
    count: u8,
}

fn main() {
    let args = Args::parse();

    for _ in 0..args.count {
        println!("Hello {}!", args.name)
    }
}
```

## Step 4: Build and Run

```bash
# Build the project
cargo build --release

# Run with arguments
./target/release/my-cli --name Alice --count 3

# Check help output
./target/release/my-cli --help
```

## Expected Output

```
$ ./target/release/my-cli --name Alice --count 3
Hello Alice!
Hello Alice!
Hello Alice!
```

## Help Output

```
$ ./target/release/my-cli --help
Simple program to greet a person

Usage: my-cli --name <NAME> [--count <COUNT>]

Options:
  -n, --name <NAME>     Name of the person to greet
  -c, --count <COUNT>   Number of times to greet [default: 1]
  -h, --help            Print help
  -V, --version         Print version
```

## Next Steps

1. **Add Subcommands**: See `subcommands.rs` template
2. **Add Validation**: See `value-parser.rs` template
3. **Environment Variables**: See `env-variables.rs` template
4. **Type-Safe Options**: See `value-enum.rs` template

## Common Patterns

### Optional Arguments

```rust
#[arg(short, long)]
output: Option<String>,
```

### Multiple Values

```rust
#[arg(short, long, num_args = 1..)]
files: Vec<PathBuf>,
```

### Boolean Flags

```rust
#[arg(short, long)]
verbose: bool,
```

### With Default Value

```rust
#[arg(short, long, default_value = "config.toml")]
config: String,
```

### Required Unless Present

```rust
#[arg(long, required_unless_present = "config")]
database_url: Option<String>,
```

## Troubleshooting

### "Parser trait not found"

Add the import:
```rust
use clap::Parser;
```

### "derive feature not enabled"

Update `Cargo.toml`:
```toml
clap = { version = "4.5", features = ["derive"] }
```

### Help text not showing

Add doc comments above fields:
```rust
/// This shows up in --help output
#[arg(short, long)]
```

## Resources

- Full templates: `skills/clap-patterns/templates/`
- Helper scripts: `skills/clap-patterns/scripts/`
- Official docs: https://docs.rs/clap/latest/clap/
