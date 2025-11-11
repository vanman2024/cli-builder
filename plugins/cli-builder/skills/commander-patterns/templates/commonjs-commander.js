#!/usr/bin/env node
const { Command } = require('commander');

const program = new Command();

program
  .name('mycli')
  .description('A simple CLI tool (CommonJS)')
  .version('1.0.0');

program
  .command('hello')
  .description('Say hello')
  .option('-n, --name <name>', 'name to greet', 'World')
  .action((options) => {
    console.log(`Hello, ${options.name}!`);
  });

program
  .command('deploy <environment>')
  .description('Deploy to environment')
  .option('-f, --force', 'force deployment', false)
  .action((environment, options) => {
    console.log(`Deploying to ${environment}...`);
    if (options.force) {
      console.log('Force mode enabled');
    }
  });

program.parse();
