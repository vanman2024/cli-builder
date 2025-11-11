import { Command } from 'commander';

const program = new Command();

program
  .name('mycli')
  .description('A simple CLI tool')
  .version('1.0.0');

program
  .command('hello')
  .description('Say hello')
  .option('-n, --name <name>', 'name to greet', 'World')
  .action((options) => {
    console.log(`Hello, ${options.name}!`);
  });

program.parse();
