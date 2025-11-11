/// Basic Parser Template with Clap Derive Macros
///
/// This template demonstrates:
/// - Parser derive macro
/// - Argument attributes (short, long, default_value)
/// - PathBuf for file handling
/// - Boolean flags
/// - Doc comments as help text

use clap::Parser;
use std::path::PathBuf;

#[derive(Parser)]
#[command(name = "myapp")]
#[command(author = "Your Name <you@example.com>")]
#[command(version = "1.0.0")]
#[command(about = "A simple CLI application", long_about = None)]
struct Cli {
    /// Input file to process
    #[arg(short, long, value_name = "FILE")]
    input: PathBuf,

    /// Optional output file
    #[arg(short, long)]
    output: Option<PathBuf>,

    /// Enable verbose output
    #[arg(short, long)]
    verbose: bool,

    /// Number of items to process
    #[arg(short = 'c', long, default_value_t = 10)]
    count: usize,

    /// Dry run mode (don't make changes)
    #[arg(short = 'n', long)]
    dry_run: bool,
}

fn main() {
    let cli = Cli::parse();

    if cli.verbose {
        println!("Input file: {:?}", cli.input);
        println!("Output file: {:?}", cli.output);
        println!("Count: {}", cli.count);
        println!("Dry run: {}", cli.dry_run);
    }

    // Check if input file exists
    if !cli.input.exists() {
        eprintln!("Error: Input file does not exist: {:?}", cli.input);
        std::process::exit(1);
    }

    // Your processing logic here
    println!("Processing {} with count {}...", cli.input.display(), cli.count);

    if let Some(output) = cli.output {
        if !cli.dry_run {
            println!("Would write to: {}", output.display());
        } else {
            println!("Dry run: Skipping write to {}", output.display());
        }
    }
}
