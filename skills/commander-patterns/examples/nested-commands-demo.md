# Nested Commands Demo

Examples of building multi-level command hierarchies with Commander.js.

## Basic Nested Commands

```typescript
import { Command } from 'commander';

const program = new Command();

program.name('mycli').version('1.0.0');

// Create parent command
const config = program.command('config').description('Configuration management');

// Add subcommands
config
  .command('get <key>')
  .description('Get config value')
  .action((key) => {
    console.log(`Getting ${key}...`);
  });

config
  .command('set <key> <value>')
  .description('Set config value')
  .action((key, value) => {
    console.log(`Setting ${key} = ${value}`);
  });

config
  .command('list')
  .description('List all config')
  .action(() => {
    console.log('Listing config...');
  });

program.parse();
```

Usage:
```bash
mycli config get api-key
mycli config set api-key abc123
mycli config list
mycli config --help    # Shows subcommands
```

## Multiple Command Groups

```typescript
import { Command } from 'commander';
import chalk from 'chalk';

const program = new Command();
program.name('mycli').version('1.0.0');

// Database commands
const db = program.command('db').description('Database operations');

db.command('migrate')
  .description('Run migrations')
  .option('-d, --dry-run', 'show migrations')
  .action((options) => {
    console.log(chalk.blue('Running migrations...'));
  });

db.command('seed')
  .description('Seed database')
  .option('-e, --env <env>', 'environment', 'dev')
  .action((options) => {
    console.log(chalk.blue(`Seeding ${options.env} database...`));
  });

db.command('reset')
  .description('Reset database')
  .option('-f, --force', 'skip confirmation')
  .action((options) => {
    if (!options.force) {
      console.log(chalk.red('Use --force to confirm'));
      return;
    }
    console.log(chalk.yellow('Resetting database...'));
  });

// User commands
const user = program.command('user').description('User management');

user
  .command('list')
  .description('List users')
  .option('-p, --page <page>', 'page number', '1')
  .action((options) => {
    console.log(`Listing users (page ${options.page})`);
  });

user
  .command('create <username> <email>')
  .description('Create user')
  .action((username, email) => {
    console.log(chalk.green(`Created user: ${username} (${email})`));
  });

user
  .command('delete <userId>')
  .description('Delete user')
  .option('-f, --force', 'skip confirmation')
  .action((userId, options) => {
    console.log(chalk.red(`Deleted user: ${userId}`));
  });

// Cache commands
const cache = program.command('cache').description('Cache management');

cache
  .command('clear')
  .description('Clear cache')
  .option('-a, --all', 'clear all caches')
  .action((options) => {
    console.log('Clearing cache...');
  });

cache
  .command('stats')
  .description('Show cache statistics')
  .action(() => {
    console.log('Cache stats:');
    console.log('  Size: 1.2 GB');
    console.log('  Hits: 89%');
  });

program.parse();
```

Usage:
```bash
mycli db migrate --dry-run
mycli db seed --env prod
mycli db reset --force

mycli user list --page 2
mycli user create john john@example.com
mycli user delete 123 --force

mycli cache clear --all
mycli cache stats
```

## Three-Level Nesting

```typescript
import { Command } from 'commander';

const program = new Command();
program.name('mycli').version('1.0.0');

// Level 1: Cloud
const cloud = program.command('cloud').description('Cloud operations');

// Level 2: AWS
const aws = cloud.command('aws').description('AWS operations');

// Level 3: EC2
const ec2 = aws.command('ec2').description('EC2 operations');

ec2
  .command('list')
  .description('List EC2 instances')
  .action(() => {
    console.log('Listing EC2 instances...');
  });

ec2
  .command('start <instanceId>')
  .description('Start EC2 instance')
  .action((instanceId) => {
    console.log(`Starting instance ${instanceId}...`);
  });

ec2
  .command('stop <instanceId>')
  .description('Stop EC2 instance')
  .action((instanceId) => {
    console.log(`Stopping instance ${instanceId}...`);
  });

// Level 3: S3
const s3 = aws.command('s3').description('S3 operations');

s3.command('list')
  .description('List S3 buckets')
  .action(() => {
    console.log('Listing S3 buckets...');
  });

s3.command('upload <file> <bucket>')
  .description('Upload to S3')
  .action((file, bucket) => {
    console.log(`Uploading ${file} to ${bucket}...`);
  });

// Level 2: Azure
const azure = cloud.command('azure').description('Azure operations');

azure
  .command('vm-list')
  .description('List VMs')
  .action(() => {
    console.log('Listing Azure VMs...');
  });

program.parse();
```

