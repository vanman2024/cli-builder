/// ValueEnum Template for Type-Safe Options
///
/// This template demonstrates:
/// - ValueEnum trait for constrained choices
/// - Type-safe option selection
/// - Automatic validation and help text
/// - Pattern matching on enums

use clap::{Parser, ValueEnum};

/// Output format options
#[derive(Copy, Clone, PartialEq, Eq, PartialOrd, Ord, ValueEnum)]
enum Format {
    /// JavaScript Object Notation
    Json,
    /// YAML Ain't Markup Language
    Yaml,
    /// Tom's Obvious, Minimal Language
    Toml,
    /// Comma-Separated Values
    Csv,
}

/// Log level options
#[derive(Copy, Clone, PartialEq, Eq, PartialOrd, Ord, ValueEnum)]
enum LogLevel {
    /// Detailed debug information
    Debug,
    /// General information
    Info,
    /// Warning messages
    Warn,
    /// Error messages only
    Error,
}

/// Color output mode
#[derive(Copy, Clone, PartialEq, Eq, PartialOrd, Ord, ValueEnum)]
enum ColorMode {
    /// Always use colors
    Always,
    /// Never use colors
    Never,
    /// Automatically detect (default)
    Auto,
}

#[derive(Parser)]
#[command(name = "converter")]
#[command(about = "Convert data between formats with type-safe options")]
struct Cli {
    /// Input file
    input: std::path::PathBuf,

    /// Output format
    #[arg(short, long, value_enum, default_value_t = Format::Json)]
    format: Format,

    /// Log level
    #[arg(short, long, value_enum, default_value_t = LogLevel::Info)]
    log_level: LogLevel,

    /// Color mode for output
    #[arg(long, value_enum, default_value_t = ColorMode::Auto)]
    color: ColorMode,

    /// Pretty print output (for supported formats)
    #[arg(short, long)]
    pretty: bool,
}

fn main() {
    let cli = Cli::parse();

    // Configure logging based on log level
    match cli.log_level {
        LogLevel::Debug => println!("🔍 Debug logging enabled"),
        LogLevel::Info => println!("ℹ️  Info logging enabled"),
        LogLevel::Warn => println!("⚠️  Warning logging enabled"),
        LogLevel::Error => println!("❌ Error logging only"),
    }

    // Check color mode
    let use_colors = match cli.color {
        ColorMode::Always => true,
        ColorMode::Never => false,
        ColorMode::Auto => atty::is(atty::Stream::Stdout),
    };

    if use_colors {
        println!("🎨 Color output enabled");
    }

    // Process based on format
    println!("Converting {} to {:?}", cli.input.display(), cli.format);

    match cli.format {
        Format::Json => {
            println!("Converting to JSON{}", if cli.pretty { " (pretty)" } else { "" });
            // JSON conversion logic here
        }
        Format::Yaml => {
            println!("Converting to YAML");
            // YAML conversion logic here
        }
        Format::Toml => {
            println!("Converting to TOML");
            // TOML conversion logic here
        }
        Format::Csv => {
            println!("Converting to CSV");
            // CSV conversion logic here
        }
    }

    println!("✓ Conversion complete");
}

// Helper function to check if stdout is a terminal (for color auto-detection)
mod atty {
    pub enum Stream {
        Stdout,
    }

    pub fn is(_stream: Stream) -> bool {
        // Simple implementation - checks if stdout is a TTY
        #[cfg(unix)]
        {
            unsafe { libc::isatty(libc::STDOUT_FILENO) != 0 }
        }

        #[cfg(not(unix))]
        {
            false
        }
    }
}

// Example usage:
//
// cargo run -- input.txt --format json --log-level debug
// cargo run -- data.yml --format toml --color always --pretty
// cargo run -- config.json --format yaml --log-level warn
