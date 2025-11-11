/**
 * Conditional Prompt Template
 *
 * Use for: Dynamic forms based on previous answers
 * Features: Skip logic, dependent questions, branching
 */

import inquirer from 'inquirer';

async function conditionalPromptExample() {
  const answers = await inquirer.prompt([
    {
      type: 'confirm',
      name: 'useDatabase',
      message: 'Do you want to use a database?',
      default: true
    },
    {
      type: 'list',
      name: 'databaseType',
      message: 'Select database type:',
      choices: ['PostgreSQL', 'MySQL', 'MongoDB', 'SQLite', 'Redis'],
      when: (answers) => answers.useDatabase
    },
    {
      type: 'input',
      name: 'databaseHost',
      message: 'Database host:',
      default: 'localhost',
      when: (answers) => {
        return answers.useDatabase && answers.databaseType !== 'SQLite';
      }
    },
    {
      type: 'input',
      name: 'databasePort',
      message: 'Database port:',
      default: (answers) => {
        const ports = {
          'PostgreSQL': '5432',
          'MySQL': '3306',
          'MongoDB': '27017',
          'Redis': '6379'
        };
        return ports[answers.databaseType] || '5432';
      },
      when: (answers) => {
        return answers.useDatabase && answers.databaseType !== 'SQLite';
      }
    },
    {
      type: 'input',
      name: 'databaseName',
      message: 'Database name:',
      when: (answers) => answers.useDatabase,
      validate: (input) => input.length > 0 || 'Database name required'
    },
    {
      type: 'confirm',
      name: 'useAuthentication',
      message: 'Do you want to use authentication?',
      default: true,
      when: (answers) => answers.useDatabase
    },
    {
      type: 'input',
      name: 'databaseUsername',
      message: 'Database username:',
      when: (answers) => answers.useDatabase && answers.useAuthentication,
      validate: (input) => input.length > 0 || 'Username required'
    },
    {
      type: 'password',
      name: 'databasePassword',
      message: 'Database password:',
      mask: '*',
      when: (answers) => answers.useDatabase && answers.useAuthentication
    },
    {
      type: 'confirm',
      name: 'useSSL',
      message: 'Use SSL connection?',
      default: false,
      when: (answers) => {
        return answers.useDatabase &&
               answers.databaseType !== 'SQLite' &&
               answers.databaseHost !== 'localhost';
      }
    },
    {
      type: 'input',
      name: 'sslCertPath',
      message: 'Path to SSL certificate:',
      when: (answers) => answers.useSSL,
      validate: (input) => input.length > 0 || 'SSL certificate path required'
    }
  ]);

  console.log('\n✅ Configuration:');
  console.log(JSON.stringify(answers, null, 2));

  return answers;
}

