import { Command } from 'commander';
import chalk from 'chalk';

const program = new Command();

program
  .name('mycli')
  .description('CLI with various argument types')
  .version('1.0.0');

// Command with required argument
program
  .command('deploy <environment>')
  .description('Deploy to specified environment')
  .argument('<environment>', 'target environment (dev, staging, prod)')
  .action((environment) => {
    console.log(chalk.blue(`Deploying to ${environment}...`));
  });

// Command with required and optional arguments
program
  .command('create <name> [description]')
  .description('Create new item')
  .argument('<name>', 'item name')
  .argument('[description]', 'item description', 'No description provided')
  .action((name, description) => {
    console.log(`Creating: ${name}`);
    console.log(`Description: ${description}`);
  });

// Command with variadic arguments
program
  .command('add <items...>')
  .description('Add multiple items')
  .argument('<items...>', 'items to add')
  .action((items) => {
    console.log(chalk.blue('Adding items:'));
    items.forEach((item, index) => {
      console.log(`  ${index + 1}. ${item}`);
    });
    console.log(chalk.green(`✓ Added ${items.length} items`));
  });

// Command with custom argument parser
program
  .command('wait <seconds>')
  .description('Wait for specified time')
  .argument('<seconds>', 'seconds to wait', parseFloat)
  .action(async (seconds) => {
    console.log(chalk.blue(`Waiting ${seconds} seconds...`));
    await new Promise((resolve) => setTimeout(resolve, seconds * 1000));
    console.log(chalk.green('✓ Done'));
  });

// Command with arguments and options
program
  .command('copy <source> <destination>')
  .description('Copy file from source to destination')
  .argument('<source>', 'source file path')
  .argument('<destination>', 'destination file path')
  .option('-f, --force', 'overwrite if exists', false)
  .option('-r, --recursive', 'copy recursively', false)
  .action((source, destination, options) => {
    console.log(`Copying ${source} to ${destination}`);
    console.log('Options:', options);
    if (options.force) {
      console.log(chalk.yellow('⚠ Force mode: will overwrite existing files'));
    }
    if (options.recursive) {
      console.log(chalk.blue('Recursive copy enabled'));
    }
    console.log(chalk.green('✓ Copy complete'));
  });

// Command with argument validation
program
  .command('set-port <port>')
  .description('Set application port')
  .argument('<port>', 'port number', (value) => {
    const port = parseInt(value, 10);
    if (isNaN(port)) {
      throw new Error('Port must be a number');
    }
    if (port < 1 || port > 65535) {
      throw new Error('Port must be between 1 and 65535');
    }
    return port;
  })
  .action((port) => {
    console.log(chalk.green(`✓ Port set to ${port}`));
  });

program.parse();
