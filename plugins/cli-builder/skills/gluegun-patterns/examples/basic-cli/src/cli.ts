import { build } from 'gluegun'

/**
 * Create the CLI and kick it off
 */
async function run(argv: string[] = process.argv) {
  // Create a CLI runtime
  const cli = build()
    .brand('mycli')
    .src(__dirname)
    .plugins('./node_modules', { matching: 'mycli-*', hidden: true })
    .help() // provides default --help command
    .version() // provides default --version command
    .create()

  // Enable the following method if you'd like to skip loading one of these core extensions
  // this can improve performance if they're not necessary for your project:
  // .exclude(['meta', 'strings', 'print', 'filesystem', 'semver', 'system', 'prompt', 'http', 'template', 'patching', 'package-manager'])

  // Run the CLI
  const toolbox = await cli.run(argv)

  // Send it back (for testing, mostly)
  return toolbox
}

module.exports = { run }
