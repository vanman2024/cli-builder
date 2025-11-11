#!/usr/bin/env node
const yargs = require('yargs/yargs');
const { hideBin } = require('yargs/helpers');

yargs(hideBin(process.argv))
  .command('greet <name>', 'greet someone', (yargs) => {
    yargs.positional('name', {
      describe: 'Name to greet',
      type: 'string'
    });
  }, (argv) => {
    console.log(`Hello, ${argv.name}!`);
  })
  .command('goodbye <name>', 'say goodbye', (yargs) => {
    yargs.positional('name', {
      describe: 'Name to say goodbye to',
      type: 'string'
    });
  }, (argv) => {
    console.log(`Goodbye, ${argv.name}!`);
  })
  .demandCommand(1, 'You need at least one command')
  .strict()
  .help()
  .alias('help', 'h')
  .version()
  .alias('version', 'V')
  .parse();
