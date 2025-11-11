/// Builder Pattern Template (Manual API)
///
/// This template demonstrates the builder API for advanced use cases:
/// - Dynamic CLI construction
/// - Runtime configuration
/// - Custom help templates
/// - Complex validation logic
///
/// Note: Prefer derive macros unless you need this level of control.

use clap::{Arg, ArgAction, ArgMatches, Command};
use std::path::PathBuf;

fn build_cli() -> Command {
    Command::new("advanced-cli")
        .version("1.0.0")
        .author("Your Name <you@example.com>")
        .about("Advanced CLI using builder pattern")
        .arg(
            Arg::new("input")
                .short('i')
                .long("input")
                .value_name("FILE")
                .help("Input file to process")
                .required(true)
                .value_parser(clap::value_parser!(PathBuf)),
        )
        .arg(
            Arg::new("output")
                .short('o')
                .long("output")
                .value_name("FILE")
                .help("Output file (optional)")
                .value_parser(clap::value_parser!(PathBuf)),
        )
        .arg(
            Arg::new("verbose")
                .short('v')
                .long("verbose")
                .help("Enable verbose output")
                .action(ArgAction::SetTrue),
        )
        .arg(
            Arg::new("count")
                .short('c')
                .long("count")
                .value_name("NUM")
                .help("Number of items to process")
                .default_value("10")
                .value_parser(clap::value_parser!(usize)),
        )
        .arg(
            Arg::new("format")
                .short('f')
                .long("format")
                .value_name("FORMAT")
                .help("Output format")
                .value_parser(["json", "yaml", "toml"])
                .default_value("json"),
        )
        .arg(
            Arg::new("tags")
                .short('t')
                .long("tag")
                .value_name("TAG")
                .help("Tags to apply (can be specified multiple times)")
                .action(ArgAction::Append),
        )
}

fn process_args(matches: &ArgMatches) {
    let input = matches.get_one::<PathBuf>("input").unwrap();
    let output = matches.get_one::<PathBuf>("output");
    let verbose = matches.get_flag("verbose");
    let count = *matches.get_one::<usize>("count").unwrap();
    let format = matches.get_one::<String>("format").unwrap();
    let tags: Vec<_> = matches
        .get_many::<String>("tags")
        .unwrap_or_default()
        .map(|s| s.as_str())
        .collect();

    if verbose {
        println!("Configuration:");
        println!("  Input: {:?}", input);
        println!("  Output: {:?}", output);
        println!("  Count: {}", count);
        println!("  Format: {}", format);
        println!("  Tags: {:?}", tags);
    }

    // Your processing logic here
    println!("Processing {} items from {}", count, input.display());

    if !tags.is_empty() {
        println!("Applying tags: {}", tags.join(", "));
    }

    if let Some(output_path) = output {
        println!("Writing {} format to {}", format, output_path.display());
    }
}

fn main() {
    let matches = build_cli().get_matches();
    process_args(&matches);
}

// Example usage:
//
// cargo run -- -i input.txt -o output.json -v -c 20 -f yaml -t alpha -t beta
// cargo run -- --input data.txt --format toml --tag important
