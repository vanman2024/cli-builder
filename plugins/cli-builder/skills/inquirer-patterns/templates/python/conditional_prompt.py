"""
Conditional Prompt Template

Use for: Dynamic forms based on previous answers
Features: Skip logic, dependent questions, branching
"""

import questionary
from questionary import Choice, Separator


def conditional_prompt_example():
    """Example conditional prompts"""

    print("\n🔀 Conditional Prompt Example\n")

    # First question: Use database?
    use_database = questionary.confirm(
        "Do you want to use a database?",
        default=True
    ).ask()

    database_config = {}

    if use_database:
        # Database type
        database_type = questionary.select(
            "Select database type:",
            choices=['PostgreSQL', 'MySQL', 'MongoDB', 'SQLite', 'Redis']
        ).ask()

        database_config['databaseType'] = database_type

        # Host and port (not for SQLite)
        if database_type != 'SQLite':
            database_host = questionary.text(
                "Database host:",
                default="localhost"
            ).ask()

            # Default ports based on database type
            default_ports = {
                'PostgreSQL': '5432',
                'MySQL': '3306',
                'MongoDB': '27017',
                'Redis': '6379'
            }

            database_port = questionary.text(
                "Database port:",
                default=default_ports.get(database_type, '5432')
            ).ask()

            database_config['host'] = database_host
            database_config['port'] = database_port

        # Database name
        database_name = questionary.text(
            "Database name:",
            validate=lambda text: len(text) > 0 or "Database name required"
        ).ask()

        database_config['databaseName'] = database_name

        # Authentication
        use_authentication = questionary.confirm(
            "Do you want to use authentication?",
            default=True
        ).ask()

        if use_authentication:
            database_username = questionary.text(
                "Database username:",
                validate=lambda text: len(text) > 0 or "Username required"
            ).ask()

            database_password = questionary.password(
                "Database password:"
            ).ask()

            database_config['useAuthentication'] = True
            database_config['username'] = database_username
            # Don't store actual password in answers

        # SSL (only for remote hosts)
        if database_type != 'SQLite' and database_config.get('host') != 'localhost':
            use_ssl = questionary.confirm(
                "Use SSL connection?",
                default=False
            ).ask()

            if use_ssl:
                ssl_cert_path = questionary.text(
                    "Path to SSL certificate:",
                    validate=lambda text: len(text) > 0 or "SSL certificate path required"
                ).ask()

                database_config['useSSL'] = True
                database_config['sslCertPath'] = ssl_cert_path

    answers = {
        'useDatabase': use_database,
        'databaseConfig': database_config if use_database else None
    }

    print("\n✅ Configuration:")
    import json
    print(json.dumps(answers, indent=2))

    return answers


