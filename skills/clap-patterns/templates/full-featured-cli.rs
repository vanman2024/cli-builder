/// Full-Featured CLI Template
///
/// This template combines all patterns:
/// - Parser derive with subcommands
/// - ValueEnum for type-safe options
/// - Environment variable support
/// - Custom value parsers
/// - Global arguments
/// - Comprehensive help text

use clap::{Parser, Subcommand, ValueEnum};
use std::path::PathBuf;

#[derive(Parser)]
#[command(name = "myapp")]
#[command(author = "Your Name <you@example.com>")]
#[command(version = "1.0.0")]
#[command(about = "A full-featured CLI application", long_about = None)]
#[command(propagate_version = true)]
struct Cli {
    /// Configuration file path
    #[arg(short, long, env = "CONFIG_FILE", global = true)]
    config: Option<PathBuf>,

    /// Enable verbose output
    #[arg(short, long, global = true)]
    verbose: bool,

    /// Output format
    #[arg(short, long, value_enum, global = true, default_value_t = Format::Text)]
    format: Format,

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

        /// Project template
        #[arg(short, long, value_enum, default_value_t = Template::Basic)]
        template: Template,

        /// Skip interactive prompts
        #[arg(short = 'y', long)]
        yes: bool,
    },

    /// Build the project
    Build {
        /// Build mode
        #[arg(short, long, value_enum, default_value_t = BuildMode::Debug)]
        mode: BuildMode,

        /// Number of parallel jobs
        #[arg(short, long, value_parser = clap::value_parser!(u8).range(1..=32), default_value_t = 4)]
        jobs: u8,

        /// Target directory
        #[arg(short, long, default_value = "target")]
        target_dir: PathBuf,

        /// Clean before building
        #[arg(long)]
        clean: bool,
    },

    /// Test the project
    Test {
        /// Test name pattern
        pattern: Option<String>,

        /// Run ignored tests
        #[arg(long)]
        ignored: bool,

        /// Number of test threads
        #[arg(long, value_parser = clap::value_parser!(usize).range(1..))]
        test_threads: Option<usize>,

        /// Show output for passing tests
        #[arg(long)]
        nocapture: bool,
    },

    /// Deploy the project
    Deploy {
        /// Deployment environment
        #[arg(value_enum)]
        environment: Environment,

        /// Skip pre-deployment checks
        #[arg(long)]
        skip_checks: bool,

        /// Deployment tag/version
        #[arg(short, long)]
        tag: Option<String>,

        /// Deployment configuration
        #[command(subcommand)]
        config: Option<DeployConfig>,
    },
}

#[derive(Subcommand)]
enum DeployConfig {
    /// Configure database settings
    Database {
        /// Database URL
        #[arg(long, env = "DATABASE_URL")]
        url: String,

        /// Run migrations
        #[arg(long)]
        migrate: bool,
    },

    /// Configure server settings
    Server {
        /// Server host
        #[arg(long, default_value = "0.0.0.0")]
        host: String,

        /// Server port
        #[arg(long, default_value_t = 8080, value_parser = port_in_range)]
        port: u16,

        /// Number of workers
        #[arg(long, default_value_t = 4)]
        workers: usize,
    },
}

#[derive(Copy, Clone, PartialEq, Eq, PartialOrd, Ord, ValueEnum)]
enum Format {
    /// Human-readable text
    Text,
    /// JSON output
    Json,
    /// YAML output
    Yaml,
}

#[derive(Copy, Clone, PartialEq, Eq, PartialOrd, Ord, ValueEnum)]
enum Template {
    /// Basic template
    Basic,
    /// Full-featured template
    Full,
    /// Minimal template
    Minimal,
}

#[derive(Copy, Clone, PartialEq, Eq, PartialOrd, Ord, ValueEnum)]
enum BuildMode {
    /// Debug build with symbols
    Debug,
    /// Release build with optimizations
    Release,
}

#[derive(Copy, Clone, PartialEq, Eq, PartialOrd, Ord, ValueEnum)]
enum Environment {
    /// Development environment
    Dev,
    /// Staging environment
    Staging,
    /// Production environment
    Prod,
}

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

fn main() {
    let cli = Cli::parse();

    if cli.verbose {
        println!("Verbose mode enabled");
        if let Some(config) = &cli.config {
            println!("Using config: {}", config.display());
        }
        println!("Output format: {:?}", cli.format);
    }

    match &cli.command {
        Commands::Init { path, template, yes } => {
            println!("Initializing project at {}", path.display());
            println!("Template: {:?}", template);
            if *yes {
                println!("Skipping prompts");
            }
        }

        Commands::Build {
            mode,
            jobs,
            target_dir,
            clean,
        } => {
            if *clean {
                println!("Cleaning target directory");
            }
            println!("Building in {:?} mode", mode);
            println!("Using {} parallel jobs", jobs);
            println!("Target directory: {}", target_dir.display());
        }

        Commands::Test {
            pattern,
            ignored,
            test_threads,
            nocapture,
        } => {
            println!("Running tests");
            if let Some(pat) = pattern {
                println!("Pattern: {}", pat);
            }
            if *ignored {
                println!("Including ignored tests");
            }
            if let Some(threads) = test_threads {
                println!("Test threads: {}", threads);
            }
            if *nocapture {
                println!("Showing test output");
            }
        }

        Commands::Deploy {
            environment,
            skip_checks,
            tag,
            config,
        } => {
            println!("Deploying to {:?}", environment);
            if *skip_checks {
                println!("⚠️  Skipping pre-deployment checks");
            }
            if let Some(version) = tag {
                println!("Version: {}", version);
            }

            if let Some(deploy_config) = config {
                match deploy_config {
                    DeployConfig::Database { url, migrate } => {
                        println!("Database URL: {}", url);
                        if *migrate {
                            println!("Running migrations");
                        }
                    }
                    DeployConfig::Server { host, port, workers } => {
                        println!("Server: {}:{}", host, port);
                        println!("Workers: {}", workers);
                    }
                }
            }
        }
    }
}

// Example usage:
//
// myapp init --template full
// myapp build --mode release --jobs 8 --clean
// myapp test integration --test-threads 4
// myapp deploy prod --tag v1.0.0 server --host 0.0.0.0 --port 443 --workers 16
