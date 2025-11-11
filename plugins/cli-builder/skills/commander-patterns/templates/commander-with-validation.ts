import { Command, Option } from 'commander';
import chalk from 'chalk';
import { z } from 'zod';

const program = new Command();

program
  .name('mycli')
  .description('CLI with comprehensive input validation')
  .version('1.0.0');

// Zod schemas for validation
const EmailSchema = z.string().email();
const UrlSchema = z.string().url();
const PortSchema = z.number().int().min(1).max(65535);
const EnvironmentSchema = z.enum(['dev', 'staging', 'prod']);

// Validation helper
function validateOrThrow<T>(schema: z.ZodSchema<T>, value: unknown, fieldName: string): T {
  try {
    return schema.parse(value);
  } catch (error) {
    if (error instanceof z.ZodError) {
      throw new Error(`Invalid ${fieldName}: ${error.errors[0].message}`);
    }
    throw error;
  }
}

// Command with validated arguments
program
  .command('create-user <email> <username>')
  .description('Create user with validated inputs')
  .argument('<email>', 'user email', (value) => {
    return validateOrThrow(EmailSchema, value, 'email');
  })
  .argument('<username>', 'username', (value) => {
    const UsernameSchema = z
      .string()
      .min(3, 'Username must be at least 3 characters')
      .max(20, 'Username must be at most 20 characters')
      .regex(/^[a-z0-9_]+$/, 'Username must contain only lowercase letters, numbers, and underscores');

    return validateOrThrow(UsernameSchema, value, 'username');
  })
  .option('-a, --age <age>', 'user age', (value) => {
    const age = parseInt(value, 10);
    const AgeSchema = z.number().int().min(13).max(120);
    return validateOrThrow(AgeSchema, age, 'age');
  })
  .action((email, username, options) => {
    console.log(chalk.green('✓ User validation passed'));
    console.log('Email:', email);
    console.log('Username:', username);
    if (options.age) {
      console.log('Age:', options.age);
    }
  });

// Command with validated options
program
  .command('deploy')
  .description('Deploy with validated configuration')
  .addOption(
    new Option('-e, --env <environment>', 'deployment environment')
      .argParser((value) => {
        return validateOrThrow(EnvironmentSchema, value, 'environment');
      })
      .makeOptionMandatory()
  )
  .addOption(
    new Option('-u, --url <url>', 'deployment URL')
      .argParser((value) => {
        return validateOrThrow(UrlSchema, value, 'URL');
      })
      .makeOptionMandatory()
  )
  .addOption(
    new Option('-p, --port <port>', 'server port')
      .argParser((value) => {
        const port = parseInt(value, 10);
        return validateOrThrow(PortSchema, port, 'port');
      })
      .default(3000)
  )
  .addOption(
    new Option('-r, --replicas <count>', 'replica count')
      .argParser((value) => {
        const count = parseInt(value, 10);
        const ReplicaSchema = z.number().int().min(1).max(100);
        return validateOrThrow(ReplicaSchema, count, 'replicas');
      })
      .default(3)
  )
  .action((options) => {
    console.log(chalk.green('✓ Deployment configuration validated'));
    console.log('Environment:', options.env);
    console.log('URL:', options.url);
    console.log('Port:', options.port);
    console.log('Replicas:', options.replicas);
  });

// Command with complex object validation
program
  .command('configure')
  .description('Configure application with JSON validation')
  .option('-c, --config <json>', 'configuration as JSON string', (value) => {
    // Parse JSON
    let parsed;
    try {
      parsed = JSON.parse(value);
    } catch {
      throw new Error('Invalid JSON format');
    }

    // Validate with Zod schema
    const ConfigSchema = z.object({
      api: z.object({
        url: z.string().url(),
        timeout: z.number().int().positive(),
        retries: z.number().int().min(0).max(5),
      }),
      database: z.object({
        host: z.string(),
        port: z.number().int().min(1).max(65535),
        name: z.string(),
      }),
      features: z.object({
        enableCache: z.boolean(),
        enableMetrics: z.boolean(),
      }),
    });

    return validateOrThrow(ConfigSchema, parsed, 'configuration');
  })
  .action((options) => {
    if (options.config) {
      console.log(chalk.green('✓ Configuration validated'));
      console.log(JSON.stringify(options.config, null, 2));
    }
  });

