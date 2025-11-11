#!/usr/bin/env node
import { Command, Option } from 'commander';
import chalk from 'chalk';
import ora from 'ora';

const program = new Command();

// Configure main program
program
  .name('mycli')
  .description('A powerful CLI tool with all Commander.js features')
  .version('1.0.0')
  .option('-c, --config <path>', 'config file path', './config.json')
  .option('-v, --verbose', 'verbose output', false)
  .option('--no-color', 'disable colored output');

// Init command
program
  .command('init')
  .description('Initialize a new project')
  .option('-t, --template <type>', 'project template', 'basic')
  .option('-d, --directory <path>', 'target directory', '.')
  .option('-f, --force', 'overwrite existing files', false)
  .action(async (options) => {
    const spinner = ora('Initializing project...').start();

    try {
      await new Promise((resolve) => setTimeout(resolve, 1000));

      spinner.text = 'Creating directory structure...';
      await new Promise((resolve) => setTimeout(resolve, 500));

      spinner.text = 'Copying template files...';
      await new Promise((resolve) => setTimeout(resolve, 500));

      spinner.text = 'Installing dependencies...';
      await new Promise((resolve) => setTimeout(resolve, 1000));

      spinner.succeed(chalk.green('Project initialized successfully!'));

      console.log(chalk.blue('\nNext steps:'));
      console.log(`  cd ${options.directory}`);
      console.log('  mycli dev');
    } catch (error) {
      spinner.fail(chalk.red('Initialization failed'));
      throw error;
    }
  });

// Dev command
program
  .command('dev')
  .description('Start development server')
  .option('-p, --port <port>', 'server port', '3000')
  .option('-h, --host <host>', 'server host', 'localhost')
  .option('--open', 'open browser automatically', false)
  .action((options) => {
    console.log(chalk.blue('Starting development server...'));
    console.log(`Server running at http://${options.host}:${options.port}`);

    if (options.open) {
      console.log(chalk.gray('Opening browser...'));
    }
  });

// Build command
program
  .command('build')
  .description('Build for production')
  .addOption(
    new Option('-m, --mode <mode>', 'build mode')
      .choices(['development', 'production'])
      .default('production')
  )
  .option('--analyze', 'analyze bundle size', false)
  .option('--sourcemap', 'generate source maps', false)
  .action(async (options) => {
    const spinner = ora('Building for production...').start();

    try {
      await new Promise((resolve) => setTimeout(resolve, 2000));

      spinner.succeed(chalk.green('Build complete!'));

      console.log(chalk.blue('\nBuild info:'));
      console.log('Mode:', options.mode);
      console.log('Source maps:', options.sourcemap ? 'enabled' : 'disabled');

      if (options.analyze) {
        console.log(chalk.gray('\nBundle analysis:'));
        console.log('  main.js: 245 KB');
        console.log('  vendor.js: 892 KB');
      }
    } catch (error) {
      spinner.fail(chalk.red('Build failed'));
      throw error;
    }
  });

// Deploy command with nested subcommands
const deploy = program.command('deploy').description('Deployment operations');

deploy
  .command('start <environment>')
  .description('Deploy to specified environment')
  .argument('<environment>', 'target environment (dev, staging, prod)')
  .addOption(
    new Option('-s, --strategy <strategy>', 'deployment strategy')
      .choices(['rolling', 'blue-green', 'canary'])
      .default('rolling')
  )
  .option('-f, --force', 'force deployment', false)
  .option('--dry-run', 'simulate deployment', false)
  .action(async (environment, options) => {
    if (options.dryRun) {
      console.log(chalk.yellow('🔍 Dry run mode - no actual deployment'));
    }

    const spinner = ora(`Deploying to ${environment}...`).start();

    try {
      spinner.text = 'Running tests...';
      await new Promise((resolve) => setTimeout(resolve, 1000));

      spinner.text = 'Building application...';
      await new Promise((resolve) => setTimeout(resolve, 1500));

      spinner.text = `Deploying with ${options.strategy} strategy...`;
      await new Promise((resolve) => setTimeout(resolve, 2000));

      spinner.succeed(chalk.green(`Deployed to ${environment}!`));

      console.log(chalk.blue('\nDeployment details:'));
      console.log('Environment:', environment);
      console.log('Strategy:', options.strategy);
      console.log('URL:', `https://${environment}.example.com`);
    } catch (error) {
      spinner.fail(chalk.red('Deployment failed'));
      throw error;
    }
  });

