#!/usr/bin/env node
// TypeScript equivalent using commander.js (similar API to urfave/cli)

import { Command } from 'commander';

const program = new Command();

program
  .name('myapp')
  .description('A simple CLI application')
  .version('0.1.0');

program
  .option('-v, --verbose', 'Enable verbose output')
  .option('-c, --config <path>', 'Path to config file', process.env.CONFIG_PATH)
  .action((options) => {
    if (options.verbose) {
      console.log('Verbose mode enabled');
    }

    if (options.config) {
      console.log(`Using config: ${options.config}`);
    }

    console.log('Hello, World!');
  });

// Subcommands
program
  .command('start')
  .description('Start the service')
  .option('-p, --port <number>', 'Port to listen on', '8080')
  .action((options) => {
    console.log(`Starting service on port ${options.port}`);
  });

program
  .command('stop')
  .description('Stop the service')
  .action(() => {
    console.log('Stopping service...');
  });

program
  .command('status')
  .description('Check service status')
  .action(() => {
    console.log('Service is running');
  });

program.parse();