// Command with file path validation
program
  .command('process <inputFile> <outputFile>')
  .description('Process file with path validation')
  .argument('<inputFile>', 'input file path', (value) => {
    const FilePathSchema = z.string().refine(
      (path) => {
        // Check file extension
        return path.endsWith('.json') || path.endsWith('.yaml') || path.endsWith('.yml');
      },
      { message: 'File must be .json, .yaml, or .yml' }
    );

    return validateOrThrow(FilePathSchema, value, 'input file');
  })
  .argument('<outputFile>', 'output file path', (value) => {
    const FilePathSchema = z.string().min(1);
    return validateOrThrow(FilePathSchema, value, 'output file');
  })
  .action((inputFile, outputFile) => {
    console.log(chalk.green('✓ File paths validated'));
    console.log('Input:', inputFile);
    console.log('Output:', outputFile);
  });

// Command with date/time validation
program
  .command('schedule <datetime>')
  .description('Schedule task with datetime validation')
  .argument('<datetime>', 'ISO 8601 datetime', (value) => {
    const date = new Date(value);

    if (isNaN(date.getTime())) {
      throw new Error('Invalid datetime format (use ISO 8601)');
    }

    if (date < new Date()) {
      throw new Error('Datetime must be in the future');
    }

    return date;
  })
  .option('-d, --duration <minutes>', 'duration in minutes', (value) => {
    const minutes = parseInt(value, 10);
    const DurationSchema = z.number().int().min(1).max(1440); // 1 min to 24 hours
    return validateOrThrow(DurationSchema, minutes, 'duration');
  })
  .action((datetime, options) => {
    console.log(chalk.green('✓ Schedule validated'));
    console.log('Start time:', datetime.toISOString());
    if (options.duration) {
      const endTime = new Date(datetime.getTime() + options.duration * 60000);
      console.log('End time:', endTime.toISOString());
    }
  });

// Command with array validation
program
  .command('tag <items...>')
  .description('Tag items with validation')
  .argument('<items...>', 'items to tag')
  .option('-t, --tags <tags...>', 'tags to apply', (values) => {
    const TagSchema = z.array(
      z
        .string()
        .min(2)
        .max(20)
        .regex(/^[a-z0-9-]+$/, 'Tags must contain only lowercase letters, numbers, and hyphens')
    );

    return validateOrThrow(TagSchema, values, 'tags');
  })
  .action((items, options) => {
    console.log(chalk.green('✓ Items and tags validated'));
    console.log('Items:', items);
    if (options.tags) {
      console.log('Tags:', options.tags);
    }
  });

// Command with custom validation logic
program
  .command('migrate')
  .description('Database migration with version validation')
  .option('-f, --from <version>', 'migrate from version', (value) => {
    const VersionSchema = z.string().regex(/^\d+\.\d+\.\d+$/, 'Version must be in format X.Y.Z');
    return validateOrThrow(VersionSchema, value, 'from version');
  })
  .option('-t, --to <version>', 'migrate to version', (value) => {
    const VersionSchema = z.string().regex(/^\d+\.\d+\.\d+$/, 'Version must be in format X.Y.Z');
    return validateOrThrow(VersionSchema, value, 'to version');
  })
  .action((options) => {
    // Additional cross-field validation
    if (options.from && options.to) {
      const fromParts = options.from.split('.').map(Number);
      const toParts = options.to.split('.').map(Number);

      const fromNum = fromParts[0] * 10000 + fromParts[1] * 100 + fromParts[2];
      const toNum = toParts[0] * 10000 + toParts[1] * 100 + toParts[2];

      if (fromNum >= toNum) {
        throw new Error('Target version must be higher than source version');
      }

      console.log(chalk.green('✓ Migration versions validated'));
      console.log(`Migrating from ${options.from} to ${options.to}`);
    }
  });

// Global error handling
program.exitOverride();

try {
  program.parse();
} catch (error: any) {
  if (error.code === 'commander.help' || error.code === 'commander.version') {
    process.exit(0);
  } else {
    console.error(chalk.red('Validation Error:'), error.message);
    console.error(chalk.gray('\nUse --help for usage information'));
    process.exit(1);
  }
}