deploy
  .command('rollback [version]')
  .description('Rollback to previous version')
  .argument('[version]', 'version to rollback to', 'previous')
  .option('-f, --force', 'skip confirmation', false)
  .action((version, options) => {
    if (!options.force) {
      console.log(chalk.yellow('⚠ This will rollback your deployment. Use --force to confirm.'));
      return;
    }

    console.log(chalk.blue(`Rolling back to ${version}...`));
    console.log(chalk.green('✓ Rollback complete'));
  });

deploy
  .command('status')
  .description('Check deployment status')
  .option('-e, --env <environment>', 'check specific environment')
  .action((options) => {
    console.log(chalk.blue('Deployment status:'));

    const envs = options.env ? [options.env] : ['dev', 'staging', 'prod'];

    envs.forEach((env) => {
      console.log(`\n${env}:`);
      console.log('  Status:', chalk.green('healthy'));
      console.log('  Version:', '1.2.3');
      console.log('  Uptime:', '5d 12h 34m');
    });
  });

// Config command group
const config = program.command('config').description('Configuration management');

config
  .command('get <key>')
  .description('Get configuration value')
  .action((key) => {
    console.log(`${key}: value`);
  });

config
  .command('set <key> <value>')
  .description('Set configuration value')
  .action((key, value) => {
    console.log(chalk.green(`✓ Set ${key} = ${value}`));
  });

config
  .command('list')
  .description('List all configuration')
  .option('-f, --format <format>', 'output format (json, yaml, table)', 'table')
  .action((options) => {
    console.log(`Configuration (format: ${options.format}):`);
    console.log('key1: value1');
    console.log('key2: value2');
  });

// Database command group
const db = program.command('db').description('Database operations');

db.command('migrate')
  .description('Run database migrations')
  .option('-d, --dry-run', 'show migrations without running')
  .action((options) => {
    if (options.dryRun) {
      console.log(chalk.blue('Migrations to run:'));
      console.log('  001_create_users.sql');
      console.log('  002_add_email_index.sql');
    } else {
      console.log(chalk.blue('Running migrations...'));
      console.log(chalk.green('✓ 2 migrations applied'));
    }
  });

db.command('seed')
  .description('Seed database with data')
  .option('-e, --env <env>', 'environment', 'dev')
  .action((options) => {
    console.log(chalk.blue(`Seeding ${options.env} database...`));
    console.log(chalk.green('✓ Database seeded'));
  });

// Test command
program
  .command('test [pattern]')
  .description('Run tests')
  .argument('[pattern]', 'test file pattern', '**/*.test.ts')
  .option('-w, --watch', 'watch mode', false)
  .option('-c, --coverage', 'collect coverage', false)
  .option('--verbose', 'verbose output', false)
  .action((pattern, options) => {
    console.log(chalk.blue('Running tests...'));
    console.log('Pattern:', pattern);

    if (options.watch) {
      console.log(chalk.gray('Watch mode enabled'));
    }

    if (options.coverage) {
      console.log(chalk.gray('\nCoverage:'));
      console.log('  Statements: 85%');
      console.log('  Branches: 78%');
      console.log('  Functions: 92%');
      console.log('  Lines: 87%');
    }

    console.log(chalk.green('\n✓ 42 tests passed'));
  });

// Global error handling
program.exitOverride();

try {
  program.parse();
} catch (error: any) {
  if (error.code === 'commander.help') {
    // Help was displayed, exit normally
    process.exit(0);
  } else if (error.code === 'commander.version') {
    // Version was displayed, exit normally
    process.exit(0);
  } else {
    console.error(chalk.red('Error:'), error.message);

    const globalOpts = program.opts();
    if (globalOpts.verbose) {
      console.error(chalk.gray('\nStack trace:'));
      console.error(chalk.gray(error.stack));
    }

    process.exit(1);
  }
}

// Handle no command
if (process.argv.length <= 2) {
  program.help();
}