// Example: Deployment configuration wizard
async function deploymentWizard() {
  console.log('\n🚀 Deployment Configuration Wizard\n');

  const config = await inquirer.prompt([
    {
      type: 'list',
      name: 'environment',
      message: 'Select deployment environment:',
      choices: ['Development', 'Staging', 'Production']
    },
    {
      type: 'confirm',
      name: 'useDocker',
      message: 'Deploy using Docker?',
      default: true
    },
    {
      type: 'input',
      name: 'dockerImage',
      message: 'Docker image name:',
      when: (answers) => answers.useDocker,
      default: 'myapp:latest',
      validate: (input) => /^[a-z0-9-_/:.]+$/.test(input) || 'Invalid Docker image name'
    },
    {
      type: 'list',
      name: 'registry',
      message: 'Container registry:',
      choices: ['Docker Hub', 'GitHub Container Registry', 'AWS ECR', 'Google Artifact Registry'],
      when: (answers) => answers.useDocker
    },
    {
      type: 'list',
      name: 'platform',
      message: 'Deployment platform:',
      choices: ['AWS', 'Google Cloud', 'Azure', 'DigitalOcean', 'Vercel', 'Netlify', 'Self-hosted']
    },
    {
      type: 'list',
      name: 'awsService',
      message: 'AWS service:',
      choices: ['ECS', 'EKS', 'Lambda', 'Elastic Beanstalk', 'EC2'],
      when: (answers) => answers.platform === 'AWS'
    },
    {
      type: 'list',
      name: 'gcpService',
      message: 'Google Cloud service:',
      choices: ['Cloud Run', 'GKE', 'App Engine', 'Compute Engine'],
      when: (answers) => answers.platform === 'Google Cloud'
    },
    {
      type: 'confirm',
      name: 'autoScale',
      message: 'Enable auto-scaling?',
      default: true,
      when: (answers) => {
        const scalableServices = ['ECS', 'EKS', 'Cloud Run', 'GKE'];
        return scalableServices.includes(answers.awsService) ||
               scalableServices.includes(answers.gcpService);
      }
    },
    {
      type: 'input',
      name: 'minInstances',
      message: 'Minimum instances:',
      default: '1',
      when: (answers) => answers.autoScale,
      validate: (input) => {
        const num = parseInt(input);
        return num > 0 || 'Must be at least 1';
      }
    },
    {
      type: 'input',
      name: 'maxInstances',
      message: 'Maximum instances:',
      default: '10',
      when: (answers) => answers.autoScale,
      validate: (input, answers) => {
        const num = parseInt(input);
        const min = parseInt(answers.minInstances);
        return num >= min || `Must be at least ${min}`;
      }
    },
    {
      type: 'confirm',
      name: 'useCDN',
      message: 'Use CDN for static assets?',
      default: true,
      when: (answers) => answers.environment === 'Production'
    },
    {
      type: 'list',
      name: 'cdnProvider',
      message: 'CDN provider:',
      choices: ['CloudFlare', 'AWS CloudFront', 'Google Cloud CDN', 'Azure CDN'],
      when: (answers) => answers.useCDN
    },
    {
      type: 'confirm',
      name: 'setupMonitoring',
      message: 'Setup monitoring?',
      default: true
    },
    {
      type: 'checkbox',
      name: 'monitoringTools',
      message: 'Select monitoring tools:',
      choices: ['Prometheus', 'Grafana', 'Datadog', 'New Relic', 'Sentry'],
      when: (answers) => answers.setupMonitoring,
      validate: (choices) => choices.length > 0 || 'Select at least one tool'
    }
  ]);

  console.log('\n✅ Deployment configuration complete!');
  console.log(JSON.stringify(config, null, 2));

  return config;
}

// Example: Feature flag configuration
async function featureFlagWizard() {
  console.log('\n🎛️  Feature Flag Configuration\n');

  const config = await inquirer.prompt([
    {
      type: 'input',
      name: 'featureName',
      message: 'Feature name:',
      validate: (input) => /^[a-z-_]+$/.test(input) || 'Use lowercase, hyphens, underscores only'
    },
    {
      type: 'confirm',
      name: 'enabledByDefault',
      message: 'Enabled by default?',
      default: false
    },
    {
      type: 'list',
      name: 'rolloutStrategy',
      message: 'Rollout strategy:',
      choices: [
        'All users',
        'Percentage rollout',
        'User targeting',
        'Beta users only',
        'Manual control'
      ]
    },
    {
      type: 'input',
      name: 'rolloutPercentage',
      message: 'Rollout percentage (0-100):',
      when: (answers) => answers.rolloutStrategy === 'Percentage rollout',
      default: '10',
      validate: (input) => {
        const num = parseInt(input);
        return (num >= 0 && num <= 100) || 'Must be between 0 and 100';
      }
    },
    {
      type: 'checkbox',
      name: 'targetUserGroups',
      message: 'Target user groups:',
      choices: ['Beta testers', 'Premium users', 'Internal team', 'Early adopters', 'Specific regions'],
      when: (answers) => answers.rolloutStrategy === 'User targeting',
      validate: (choices) => choices.length > 0 || 'Select at least one group'
    },
    {
      type: 'checkbox',
      name: 'targetRegions',
      message: 'Target regions:',
      choices: ['North America', 'Europe', 'Asia Pacific', 'South America', 'Africa'],
      when: (answers) => {
        return answers.rolloutStrategy === 'User targeting' &&
               answers.targetUserGroups.includes('Specific regions');
      }
    },
    {
      type: 'confirm',
      name: 'enableMetrics',
      message: 'Track feature usage metrics?',
      default: true
    },
    {
      type: 'checkbox',
      name: 'metrics',
      message: 'Select metrics to track:',
      choices: [
        'Usage count',
        'User adoption rate',
        'Performance impact',
        'Error rate',
        'User feedback'
      ],
      when: (answers) => answers.enableMetrics
    },
    {
      type: 'confirm',
      name: 'addExpirationDate',
      message: 'Set feature flag expiration?',
      default: false
    },
    {
      type: 'input',
      name: 'expirationDate',
      message: 'Expiration date (YYYY-MM-DD):',
      when: (answers) => answers.addExpirationDate,
      validate: (input) => {
        const date = new Date(input);
        if (isNaN(date.getTime())) return 'Invalid date format';
        if (date < new Date()) return 'Date must be in the future';
        return true;
      }
    }
  ]);

  console.log('\n✅ Feature flag configured!');
  console.log(JSON.stringify(config, null, 2));

  return config;
}