def deployment_wizard():
    """Example: Deployment configuration wizard"""

    print("\n🚀 Deployment Configuration Wizard\n")

    # Environment
    environment = questionary.select(
        "Select deployment environment:",
        choices=['Development', 'Staging', 'Production']
    ).ask()

    config = {'environment': environment}

    # Docker
    use_docker = questionary.confirm(
        "Deploy using Docker?",
        default=True
    ).ask()

    config['useDocker'] = use_docker

    if use_docker:
        docker_image = questionary.text(
            "Docker image name:",
            default="myapp:latest",
            validate=lambda text: len(text) > 0 or "Docker image name required"
        ).ask()

        config['dockerImage'] = docker_image

        registry = questionary.select(
            "Container registry:",
            choices=[
                'Docker Hub',
                'GitHub Container Registry',
                'AWS ECR',
                'Google Artifact Registry'
            ]
        ).ask()

        config['registry'] = registry

    # Platform
    platform = questionary.select(
        "Deployment platform:",
        choices=[
            'AWS', 'Google Cloud', 'Azure',
            'DigitalOcean', 'Vercel', 'Netlify', 'Self-hosted'
        ]
    ).ask()

    config['platform'] = platform

    # Platform-specific configuration
    if platform == 'AWS':
        aws_service = questionary.select(
            "AWS service:",
            choices=['ECS', 'EKS', 'Lambda', 'Elastic Beanstalk', 'EC2']
        ).ask()
        config['awsService'] = aws_service

        # Auto-scaling (only for certain services)
        if aws_service in ['ECS', 'EKS']:
            auto_scale = questionary.confirm(
                "Enable auto-scaling?",
                default=True
            ).ask()

            config['autoScale'] = auto_scale

            if auto_scale:
                min_instances = questionary.text(
                    "Minimum instances:",
                    default="1",
                    validate=lambda text: text.isdigit() and int(text) > 0 or "Must be at least 1"
                ).ask()

                max_instances = questionary.text(
                    "Maximum instances:",
                    default="10",
                    validate=lambda text: text.isdigit() and int(text) >= int(min_instances) or f"Must be at least {min_instances}"
                ).ask()

                config['minInstances'] = int(min_instances)
                config['maxInstances'] = int(max_instances)

    elif platform == 'Google Cloud':
        gcp_service = questionary.select(
            "Google Cloud service:",
            choices=['Cloud Run', 'GKE', 'App Engine', 'Compute Engine']
        ).ask()
        config['gcpService'] = gcp_service

    # CDN (only for production)
    if environment == 'Production':
        use_cdn = questionary.confirm(
            "Use CDN for static assets?",
            default=True
        ).ask()

        config['useCDN'] = use_cdn

        if use_cdn:
            cdn_provider = questionary.select(
                "CDN provider:",
                choices=['CloudFlare', 'AWS CloudFront', 'Google Cloud CDN', 'Azure CDN']
            ).ask()
            config['cdnProvider'] = cdn_provider

    # Monitoring
    setup_monitoring = questionary.confirm(
        "Setup monitoring?",
        default=True
    ).ask()

    if setup_monitoring:
        monitoring_tools = questionary.checkbox(
            "Select monitoring tools:",
            choices=['Prometheus', 'Grafana', 'Datadog', 'New Relic', 'Sentry'],
            validate=lambda choices: len(choices) > 0 or "Select at least one tool"
        ).ask()

        config['monitoringTools'] = monitoring_tools

    print("\n✅ Deployment configuration complete!")
    import json
    print(json.dumps(config, indent=2))

    return config


def feature_flag_wizard():
    """Example: Feature flag configuration"""

    print("\n🎛️  Feature Flag Configuration\n")

    # Feature name
    feature_name = questionary.text(
        "Feature name:",
        validate=lambda text: text and text.replace('-', '').replace('_', '').islower() or "Use lowercase, hyphens, underscores only"
    ).ask()

    # Enabled by default
    enabled_by_default = questionary.confirm(
        "Enabled by default?",
        default=False
    ).ask()

    config = {
        'featureName': feature_name,
        'enabledByDefault': enabled_by_default
    }

    # Rollout strategy
    rollout_strategy = questionary.select(
        "Rollout strategy:",
        choices=[
            'All users',
            'Percentage rollout',
            'User targeting',
            'Beta users only',
            'Manual control'
        ]
    ).ask()

    config['rolloutStrategy'] = rollout_strategy

    # Percentage rollout
    if rollout_strategy == 'Percentage rollout':
        rollout_percentage = questionary.text(
            "Rollout percentage (0-100):",
            default="10",
            validate=lambda text: text.isdigit() and 0 <= int(text) <= 100 or "Must be between 0 and 100"
        ).ask()

        config['rolloutPercentage'] = int(rollout_percentage)

    # User targeting
    if rollout_strategy == 'User targeting':
        target_user_groups = questionary.checkbox(
            "Target user groups:",
            choices=[
                'Beta testers',
                'Premium users',
                'Internal team',
                'Early adopters',
                'Specific regions'
            ],
            validate=lambda choices: len(choices) > 0 or "Select at least one group"
        ).ask()

        config['targetUserGroups'] = target_user_groups

        # Specific regions
        if 'Specific regions' in target_user_groups:
            target_regions = questionary.checkbox(
                "Target regions:",
                choices=[
                    'North America',
                    'Europe',
                    'Asia Pacific',
                    'South America',
                    'Africa'
                ]
            ).ask()

            config['targetRegions'] = target_regions

    # Metrics
    enable_metrics = questionary.confirm(
        "Track feature usage metrics?",
        default=True
    ).ask()

    if enable_metrics:
        metrics = questionary.checkbox(
            "Select metrics to track:",
            choices=[
                'Usage count',
                'User adoption rate',
                'Performance impact',
                'Error rate',
                'User feedback'
            ]
        ).ask()

        config['metrics'] = metrics

    # Expiration
    add_expiration_date = questionary.confirm(
        "Set feature flag expiration?",
        default=False
    ).ask()

    if add_expiration_date:
        expiration_date = questionary.text(
            "Expiration date (YYYY-MM-DD):",
            validate=lambda text: len(text) == 10 and text.count('-') == 2 or "Use format YYYY-MM-DD"
        ).ask()

        config['expirationDate'] = expiration_date

    print("\n✅ Feature flag configured!")
    import json
    print(json.dumps(config, indent=2))

    return config


