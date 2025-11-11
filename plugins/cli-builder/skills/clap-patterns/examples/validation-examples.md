# Clap Validation Examples

Comprehensive examples for validating CLI input with Clap value parsers.

## 1. Port Number Validation

Validate port numbers are in the valid range (1-65535):

```rust
use std::ops::RangeInclusive;

const PORT_RANGE: RangeInclusive<usize> = 1..=65535;

fn port_in_range(s: &str) -> Result<u16, String> {
    let port: usize = s
        .parse()
        .map_err(|_| format!("`{}` isn't a valid port number", s))?;

    if PORT_RANGE.contains(&port) {
        Ok(port as u16)
    } else {
        Err(format!(
            "port not in range {}-{}",
            PORT_RANGE.start(),
            PORT_RANGE.end()
        ))
    }
}

#[derive(Parser)]
struct Cli {
    #[arg(short, long, value_parser = port_in_range)]
    port: u16,
}
```

**Usage:**
```bash
$ my-cli --port 8080      # ✓ Valid
$ my-cli --port 80000     # ❌ Error: port not in range 1-65535
$ my-cli --port abc       # ❌ Error: `abc` isn't a valid port number
```

## 2. Email Validation

Basic email format validation:

```rust
fn validate_email(s: &str) -> Result<String, String> {
    if s.contains('@') && s.contains('.') && s.len() > 5 {
        Ok(s.to_string())
    } else {
        Err(format!("`{}` is not a valid email address", s))
    }
}

#[derive(Parser)]
struct Cli {
    #[arg(short, long, value_parser = validate_email)]
    email: String,
}
```

## 3. File/Directory Existence

Validate that files or directories exist:

```rust
fn file_exists(s: &str) -> Result<PathBuf, String> {
    let path = PathBuf::from(s);
    if path.exists() && path.is_file() {
        Ok(path)
    } else {
        Err(format!("file does not exist: {}", s))
    }
}

fn dir_exists(s: &str) -> Result<PathBuf, String> {
    let path = PathBuf::from(s);
    if path.exists() && path.is_dir() {
        Ok(path)
    } else {
        Err(format!("directory does not exist: {}", s))
    }
}

#[derive(Parser)]
struct Cli {
    #[arg(short, long, value_parser = file_exists)]
    input: PathBuf,

    #[arg(short, long, value_parser = dir_exists)]
    output_dir: PathBuf,
}
```

## 4. URL Validation

Validate URL format:

```rust
fn validate_url(s: &str) -> Result<String, String> {
    if s.starts_with("http://") || s.starts_with("https://") {
        Ok(s.to_string())
    } else {
        Err(format!("`{}` must start with http:// or https://", s))
    }
}

#[derive(Parser)]
struct Cli {
    #[arg(short, long, value_parser = validate_url)]
    endpoint: String,
}
```

## 5. Numeric Range Validation

Use built-in range validation:

```rust
#[derive(Parser)]
struct Cli {
    /// Port (1-65535)
    #[arg(long, value_parser = clap::value_parser!(u16).range(1..=65535))]
    port: u16,

    /// Threads (1-32)
    #[arg(long, value_parser = clap::value_parser!(u8).range(1..=32))]
    threads: u8,

    /// Percentage (0-100)
    #[arg(long, value_parser = clap::value_parser!(u8).range(0..=100))]
    percentage: u8,
}
```

## 6. Regex Pattern Validation

Validate against regex patterns:

```rust
use regex::Regex;

fn validate_version(s: &str) -> Result<String, String> {
    let re = Regex::new(r"^\d+\.\d+\.\d+$").unwrap();
    if re.is_match(s) {
        Ok(s.to_string())
    } else {
        Err(format!("`{}` is not a valid semantic version (e.g., 1.2.3)", s))
    }
}

#[derive(Parser)]
struct Cli {
    #[arg(short, long, value_parser = validate_version)]
    version: String,
}
```

**Note:** Add `regex = "1"` to `Cargo.toml` for this example.

## 7. Multiple Validation Rules

Combine multiple validation rules:

```rust
fn validate_username(s: &str) -> Result<String, String> {
    // Must be 3-20 characters
    if s.len() < 3 || s.len() > 20 {
        return Err("username must be 3-20 characters".to_string());
    }

    // Must start with letter
    if !s.chars().next().unwrap().is_alphabetic() {
        return Err("username must start with a letter".to_string());
    }

    // Only alphanumeric and underscore
    if !s.chars().all(|c| c.is_alphanumeric() || c == '_') {
        return Err("username can only contain letters, numbers, and underscores".to_string());
    }

    Ok(s.to_string())
}

#[derive(Parser)]
struct Cli {
    #[arg(short, long, value_parser = validate_username)]
    username: String,
}
```

## 8. Conditional Validation

Validate based on other arguments:

```rust
#[derive(Parser)]
struct Cli {
    /// Enable SSL
    #[arg(long)]
    ssl: bool,

    /// SSL certificate (required if --ssl is set)
    #[arg(long, required_if_eq("ssl", "true"))]
    cert: Option<PathBuf>,

    /// SSL key (required if --ssl is set)
    #[arg(long, required_if_eq("ssl", "true"))]
    key: Option<PathBuf>,
}
```

## 9. Mutually Exclusive Arguments

Ensure only one option is provided:

```rust
#[derive(Parser)]
struct Cli {
    /// Use JSON format
    #[arg(long, conflicts_with = "yaml")]
    json: bool,

    /// Use YAML format
    #[arg(long, conflicts_with = "json")]
    yaml: bool,
}
```

## 10. Custom Type with FromStr

Implement `FromStr` for automatic parsing:

```rust
use std::str::FromStr;

struct IpPort {
    ip: std::net::IpAddr,
    port: u16,
}

impl FromStr for IpPort {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let parts: Vec<&str> = s.split(':').collect();
        if parts.len() != 2 {
            return Err("format must be IP:PORT (e.g., 127.0.0.1:8080)".to_string());
        }

        let ip = parts[0]
            .parse()
            .map_err(|_| format!("invalid IP address: {}", parts[0]))?;

        let port = parts[1]
            .parse()
            .map_err(|_| format!("invalid port: {}", parts[1]))?;

        Ok(IpPort { ip, port })
    }
}

#[derive(Parser)]
struct Cli {
    /// Bind address (IP:PORT)
    #[arg(short, long)]
    bind: IpPort,
}
```

**Usage:**
```bash
$ my-cli --bind 127.0.0.1:8080    # ✓ Valid
$ my-cli --bind 192.168.1.1:3000  # ✓ Valid
$ my-cli --bind invalid           # ❌ Error
```

## Testing Validation

Use the provided test script:

```bash
bash scripts/test-cli.sh ./target/debug/my-cli validation
```

## Best Practices

1. **Provide Clear Error Messages**: Tell users what went wrong and how to fix it
2. **Validate Early**: Use value parsers instead of validating after parsing
3. **Use Type System**: Leverage Rust's type system for compile-time safety
4. **Document Constraints**: Add constraints to help text
5. **Test Edge Cases**: Test boundary values and invalid inputs

## Resources

- Value parser template: `templates/value-parser.rs`
- Test script: `scripts/test-cli.sh`
- Clap docs: https://docs.rs/clap/latest/clap/
