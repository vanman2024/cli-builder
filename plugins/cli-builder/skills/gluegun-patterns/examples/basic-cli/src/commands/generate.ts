import { GluegunCommand } from 'gluegun'

/**
 * Generate Command
 * Demonstrates template generation and filesystem operations
 */
const command: GluegunCommand = {
  name: 'generate',
  alias: ['g', 'create'],
  description: 'Generate a new component from template',

  run: async (toolbox) => {
    const { template, print, parameters, filesystem, strings } = toolbox

    // Get component name
    const name = parameters.first

    if (!name) {
      print.error('Component name is required')
      print.info('Usage: mycli generate <ComponentName>')
      return
    }

    // Convert to different cases
    const pascalName = strings.pascalCase(name)
    const kebabName = strings.kebabCase(name)

    // Target directory
    const targetDir = 'src/components'
    const targetFile = `${targetDir}/${kebabName}.ts`

    // Ensure directory exists
    await filesystem.dir(targetDir)

    // Check if file already exists
    if (filesystem.exists(targetFile)) {
      const overwrite = await toolbox.prompt.confirm(
        `${targetFile} already exists. Overwrite?`
      )

      if (!overwrite) {
        print.warning('Generation cancelled')
        return
      }
    }

    // Show spinner while generating
    const spinner = print.spin(`Generating ${pascalName} component...`)

    try {
      // Generate from template
      await template.generate({
        template: 'component.ts.ejs',
        target: targetFile,
        props: {
          name: pascalName,
          kebabName,
          timestamp: new Date().toISOString()
        }
      })

      spinner.succeed(`Generated ${targetFile}`)

      // Add to index if it exists
      const indexPath = `${targetDir}/index.ts`
      if (filesystem.exists(indexPath)) {
        await filesystem.append(
          indexPath,
          `export { ${pascalName} } from './${kebabName}'\n`
        )
        print.info(`Added export to ${indexPath}`)
      }

      // Success message with details
      print.success('Component generated successfully!')
      print.info('')
      print.info('Next steps:')
      print.info(`  1. Edit ${targetFile}`)
      print.info(`  2. Import in your app: import { ${pascalName} } from './components/${kebabName}'`)

    } catch (error) {
      spinner.fail('Generation failed')
      print.error(error.message)
    }
  }
}

module.exports = command