Usage:
```bash
mycli cloud aws ec2 list
mycli cloud aws ec2 start i-123456
mycli cloud aws s3 list
mycli cloud aws s3 upload file.txt my-bucket
mycli cloud azure vm-list
```

## CRUD Pattern

```typescript
import { Command } from 'commander';
import chalk from 'chalk';

const program = new Command();
program.name('api-cli').version('1.0.0');

function createResourceCommands(name: string) {
  const resource = program.command(name).description(`${name} management`);

  resource
    .command('list')
    .description(`List all ${name}`)
    .option('-p, --page <page>', 'page number', '1')
    .option('-l, --limit <limit>', 'items per page', '10')
    .action((options) => {
      console.log(chalk.blue(`Listing ${name}...`));
      console.log(`Page ${options.page}, Limit ${options.limit}`);
    });

  resource
    .command('get <id>')
    .description(`Get ${name} by ID`)
    .action((id) => {
      console.log(chalk.blue(`Getting ${name} ${id}...`));
    });

  resource
    .command('create')
    .description(`Create new ${name}`)
    .option('-d, --data <json>', 'JSON data')
    .action((options) => {
      console.log(chalk.green(`Creating ${name}...`));
      console.log('Data:', options.data);
    });

  resource
    .command('update <id>')
    .description(`Update ${name}`)
    .option('-d, --data <json>', 'JSON data')
    .action((id, options) => {
      console.log(chalk.yellow(`Updating ${name} ${id}...`));
      console.log('Data:', options.data);
    });

  resource
    .command('delete <id>')
    .description(`Delete ${name}`)
    .option('-f, --force', 'skip confirmation')
    .action((id, options) => {
      if (!options.force) {
        console.log(chalk.red('Use --force to confirm deletion'));
        return;
      }
      console.log(chalk.red(`Deleted ${name} ${id}`));
    });

  return resource;
}

// Create CRUD commands for different resources
createResourceCommands('users');
createResourceCommands('posts');
createResourceCommands('comments');

program.parse();
```

Usage:
```bash
# Users
api-cli users list --page 2
api-cli users get 123
api-cli users create --data '{"name":"John"}'
api-cli users update 123 --data '{"email":"new@example.com"}'
api-cli users delete 123 --force

# Posts
api-cli posts list
api-cli posts get 456
api-cli posts create --data '{"title":"Hello"}'

# Comments
api-cli comments list
```

## Modular Command Structure

Split commands into separate files for better organization:

**src/commands/config.ts**
```typescript
import { Command } from 'commander';

export function createConfigCommand(): Command {
  const config = new Command('config').description('Configuration management');

  config
    .command('get <key>')
    .description('Get config value')
    .action((key) => {
      console.log(`Getting ${key}...`);
    });

  config
    .command('set <key> <value>')
    .description('Set config value')
    .action((key, value) => {
      console.log(`Setting ${key} = ${value}`);
    });

  return config;
}
```

**src/commands/user.ts**
```typescript
import { Command } from 'commander';

export function createUserCommand(): Command {
  const user = new Command('user').description('User management');

  user
    .command('list')
    .description('List users')
    .action(() => {
      console.log('Listing users...');
    });

  user
    .command('create <username>')
    .description('Create user')
    .action((username) => {
      console.log(`Creating user: ${username}`);
    });

  return user;
}
```

