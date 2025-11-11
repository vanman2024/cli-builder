/// Subcommand Template with Clap
///
/// This template demonstrates:
/// - Subcommand derive macro
/// - Nested command structure
/// - Per-subcommand arguments
/// - Enum-based command routing

use clap::{Parser, Subcommand};
use std::path::PathBuf;

#[derive(Parser)]
#[command(name = "git-like")]
#[command(author, version, about, long_about = None)]
#[command(propagate_version = true)]
struct Cli {
    /// Enable verbose output
    #[arg(global = true, short, long)]
    verbose: bool,

    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Initialize a new repository
    Init {
        /// Directory to initialize
        #[arg(value_name = "DIR", default_value = ".")]
        path: PathBuf,

        /// Create a bare repository
        #[arg(long)]
        bare: bool,
    },

    /// Add files to staging area
    Add {
        /// Files to add
        #[arg(value_name = "FILE", required = true)]
        files: Vec<PathBuf>,

        /// Add all files
        #[arg(short = 'A', long)]
        all: bool,
    },

    /// Commit staged changes
    Commit {
        /// Commit message
        #[arg(short, long)]
        message: String,

        /// Amend previous commit
        #[arg(long)]
        amend: bool,
    },

    /// Remote repository operations
    Remote {
        #[command(subcommand)]
        command: RemoteCommands,
    },
}

#[derive(Subcommand)]
enum RemoteCommands {
    /// Add a new remote
    Add {
        /// Remote name
        name: String,

        /// Remote URL
        url: String,
    },

    /// Remove a remote
    Remove {
        /// Remote name
        name: String,
    },

    /// List all remotes
    List {
        /// Show URLs
        #[arg(short, long)]
        verbose: bool,
    },
}

fn main() {
    let cli = Cli::parse();

    match &cli.command {
        Commands::Init { path, bare } => {
            if cli.verbose {
                println!("Initializing repository at {:?}", path);
            }
            println!(
                "Initialized {} repository in {}",
                if *bare { "bare" } else { "normal" },
                path.display()
            );
        }

        Commands::Add { files, all } => {
            if *all {
                println!("Adding all files");
            } else {
                println!("Adding {} file(s)", files.len());
                if cli.verbose {
                    for file in files {
                        println!("  - {}", file.display());
                    }
                }
            }
        }

        Commands::Commit { message, amend } => {
            if *amend {
                println!("Amending previous commit");
            }
            println!("Committing with message: {}", message);
        }

        Commands::Remote { command } => match command {
            RemoteCommands::Add { name, url } => {
                println!("Adding remote '{}' -> {}", name, url);
            }
            RemoteCommands::Remove { name } => {
                println!("Removing remote '{}'", name);
            }
            RemoteCommands::List { verbose } => {
                println!("Listing remotes{}", if *verbose { " (verbose)" } else { "" });
            }
        },
    }
}
