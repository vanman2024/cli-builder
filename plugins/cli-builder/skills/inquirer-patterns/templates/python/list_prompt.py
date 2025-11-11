"""
List Selection Prompt Template

Use for: Single choice from predefined options
Features: Arrow key navigation, search filtering
"""

import questionary
from questionary import Choice, Separator


def list_prompt_example():
    """Example list selection prompts"""

    print("\n📋 List Selection Example\n")

    # Simple list
    framework = questionary.select(
        "Choose your preferred framework:",
        choices=[
            'React',
            'Vue',
            'Angular',
            'Svelte',
            'Next.js',
            'Nuxt.js'
        ],
        default='React'
    ).ask()

    # List with values
    language = questionary.select(
        "Choose programming language:",
        choices=[
            Choice('JavaScript', value='js'),
            Choice('TypeScript', value='ts'),
            Choice('Python', value='py'),
            Choice('Ruby', value='rb'),
            Choice('Go', value='go')
        ],
        default='ts'
    ).ask()

    # List with descriptions
    package_manager = questionary.select(
        "Choose package manager:",
        choices=[
            Choice('npm - Node Package Manager', value='npm', shortcut_key='n'),
            Choice('yarn - Fast, reliable package manager', value='yarn', shortcut_key='y'),
            Choice('pnpm - Fast, disk space efficient', value='pnpm', shortcut_key='p'),
            Choice('bun - All-in-one toolkit', value='bun', shortcut_key='b')
        ]
    ).ask()

    # List with separators
    environment = questionary.select(
        "Select deployment environment:",
        choices=[
            Separator('--- Cloud Platforms ---'),
            'AWS',
            'Google Cloud',
            'Azure',
            Separator('--- Serverless ---'),
            'Vercel',
            'Netlify',
            'Cloudflare Workers',
            Separator('--- Self-hosted ---'),
            'Docker',
            'Kubernetes'
        ]
    ).ask()

    # List with emojis and styling
    database = questionary.select(
        "Choose database:",
        choices=[
            Choice('🐘 PostgreSQL (Relational)', value='postgresql'),
            Choice('🐬 MySQL (Relational)', value='mysql'),
            Choice('🍃 MongoDB (Document)', value='mongodb'),
            Choice('⚡ Redis (Key-Value)', value='redis'),
            Choice('📊 SQLite (Embedded)', value='sqlite'),
            Choice('🔥 Supabase (PostgreSQL + APIs)', value='supabase')
        ],
        use_shortcuts=True,
        use_arrow_keys=True
    ).ask()

    answers = {
        'framework': framework,
        'language': language,
        'packageManager': package_manager,
        'environment': environment,
        'database': database
    }

    print("\n✅ Selections:")
    import json
    print(json.dumps(answers, indent=2))

    return answers


def dynamic_list_example():
    """Example with dynamic choices based on context"""

    print("\n🔄 Dynamic List Example\n")

    # First selection
    project_type = questionary.select(
        "Project type:",
        choices=['Web Application', 'CLI Tool', 'API/Backend', 'Library']
    ).ask()

    # Dynamic framework choices based on project type
    framework_choices = {
        'Web Application': ['React', 'Vue', 'Angular', 'Svelte', 'Next.js'],
        'CLI Tool': ['Commander.js', 'Yargs', 'Click', 'Typer', 'Cobra'],
        'API/Backend': ['Express', 'Fastify', 'Flask', 'FastAPI', 'Gin'],
        'Library': ['TypeScript', 'JavaScript', 'Python', 'Go', 'Rust']
    }

    framework = questionary.select(
        f"Choose framework for {project_type}:",
        choices=framework_choices.get(project_type, ['None'])
    ).ask()

    print(f"\n✅ Selected: {project_type} with {framework}")

    return {'projectType': project_type, 'framework': framework}


def categorized_list_example():
    """Example with categorized options"""

    print("\n📂 Categorized List Example\n")

    cloud_service = questionary.select(
        "Choose cloud service:",
        choices=[
            Separator('=== Compute ==='),
            Choice('EC2 - Virtual Servers', value='ec2'),
            Choice('Lambda - Serverless Functions', value='lambda'),
            Choice('ECS - Container Service', value='ecs'),
            Choice('EKS - Kubernetes Service', value='eks'),
            Separator('=== Storage ==='),
            Choice('S3 - Object Storage', value='s3'),
            Choice('EBS - Block Storage', value='ebs'),
            Choice('EFS - File System', value='efs'),
            Separator('=== Database ==='),
            Choice('RDS - Relational Database', value='rds'),
            Choice('DynamoDB - NoSQL Database', value='dynamodb'),
            Choice('ElastiCache - In-Memory Cache', value='elasticache'),
            Separator('=== Other ==='),
            Choice('CloudFront - CDN', value='cloudfront'),
            Choice('Route53 - DNS', value='route53'),
            Choice('SQS - Message Queue', value='sqs')
        ],
        use_indicator=True
    ).ask()

    print(f"\n✅ Selected: {cloud_service}")

    return {'cloudService': cloud_service}


def numbered_list_example():
    """Example with numbered choices for easier selection"""

    print("\n🔢 Numbered List Example\n")

    languages = [
        'Python', 'JavaScript', 'TypeScript', 'Go', 'Rust',
        'Java', 'C++', 'Ruby', 'PHP', 'Swift'
    ]

    # Add numbers to choices for easier reference
    numbered_choices = [
        Choice(f"{i+1}. {lang}", value=lang)
        for i, lang in enumerate(languages)
    ]

    language = questionary.select(
        "Choose programming language:",
        choices=numbered_choices,
        use_shortcuts=False  # Disable letter shortcuts when using numbers
    ).ask()

    print(f"\n✅ Selected: {language}")

    return {'language': language}


def main():
    """Run list prompt examples"""
    try:
        print("=== List Selection Examples ===")

        # Example 1: Basic list selections
        list_prompt_example()

        # Example 2: Dynamic choices
        dynamic_list_example()

        # Example 3: Categorized options
        categorized_list_example()

        # Example 4: Numbered list
        numbered_list_example()

        print("\n✅ List selection examples complete!")

    except KeyboardInterrupt:
        print("\n\n❌ User interrupted prompt")
        exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