**src/index.ts**
```typescript
import { Command } from 'commander';
import { createConfigCommand } from './commands/config';
import { createUserCommand } from './commands/user';

const program = new Command();

program
  .name('mycli')
  .version('1.0.0')
  .description('My CLI tool');

// Add command groups
program.addCommand(createConfigCommand());
program.addCommand(createUserCommand());

program.parse();
```

## Nested Commands with Shared Options

```typescript
import { Command } from 'commander';

const program = new Command();
program.name('deploy-cli').version('1.0.0');

// Parent deploy command with shared options
const deploy = program
  .command('deploy')
  .description('Deployment operations')
  .option('-e, --env <environment>', 'environment', 'dev')
  .option('-v, --verbose', 'verbose output');

// Subcommands inherit parent context
deploy
  .command('start')
  .description('Start deployment')
  .option('-f, --force', 'force deployment')
  .action((options, command) => {
    const parentOpts = command.parent?.opts();
    console.log('Environment:', parentOpts?.env);
    console.log('Verbose:', parentOpts?.verbose);
    console.log('Force:', options.force);
  });

deploy
  .command('status')
  .description('Check deployment status')
  .action((options, command) => {
    const parentOpts = command.parent?.opts();
    console.log(`Checking ${parentOpts?.env} status...`);
  });

deploy
  .command('rollback [version]')
  .description('Rollback deployment')
  .action((version, options, command) => {
    const parentOpts = command.parent?.opts();
    console.log(`Rolling back ${parentOpts?.env}...`);
  });

program.parse();
```

Usage:
```bash
deploy-cli deploy --env prod start --force
deploy-cli deploy --env staging status
deploy-cli deploy --verbose rollback v1.0.0
```

## Command Aliases

```typescript
import { Command } from 'commander';

const program = new Command();
program.name('mycli').version('1.0.0');

const db = program.command('database').alias('db').description('Database ops');

db.command('migrate')
  .alias('m')
  .description('Run migrations')
  .action(() => {
    console.log('Running migrations...');
  });

db.command('seed')
  .alias('s')
  .description('Seed database')
  .action(() => {
    console.log('Seeding...');
  });

program.parse();
```

Usage (all equivalent):
```bash
mycli database migrate
mycli db migrate
mycli db m

mycli database seed
mycli db seed
mycli db s
```

## Complete CLI Example

```typescript
#!/usr/bin/env node
import { Command } from 'commander';
import chalk from 'chalk';

const program = new Command();

program
  .name('project-cli')
  .version('1.0.0')
  .description('Project management CLI');

// Project commands
const project = program.command('project').alias('p').description('Project operations');

project
  .command('init <name>')
  .description('Initialize new project')
  .option('-t, --template <type>', 'template', 'basic')
  .action((name, options) => {
    console.log(chalk.green(`✓ Initialized ${name} with ${options.template} template`));
  });

project
  .command('build')
  .description('Build project')
  .action(() => {
    console.log(chalk.blue('Building...'));
  });

// Environment commands
const env = program.command('env').alias('e').description('Environment management');

env
  .command('list')
  .alias('ls')
  .description('List environments')
  .action(() => {
    console.log('dev, staging, prod');
  });

env
  .command('create <name>')
  .description('Create environment')
  .action((name) => {
    console.log(chalk.green(`✓ Created environment: ${name}`));
  });

// Deploy commands
const deploy = program.command('deploy').alias('d').description('Deployment operations');

deploy
  .command('start <env>')
  .description('Start deployment')
  .action((env) => {
    console.log(chalk.blue(`Deploying to ${env}...`));
  });

deploy
  .command('status [env]')
  .description('Check status')
  .action((env) => {
    console.log(`Status of ${env || 'all'}:`);
  });

program.parse();
```

Usage:
```bash
project-cli project init my-app --template advanced
project-cli p build

project-cli env list
project-cli e create staging

project-cli deploy start prod
project-cli d status
```
