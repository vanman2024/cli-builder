#!/usr/bin/env node
/**
 * argparse patterns translated to commander.js
 *
 * Shows equivalent patterns between Python argparse and Node.js commander
 *
 * Usage:
 *   npm install commander
 *   node argparse-to-commander.ts deploy production --force
 */

import { Command, Option } from 'commander';

const program = new Command();

// ===== Basic Configuration (like ArgumentParser) =====
program
  .name('mycli')
  .description('A powerful CLI tool')
  .version('1.0.0');

// ===== Subcommands (like add_subparsers) =====

// Init command (like subparsers.add_parser('init'))
program
  .command('init')
  .description('Initialize a new project')
  .option('-t, --template <type>', 'project template', 'basic')
  .option('-p, --path <path>', 'project path', '.')
  .action((options) => {
    console.log(`Initializing project with ${options.template} template...`);
    console.log(`Path: ${options.path}`);
  });

// Deploy command with choices (like choices=[...])
program
  .command('deploy <environment>')
  .description('Deploy to specified environment')
  .addOption(
    new Option('-m, --mode <mode>', 'deployment mode')
      .choices(['fast', 'safe', 'rollback'])
      .default('safe')
  )
  .option('-f, --force', 'force deployment', false)
  .action((environment, options) => {
    console.log(`Deploying to ${environment} in ${options.mode} mode`);
    if (options.force) {
      console.log('Warning: Force mode enabled');
    }
  });

// ===== Nested Subcommands (like nested add_subparsers) =====
const config = program
  .command('config')
  .description('Manage configuration');

config
  .command('get <key>')
  .description('Get configuration value')
  .action((key) => {
    console.log(`Getting config: ${key}`);
  });

config
  .command('set <key> <value>')
  .description('Set configuration value')
  .option('-f, --force', 'overwrite existing value')
  .action((key, value, options) => {
    console.log(`Setting ${key} = ${value}`);
    if (options.force) {
      console.log('(Overwriting existing value)');
    }
  });

config
  .command('list')
  .description('List all configuration values')
  .option('--format <format>', 'output format', 'text')
  .action((options) => {
    console.log(`Listing configuration (format: ${options.format})`);
  });

// ===== Boolean Flags (like action='store_true') =====
program
  .command('build')
  .description('Build the project')
  .option('--verbose', 'enable verbose output')
  .option('--debug', 'enable debug mode')
  .option('--no-cache', 'disable cache (enabled by default)')
  .action((options) => {
    console.log('Building project...');
    console.log(`Verbose: ${options.verbose || false}`);
    console.log(`Debug: ${options.debug || false}`);
    console.log(`Cache: ${options.cache}`);
  });

// ===== Type Coercion (like type=int, type=float) =====
program
  .command('server')
  .description('Start server')
  .option('-p, --port <number>', 'server port', parseInt, 8080)
  .option('-t, --timeout <seconds>', 'timeout in seconds', parseFloat, 30.0)
  .option('-w, --workers <number>', 'number of workers', parseInt, 4)
  .action((options) => {
    console.log(`Starting server on port ${options.port}`);
    console.log(`Timeout: ${options.timeout}s`);
    console.log(`Workers: ${options.workers}`);
  });

// ===== Variadic Arguments (like nargs='+') =====
program
  .command('process <files...>')
  .description('Process multiple files')
  .option('--format <format>', 'output format', 'json')
  .action((files, options) => {
    console.log(`Processing ${files.length} file(s):`);
    files.forEach((file) => console.log(`  - ${file}`));
    console.log(`Output format: ${options.format}`);
  });

// ===== Mutually Exclusive Options =====
// Note: Commander doesn't have built-in mutually exclusive groups
// You need to validate manually
program
  .command('export')
  .description('Export data')
  .option('--json <file>', 'export as JSON')
  .option('--yaml <file>', 'export as YAML')
  .option('--xml <file>', 'export as XML')
  .action((options) => {
    const formats = [options.json, options.yaml, options.xml].filter(Boolean);
    if (formats.length > 1) {
      console.error('Error: --json, --yaml, and --xml are mutually exclusive');
      process.exit(1);
    }

    if (options.json) {
      console.log(`Exporting as JSON to ${options.json}`);
    } else if (options.yaml) {
      console.log(`Exporting as YAML to ${options.yaml}`);
    } else if (options.xml) {
      console.log(`Exporting as XML to ${options.xml}`);
    }
  });

// ===== Required Options (like required=True) =====
program
  .command('login')
  .description('Login to service')
  .requiredOption('--username <username>', 'username for authentication')
  .requiredOption('--password <password>', 'password for authentication')
  .option('--token <token>', 'authentication token (alternative to password)')
  .action((options) => {
    console.log(`Logging in as ${options.username}`);
  });

// ===== Custom Validation =====
function validatePort(value: string): number {
  const port = parseInt(value, 10);
  if (isNaN(port) || port < 1 || port > 65535) {
    throw new Error(`Invalid port: ${value} (must be 1-65535)`);
  }
  return port;
}

program
  .command('connect')
  .description('Connect to server')
  .option('-p, --port <number>', 'server port', validatePort, 8080)
  .action((options) => {
    console.log(`Connecting to port ${options.port}`);
  });

// ===== Argument Groups (display organization) =====
// Note: Commander doesn't have argument groups for help display
// You can organize with comments or separate commands

// ===== Parse Arguments =====
program.parse();

/**
 * COMPARISON SUMMARY:
 *
 * argparse Pattern                 | commander.js Equivalent
 * ---------------------------------|--------------------------------
 * ArgumentParser()                 | new Command()
 * add_argument()                   | .option() or .argument()
 * add_subparsers()                 | .command()
 * choices=[...]                    | .choices([...])
 * action='store_true'              | .option('--flag')
 * action='store_false'             | .option('--no-flag')
 * type=int                         | parseInt
 * type=float                       | parseFloat
 * nargs='+'                        | <arg...>
 * nargs='*'                        | [arg...]
 * required=True                    | .requiredOption()
 * default=value                    | option(..., default)
 * help='...'                       | .description('...')
 * mutually_exclusive_group()       | Manual validation
 * add_argument_group()             | Organize with subcommands
 */