// Example: CI/CD pipeline setup
async function cicdPipelineWizard() {
  console.log('\n⚙️  CI/CD Pipeline Configuration\n');

  const config = await inquirer.prompt([
    {
      type: 'list',
      name: 'provider',
      message: 'CI/CD provider:',
      choices: ['GitHub Actions', 'GitLab CI', 'CircleCI', 'Jenkins', 'Travis CI']
    },
    {
      type: 'checkbox',
      name: 'triggers',
      message: 'Pipeline triggers:',
      choices: [
        'Push to main/master',
        'Pull request',
        'Tag creation',
        'Manual trigger',
        'Scheduled (cron)'
      ],
      default: ['Push to main/master', 'Pull request']
    },
    {
      type: 'input',
      name: 'cronSchedule',
      message: 'Cron schedule:',
      when: (answers) => answers.triggers.includes('Scheduled (cron)'),
      default: '0 2 * * *',
      validate: (input) => {
        // Basic cron validation
        const parts = input.split(' ');
        return parts.length === 5 || 'Invalid cron format (5 parts required)';
      }
    },
    {
      type: 'checkbox',
      name: 'stages',
      message: 'Pipeline stages:',
      choices: ['Build', 'Test', 'Lint', 'Security scan', 'Deploy'],
      default: ['Build', 'Test', 'Deploy'],
      validate: (choices) => choices.length > 0 || 'Select at least one stage'
    },
    {
      type: 'checkbox',
      name: 'testTypes',
      message: 'Test types to run:',
      choices: ['Unit tests', 'Integration tests', 'E2E tests', 'Performance tests'],
      when: (answers) => answers.stages.includes('Test')
    },
    {
      type: 'checkbox',
      name: 'securityTools',
      message: 'Security scanning tools:',
      choices: ['Snyk', 'Dependabot', 'SonarQube', 'OWASP Dependency Check'],
      when: (answers) => answers.stages.includes('Security scan')
    },
    {
      type: 'checkbox',
      name: 'deployEnvironments',
      message: 'Deployment environments:',
      choices: ['Development', 'Staging', 'Production'],
      when: (answers) => answers.stages.includes('Deploy'),
      default: ['Staging', 'Production']
    },
    {
      type: 'confirm',
      name: 'requireApproval',
      message: 'Require manual approval for production?',
      default: true,
      when: (answers) => {
        return answers.stages.includes('Deploy') &&
               answers.deployEnvironments?.includes('Production');
      }
    },
    {
      type: 'confirm',
      name: 'enableNotifications',
      message: 'Enable build notifications?',
      default: true
    },
    {
      type: 'checkbox',
      name: 'notificationChannels',
      message: 'Notification channels:',
      choices: ['Email', 'Slack', 'Discord', 'Microsoft Teams'],
      when: (answers) => answers.enableNotifications
    }
  ]);

  console.log('\n✅ CI/CD pipeline configured!');
  console.log(JSON.stringify(config, null, 2));

  return config;
}

// Run if executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  (async () => {
    console.log('=== Conditional Prompt Examples ===\n');

    console.log('1. Database Configuration');
    await conditionalPromptExample();

    console.log('\n2. Deployment Wizard');
    await deploymentWizard();

    console.log('\n3. Feature Flag Configuration');
    await featureFlagWizard();

    console.log('\n4. CI/CD Pipeline Setup');
    await cicdPipelineWizard();

    process.exit(0);
  })().catch((error) => {
    if (error.isTtyError) {
      console.error('❌ Prompt could not be rendered in this environment');
    } else {
      console.error('❌ User interrupted prompt');
    }
    process.exit(1);
  });
}

export {
  conditionalPromptExample,
  deploymentWizard,
  featureFlagWizard,
  cicdPipelineWizard
};
