/// Value Parser Template with Custom Validation
///
/// This template demonstrates:
/// - Custom value parsers
/// - Range validation
/// - Format validation (regex)
/// - Error handling with helpful messages

use clap::Parser;
use std::ops::RangeInclusive;

const PORT_RANGE: RangeInclusive<usize> = 1..=65535;

/// Parse and validate port number
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

/// Validate email format (basic validation)
fn validate_email(s: &str) -> Result<String, String> {
    if s.contains('@') && s.contains('.') && s.len() > 5 {
        Ok(s.to_string())
    } else {
        Err(format!("`{}` is not a valid email address", s))
    }
}

/// Parse percentage (0-100)
fn parse_percentage(s: &str) -> Result<u8, String> {
    let value: u8 = s
        .parse()
        .map_err(|_| format!("`{}` isn't a valid number", s))?;

    if value <= 100 {
        Ok(value)
    } else {
        Err("percentage must be between 0 and 100".to_string())
    }
}

/// Validate directory exists
fn validate_directory(s: &str) -> Result<std::path::PathBuf, String> {
    let path = std::path::PathBuf::from(s);

    if path.exists() && path.is_dir() {
        Ok(path)
    } else {
        Err(format!("directory does not exist: {}", s))
    }
}

#[derive(Parser)]
#[command(name = "validator")]
#[command(about = "CLI with custom value parsers and validation")]
struct Cli {
    /// Port number (1-65535)
    #[arg(short, long, value_parser = port_in_range)]
    port: u16,

    /// Email address
    #[arg(short, long, value_parser = validate_email)]
    email: String,

    /// Success threshold percentage (0-100)
    #[arg(short, long, value_parser = parse_percentage, default_value = "80")]
    threshold: u8,

    /// Working directory (must exist)
    #[arg(short, long, value_parser = validate_directory)]
    workdir: Option<std::path::PathBuf>,

    /// Number of retries (1-10)
    #[arg(
        short,
        long,
        default_value = "3",
        value_parser = clap::value_parser!(u8).range(1..=10)
    )]
    retries: u8,
}

fn main() {
    let cli = Cli::parse();

    println!("Configuration:");
    println!("  Port: {}", cli.port);
    println!("  Email: {}", cli.email);
    println!("  Threshold: {}%", cli.threshold);
    println!("  Retries: {}", cli.retries);

    if let Some(workdir) = cli.workdir {
        println!("  Working directory: {}", workdir.display());
    }

    // Your application logic here
    println!("\nValidation passed! All inputs are valid.");
}