def cicd_pipeline_wizard():
    """Example: CI/CD pipeline setup"""

    print("\n⚙️  CI/CD Pipeline Configuration\n")

    # Provider
    provider = questionary.select(
        "CI/CD provider:",
        choices=['GitHub Actions', 'GitLab CI', 'CircleCI', 'Jenkins', 'Travis CI']
    ).ask()

    config = {'provider': provider}

    # Triggers
    triggers = questionary.checkbox(
        "Pipeline triggers:",
        choices=[
            'Push to main/master',
            'Pull request',
            'Tag creation',
            'Manual trigger',
            'Scheduled (cron)'
        ],
        default=['Push to main/master', 'Pull request']
    ).ask()

    config['triggers'] = triggers

    # Cron schedule
    if 'Scheduled (cron)' in triggers:
        cron_schedule = questionary.text(
            "Cron schedule:",
            default="0 2 * * *",
            validate=lambda text: len(text.split()) == 5 or "Invalid cron format (5 parts required)"
        ).ask()

        config['cronSchedule'] = cron_schedule

    # Stages
    stages = questionary.checkbox(
        "Pipeline stages:",
        choices=['Build', 'Test', 'Lint', 'Security scan', 'Deploy'],
        default=['Build', 'Test', 'Deploy'],
        validate=lambda choices: len(choices) > 0 or "Select at least one stage"
    ).ask()

    config['stages'] = stages

    # Test types
    if 'Test' in stages:
        test_types = questionary.checkbox(
            "Test types to run:",
            choices=[
                'Unit tests',
                'Integration tests',
                'E2E tests',
                'Performance tests'
            ]
        ).ask()

        config['testTypes'] = test_types

    # Security tools
    if 'Security scan' in stages:
        security_tools = questionary.checkbox(
            "Security scanning tools:",
            choices=['Snyk', 'Dependabot', 'SonarQube', 'OWASP Dependency Check']
        ).ask()

        config['securityTools'] = security_tools

    # Deploy environments
    if 'Deploy' in stages:
        deploy_environments = questionary.checkbox(
            "Deployment environments:",
            choices=['Development', 'Staging', 'Production'],
            default=['Staging', 'Production']
        ).ask()

        config['deployEnvironments'] = deploy_environments

        # Approval for production
        if 'Production' in deploy_environments:
            require_approval = questionary.confirm(
                "Require manual approval for production?",
                default=True
            ).ask()

            config['requireApproval'] = require_approval

    # Notifications
    enable_notifications = questionary.confirm(
        "Enable build notifications?",
        default=True
    ).ask()

    if enable_notifications:
        notification_channels = questionary.checkbox(
            "Notification channels:",
            choices=['Email', 'Slack', 'Discord', 'Microsoft Teams']
        ).ask()

        config['notificationChannels'] = notification_channels

    print("\n✅ CI/CD pipeline configured!")
    import json
    print(json.dumps(config, indent=2))

    return config


def main():
    """Run conditional prompt examples"""
    try:
        print("=== Conditional Prompt Examples ===")

        # Example 1: Database configuration
        conditional_prompt_example()

        # Example 2: Deployment wizard
        deployment_wizard()

        # Example 3: Feature flag configuration
        feature_flag_wizard()

        # Example 4: CI/CD pipeline setup
        cicd_pipeline_wizard()

        print("\n✅ Conditional prompt examples complete!")

    except KeyboardInterrupt:
        print("\n\n❌ User interrupted prompt")
        exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
