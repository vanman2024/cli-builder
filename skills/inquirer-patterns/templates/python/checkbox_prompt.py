"""
Checkbox Prompt Template

Use for: Multiple selections from options
Features: Space to toggle, Enter to confirm
"""

import questionary
from questionary import Choice, Separator, ValidationError, Validator


class MinimumChoicesValidator(Validator):
    """Validator to ensure minimum number of choices selected"""

    def __init__(self, minimum=1, message=None):
        self.minimum = minimum
        self.message = message or f"You must select at least {minimum} option(s)"

    def validate(self, document):
        # document.text contains selected choices as list
        if len(document.text) < self.minimum:
            raise ValidationError(
                message=self.message,
                cursor_position=0
            )


class MaximumChoicesValidator(Validator):
    """Validator to ensure maximum number of choices selected"""

    def __init__(self, maximum=10, message=None):
        self.maximum = maximum
        self.message = message or f"Please select no more than {maximum} options"

    def validate(self, document):
        if len(document.text) > self.maximum:
            raise ValidationError(
                message=self.message,
                cursor_position=0
            )


def checkbox_prompt_example():
    """Example checkbox prompts"""

    print("\n☑️  Checkbox Selection Example\n")

    # Simple checkbox
    features = questionary.checkbox(
        "Select features to include:",
        choices=[
            'Authentication',
            'Authorization',
            'Database Integration',
            'API Documentation',
            'Testing Suite',
            'CI/CD Pipeline',
            'Monitoring',
            'Logging'
        ],
        validate=lambda choices: len(choices) > 0 or "You must select at least one feature"
    ).ask()

    # Checkbox with default selections
    dev_tools = questionary.checkbox(
        "Select development tools:",
        choices=[
            Choice('ESLint (Linting)', value='eslint', checked=True),
            Choice('Prettier (Formatting)', value='prettier', checked=True),
            Choice('Jest (Testing)', value='jest'),
            Choice('Husky (Git Hooks)', value='husky'),
            Choice('TypeDoc (Documentation)', value='typedoc'),
            Choice('Webpack (Bundling)', value='webpack')
        ]
    ).ask()

    # Checkbox with separators and checked defaults
    plugins = questionary.checkbox(
        "Select plugins to install:",
        choices=[
            Separator('=== Essential ==='),
            Choice('dotenv - Environment variables', value='dotenv', checked=True),
            Choice('axios - HTTP client', value='axios', checked=True),
            Separator('=== Utilities ==='),
            Choice('lodash - Utility functions', value='lodash'),
            Choice('dayjs - Date manipulation', value='dayjs'),
            Choice('uuid - Unique IDs', value='uuid'),
            Separator('=== Validation ==='),
            Choice('joi - Schema validation', value='joi'),
            Choice('zod - TypeScript-first validation', value='zod'),
            Separator('=== Advanced ==='),
            Choice('bull - Job queues', value='bull'),
            Choice('socket.io - WebSockets', value='socket.io')
        ],
        validate=MaximumChoicesValidator(maximum=10)
    ).ask()

    # Checkbox with emojis
    permissions = questionary.checkbox(
        "Grant the following permissions:",
        choices=[
            Choice('📁 Read files', value='read', checked=True),
            Choice('✏️  Write files', value='write'),
            Choice('🗑️  Delete files', value='delete'),
            Choice('🌐 Network access', value='network', checked=True),
            Choice('🖥️  System commands', value='system'),
            Choice('🔒 Keychain access', value='keychain')
        ]
    ).ask()

    # Validate permissions logic
    if 'delete' in permissions and 'write' not in permissions:
        print("\n⚠️  Warning: Delete permission requires write permission")
        permissions.append('write')

    # Checkbox with validation
    environments = questionary.checkbox(
        "Select deployment environments:",
        choices=[
            Choice('Development', value='dev', checked=True),
            Choice('Staging', value='staging'),
            Choice('Production', value='prod'),
            Choice('Testing', value='test', checked=True)
        ],
        validate=lambda choices: (
            'dev' in choices or "Development environment is required"
        )
    ).ask()

    # Additional validation
    if 'prod' in environments and 'staging' not in environments:
        print("\n⚠️  Warning: Staging environment is recommended before production")

    answers = {
        'features': features,
        'devTools': dev_tools,
        'plugins': plugins,
        'permissions': permissions,
        'environments': environments
    }

    print("\n✅ Selected options:")
    import json
    print(json.dumps(answers, indent=2))

    # Example: Process selections
    print("\n📦 Installing selected features...")
    for feature in features:
        print(f"  - {feature}")

    return answers


