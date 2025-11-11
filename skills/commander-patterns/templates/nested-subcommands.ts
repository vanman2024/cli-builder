import { Command } from 'commander';
import chalk from 'chalk';

const program = new Command();

program
  .name('mycli')
  .description('CLI with nested subcommands')
  .version('1.0.0');

// Config command group
const config = program.command('config').description('Manage configuration');

config
  .command('get <key>')
  .description('Get configuration value')
  .action((key) => {
    const value = getConfig(key);
    if (value) {
      console.log(`${key} = ${value}`);
    } else {
      console.log(chalk.yellow(`Config key '${key}' not found`));
    }
  });

config
  .command('set <key> <value>')
  .description('Set configuration value')
  .action((key, value) => {
    setConfig(key, value);
    console.log(chalk.green(`✓ Set ${key} = ${value}`));
  });

config
  .command('list')
  .description('List all configuration')
  .option('-f, --format <format>', 'output format (json, table)', 'table')
  .action((options) => {
    const allConfig = getAllConfig();
    if (options.format === 'json') {
      console.log(JSON.stringify(allConfig, null, 2));
    } else {
      Object.entries(allConfig).forEach(([key, value]) => {
        console.log(`${key.padEnd(20)} ${value}`);
      });
    }
  });

config
  .command('delete <key>')
  .description('Delete configuration value')
  .option('-f, --force', 'skip confirmation', false)
  .action((key, options) => {
    if (!options.force) {
      console.log(chalk.yellow(`Are you sure? Use --force to confirm`));
      return;
    }
    deleteConfig(key);
    console.log(chalk.green(`✓ Deleted ${key}`));
  });

// Database command group
const db = program.command('db').description('Database operations');

db.command('migrate')
  .description('Run database migrations')
  .option('-d, --dry-run', 'show what would be migrated')
  .action((options) => {
    if (options.dryRun) {
      console.log(chalk.blue('Dry run: showing migrations...'));
    } else {
      console.log(chalk.blue('Running migrations...'));
    }
    console.log(chalk.green('✓ Migrations complete'));
  });

db.command('seed')
  .description('Seed database with data')
  .option('-e, --env <env>', 'environment', 'dev')
  .action((options) => {
    console.log(chalk.blue(`Seeding ${options.env} database...`));
    console.log(chalk.green('✓ Seeding complete'));
  });

db.command('reset')
  .description('Reset database')
  .option('-f, --force', 'skip confirmation')
  .action((options) => {
    if (!options.force) {
      console.log(chalk.red('⚠ This will delete all data! Use --force to confirm'));
      return;
    }
    console.log(chalk.yellow('Resetting database...'));
    console.log(chalk.green('✓ Database reset'));
  });

// User command group with nested subcommands
const user = program.command('user').description('User management');

const userList = user.command('list').description('List users');
userList
  .option('-p, --page <page>', 'page number', '1')
  .option('-l, --limit <limit>', 'items per page', '10')
  .action((options) => {
    console.log(`Listing users (page ${options.page}, limit ${options.limit})`);
  });

user
  .command('create <username> <email>')
  .description('Create new user')
  .option('-r, --role <role>', 'user role', 'user')
  .action((username, email, options) => {
    console.log(chalk.green(`✓ Created user ${username} (${email}) with role ${options.role}`));
  });

user
  .command('delete <userId>')
  .description('Delete user')
  .option('-f, --force', 'skip confirmation')
  .action((userId, options) => {
    if (!options.force) {
      console.log(chalk.red('Use --force to confirm deletion'));
      return;
    }
    console.log(chalk.green(`✓ Deleted user ${userId}`));
  });

// Helper functions (mock implementations)
const configStore: Record<string, string> = {
  apiUrl: 'https://api.example.com',
  timeout: '5000',
};

function getConfig(key: string): string | undefined {
  return configStore[key];
}

function setConfig(key: string, value: string): void {
  configStore[key] = value;
}

function getAllConfig(): Record<string, string> {
  return { ...configStore };
}

function deleteConfig(key: string): void {
  delete configStore[key];
}

program.parse();
