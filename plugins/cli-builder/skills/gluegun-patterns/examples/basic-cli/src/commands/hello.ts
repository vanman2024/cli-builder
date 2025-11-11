import { GluegunCommand } from 'gluegun'

/**
 * Hello Command
 * Demonstrates basic parameter handling and print utilities
 */
const command: GluegunCommand = {
  name: 'hello',
  alias: ['hi', 'greet'],
  description: 'Say hello to someone',

  run: async (toolbox) => {
    const { print, parameters } = toolbox

    // Get name from first parameter
    const name = parameters.first || 'World'

    // Get options
    const options = parameters.options
    const loud = options.loud || options.l

    // Format message
    let message = `Hello, ${name}!`

    if (loud) {
      message = message.toUpperCase()
    }

    // Display with appropriate style
    print.success(message)

    // Show some additional info if verbose
    if (options.verbose || options.v) {
      print.info('Command executed successfully')
      print.info(`Parameters: ${JSON.stringify(parameters.array)}`)
      print.info(`Options: ${JSON.stringify(options)}`)
    }
  }
}

module.exports = command