def grouped_checkbox_example():
    """Example with logically grouped checkboxes"""

    print("\n📂 Grouped Checkbox Example\n")

    security_features = questionary.checkbox(
        "Select security features:",
        choices=[
            Separator('=== Authentication ==='),
            Choice('JWT Tokens', value='jwt', checked=True),
            Choice('OAuth 2.0', value='oauth'),
            Choice('Session Management', value='session'),
            Choice('Two-Factor Auth', value='2fa'),
            Separator('=== Authorization ==='),
            Choice('Role-Based Access Control', value='rbac', checked=True),
            Choice('Permission System', value='permissions', checked=True),
            Choice('API Key Management', value='api-keys'),
            Separator('=== Security ==='),
            Choice('Rate Limiting', value='rate-limit', checked=True),
            Choice('CORS Configuration', value='cors', checked=True),
            Choice('Input Sanitization', value='sanitization', checked=True),
            Choice('SQL Injection Prevention', value='sql-prevent', checked=True),
            Choice('XSS Protection', value='xss-protect', checked=True),
            Separator('=== Encryption ==='),
            Choice('Data Encryption at Rest', value='encrypt-rest'),
            Choice('SSL/TLS', value='ssl', checked=True),
            Choice('Password Hashing', value='hash', checked=True)
        ],
        validate=MinimumChoicesValidator(minimum=3, message="Select at least 3 security features")
    ).ask()

    print(f"\n✅ Selected {len(security_features)} security features")
    return {'securityFeatures': security_features}


def dependent_checkbox_example():
    """Example with checkboxes that depend on previous selections"""

    print("\n🔗 Dependent Checkbox Example\n")

    # First checkbox: Select cloud providers
    cloud_providers = questionary.checkbox(
        "Select cloud providers:",
        choices=[
            Choice('☁️  AWS', value='aws'),
            Choice('☁️  Google Cloud', value='gcp'),
            Choice('☁️  Azure', value='azure'),
            Choice('☁️  DigitalOcean', value='do')
        ],
        validate=lambda c: len(c) > 0 or "Select at least one cloud provider"
    ).ask()

    # Second checkbox: AWS services (only if AWS selected)
    aws_services = []
    if 'aws' in cloud_providers:
        aws_services = questionary.checkbox(
            "Select AWS services:",
            choices=[
                Choice('EC2 - Virtual Servers', value='ec2'),
                Choice('Lambda - Serverless', value='lambda'),
                Choice('S3 - Object Storage', value='s3', checked=True),
                Choice('RDS - Databases', value='rds'),
                Choice('CloudFront - CDN', value='cloudfront')
            ]
        ).ask()

    # Third checkbox: GCP services (only if GCP selected)
    gcp_services = []
    if 'gcp' in cloud_providers:
        gcp_services = questionary.checkbox(
            "Select GCP services:",
            choices=[
                Choice('Compute Engine', value='compute'),
                Choice('Cloud Functions', value='functions'),
                Choice('Cloud Storage', value='storage', checked=True),
                Choice('Cloud SQL', value='sql'),
                Choice('Cloud CDN', value='cdn')
            ]
        ).ask()

    result = {
        'cloudProviders': cloud_providers,
        'awsServices': aws_services,
        'gcpServices': gcp_services
    }

    print("\n✅ Configuration complete:")
    import json
    print(json.dumps(result, indent=2))

    return result


def conditional_validation_example():
    """Example with conditional validation logic"""

    print("\n🔍 Conditional Validation Example\n")

    database_features = questionary.checkbox(
        "Select database features:",
        choices=[
            Choice('Connection Pooling', value='pool', checked=True),
            Choice('Migrations', value='migrations', checked=True),
            Choice('Transactions', value='transactions'),
            Choice('Replication', value='replication'),
            Choice('Sharding', value='sharding'),
            Choice('Caching', value='caching')
        ]
    ).ask()

    # Conditional logic: Sharding requires replication
    if 'sharding' in database_features and 'replication' not in database_features:
        print("\n⚠️  Sharding requires replication. Adding replication...")
        database_features.append('replication')

    # Conditional logic: Caching works best with pooling
    if 'caching' in database_features and 'pool' not in database_features:
        add_pooling = questionary.confirm(
            "Caching works best with connection pooling. Add it?",
            default=True
        ).ask()
        if add_pooling:
            database_features.append('pool')

    print(f"\n✅ Selected {len(database_features)} database features")
    return {'databaseFeatures': database_features}


def main():
    """Run checkbox prompt examples"""
    try:
        print("=== Checkbox Prompt Examples ===")

        # Example 1: Basic checkbox selections
        checkbox_prompt_example()

        # Example 2: Grouped checkboxes
        grouped_checkbox_example()

        # Example 3: Dependent checkboxes
        dependent_checkbox_example()

        # Example 4: Conditional validation
        conditional_validation_example()

        print("\n✅ Checkbox examples complete!")

    except KeyboardInterrupt:
        print("\n\n❌ User interrupted prompt")
        exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
