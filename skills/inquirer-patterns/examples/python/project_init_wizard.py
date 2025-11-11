"""
Example: Complete Project Initialization Wizard

Demonstrates combining multiple prompt types to create
a comprehensive CLI tool for project setup
"""

import questionary
from questionary import Choice
import json


def project_init_wizard():
    """Complete project initialization wizard"""

    print('\n╔════════════════════════════════════════╗')
    print('║  🚀 Project Initialization Wizard 🚀  ║')
    print('╚════════════════════════════════════════╝\n')

    # Project basics
    name = questionary.text(
        "Project name:",
        validate=lambda text: (
            text and text.replace('-', '').isalnum()
            or "Use lowercase letters, numbers, and hyphens only"
        )
    ).ask()

    description = questionary.text(
        "Description:",
        validate=lambda text: len(text) > 0 or "Description required"
    ).ask()

    # Language selection
    language = questionary.select(
        "Programming language:",
        choices=['TypeScript', 'JavaScript', 'Python', 'Go', 'Rust']
    ).ask()

    # Framework selection (based on language)
    frameworks = {
        'TypeScript': ['Next.js', 'Nest.js', 'Express', 'Fastify'],
        'JavaScript': ['React', 'Vue', 'Express', 'Koa'],
        'Python': ['FastAPI', 'Django', 'Flask'],
        'Go': ['Gin', 'Echo', 'Fiber'],
        'Rust': ['Actix', 'Rocket', 'Axum']
    }

    framework = questionary.select(
        "Framework:",
        choices=frameworks.get(language, ['None'])
    ).ask()

    # Feature selection
    features = questionary.checkbox(
        "Select features:",
        choices=[
            Choice('Database', value='database', checked=True),
            Choice('Authentication', value='auth'),
            Choice('API Documentation', value='docs'),
            Choice('Testing', value='testing', checked=True),
            Choice('Logging', value='logging', checked=True)
        ]
    ).ask()

    # Docker
    use_docker = questionary.confirm(
        "Use Docker?",
        default=True
    ).ask()

    # CI/CD
    setup_ci = questionary.confirm(
        "Setup CI/CD?",
        default=True
    ).ask()

    # Build configuration object
    config = {
        'name': name,
        'description': description,
        'language': language,
        'framework': framework,
        'features': features,
        'useDocker': use_docker,
        'setupCI': setup_ci
    }

    print('\n✅ Configuration complete!\n')
    print(json.dumps(config, indent=2))

    return config


if __name__ == "__main__":
    try:
        project_init_wizard()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
        exit(1)
