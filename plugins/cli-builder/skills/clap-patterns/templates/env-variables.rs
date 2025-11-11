/// Environment Variable Integration Template
///
/// This template demonstrates:
/// - Reading from environment variables
/// - Fallback to CLI arguments
/// - Default values
/// - Sensitive data handling (API keys, tokens)

use clap::Parser;
use std::path::PathBuf;

#[derive(Parser)]
#[command(name = "envapp")]
#[command(about = "CLI with environment variable support")]
struct Cli {
    /// API key (or set API_KEY env var)
    ///
    /// Sensitive data like API keys should preferably be set via environment
    /// variables to avoid exposing them in shell history or process lists.
    #[arg(long, env = "API_KEY", hide_env_values = true)]
    api_key: String,

    /// Database URL (or set DATABASE_URL env var)
    #[arg(long, env = "DATABASE_URL")]
    database_url: String,

    /// Log level: debug, info, warn, error
    ///
    /// Defaults to "info" if not provided via CLI or LOG_LEVEL env var.
    #[arg(long, env = "LOG_LEVEL", default_value = "info")]
    log_level: String,

    /// Configuration file path
    ///
    /// Reads from CONFIG_FILE env var, or uses default if not specified.
    #[arg(long, env = "CONFIG_FILE", default_value = "config.toml")]
    config: PathBuf,

    /// Number of workers (default from env or 4)
    #[arg(long, env = "WORKER_COUNT", default_value_t = 4)]
    workers: usize,

    /// Enable debug mode
    ///
    /// Can be set via DEBUG=1 or --debug flag
    #[arg(long, env = "DEBUG", value_parser = clap::value_parser!(bool))]
    debug: bool,

    /// Host to bind to
    #[arg(long, env = "HOST", default_value = "127.0.0.1")]
    host: String,

    /// Port to listen on
    #[arg(short, long, env = "PORT", default_value_t = 8080)]
    port: u16,
}

fn main() {
    let cli = Cli::parse();

    println!("Configuration loaded:");
    println!("  Database URL: {}", cli.database_url);
    println!("  API Key: {}...", &cli.api_key[..4.min(cli.api_key.len())]);
    println!("  Log level: {}", cli.log_level);
    println!("  Config file: {}", cli.config.display());
    println!("  Workers: {}", cli.workers);
    println!("  Debug mode: {}", cli.debug);
    println!("  Host: {}", cli.host);
    println!("  Port: {}", cli.port);

    // Initialize logging based on log_level
    match cli.log_level.to_lowercase().as_str() {
        "debug" => println!("Log level set to DEBUG"),
        "info" => println!("Log level set to INFO"),
        "warn" => println!("Log level set to WARN"),
        "error" => println!("Log level set to ERROR"),
        _ => println!("Unknown log level: {}", cli.log_level),
    }

    // Your application logic here
    println!("\nStarting application...");
    println!("Listening on {}:{}", cli.host, cli.port);
}

// Example usage:
//
// 1. Set environment variables:
//    export API_KEY="sk-1234567890abcdef"
//    export DATABASE_URL="postgres://localhost/mydb"
//    export LOG_LEVEL="debug"
//    export WORKER_COUNT="8"
//    cargo run
//
// 2. Override with CLI arguments:
//    cargo run -- --api-key "other-key" --workers 16
//
// 3. Mix environment and CLI:
//    export DATABASE_URL="postgres://localhost/mydb"
//    cargo run -- --api-key "sk-1234" --debug
