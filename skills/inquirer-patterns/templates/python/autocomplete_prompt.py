"""
Autocomplete Prompt Template

Use for: Large option lists with search
Features: Type-ahead, fuzzy matching, suggestions
"""

import questionary
from questionary import Choice


# Example: Countries list for autocomplete
COUNTRIES = [
    'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola',
    'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan',
    'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus',
    'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia',
    'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi',
    'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Chad',
    'Chile', 'China', 'Colombia', 'Comoros', 'Congo',
    'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic',
    'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic',
    'Ecuador', 'Egypt', 'El Salvador', 'Estonia', 'Ethiopia',
    'Fiji', 'Finland', 'France', 'Gabon', 'Gambia',
    'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada',
    'Guatemala', 'Guinea', 'Guyana', 'Haiti', 'Honduras',
    'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran',
    'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica',
    'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kuwait',
    'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia',
    'Libya', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malawi',
    'Malaysia', 'Maldives', 'Mali', 'Malta', 'Mexico',
    'Moldova', 'Monaco', 'Mongolia', 'Morocco', 'Mozambique',
    'Myanmar', 'Namibia', 'Nepal', 'Netherlands', 'New Zealand',
    'Nicaragua', 'Niger', 'Nigeria', 'Norway', 'Oman',
    'Pakistan', 'Panama', 'Paraguay', 'Peru', 'Philippines',
    'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia',
    'Rwanda', 'Saudi Arabia', 'Senegal', 'Serbia', 'Singapore',
    'Slovakia', 'Slovenia', 'Somalia', 'South Africa', 'South Korea',
    'Spain', 'Sri Lanka', 'Sudan', 'Sweden', 'Switzerland',
    'Syria', 'Taiwan', 'Tanzania', 'Thailand', 'Togo',
    'Tunisia', 'Turkey', 'Uganda', 'Ukraine', 'United Arab Emirates',
    'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan',
    'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe'
]

# Example: Popular packages
POPULAR_PACKAGES = [
    'express', 'react', 'vue', 'angular', 'next', 'nuxt',
    'axios', 'lodash', 'moment', 'dayjs', 'uuid', 'dotenv',
    'typescript', 'eslint', 'prettier', 'jest', 'mocha', 'chai',
    'webpack', 'vite', 'rollup', 'babel', 'esbuild',
    'socket.io', 'redis', 'mongodb', 'mongoose', 'sequelize',
    'prisma', 'typeorm', 'knex', 'pg', 'mysql2',
    'bcrypt', 'jsonwebtoken', 'passport', 'helmet', 'cors',
    'multer', 'sharp', 'puppeteer', 'playwright', 'cheerio'
]


def autocomplete_prompt_example():
    """Example autocomplete prompts"""

    print("\n🔍 Autocomplete Example\n")

    # Country selection with autocomplete
    country = questionary.autocomplete(
        "Select your country:",
        choices=COUNTRIES,
        validate=lambda text: len(text) > 0 or "Please select a country"
    ).ask()

    # Package selection
    package = questionary.autocomplete(
        "Search for an npm package:",
        choices=POPULAR_PACKAGES
    ).ask()

    # Cities based on country (conditional)
    city = None
    cities_by_country = {
        'United States': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
        'United Kingdom': ['London', 'Manchester', 'Birmingham', 'Glasgow', 'Liverpool'],
        'Canada': ['Toronto', 'Vancouver', 'Montreal', 'Calgary', 'Ottawa'],
        'Australia': ['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide'],
        'Germany': ['Berlin', 'Munich', 'Hamburg', 'Frankfurt', 'Cologne']
    }

    if country in cities_by_country:
        city = questionary.autocomplete(
            "Select city:",
            choices=cities_by_country[country]
        ).ask()

    answers = {
        'country': country,
        'package': package,
        'city': city
    }

    print("\n✅ Selections:")
    import json
    print(json.dumps(answers, indent=2))

    return answers


def framework_search_example():
    """Example: Framework/library search with descriptions"""

    print("\n🔎 Framework Search Example\n")

    frameworks = [
        'React - UI library by Facebook',
        'Vue.js - Progressive JavaScript framework',
        'Angular - Platform for building web apps',
        'Svelte - Cybernetically enhanced web apps',
        'Next.js - React framework with SSR',
        'Nuxt.js - Vue.js framework with SSR',
        'Remix - Full stack web framework',
        'SvelteKit - Svelte framework',
        'Express - Fast Node.js web framework',
        'Fastify - Fast and low overhead web framework',
        'NestJS - Progressive Node.js framework',
        'Koa - Expressive middleware for Node.js'
    ]

    framework = questionary.autocomplete(
        "Search for a framework:",
        choices=frameworks
    ).ask()

    # Extract value (remove description)
    framework_name = framework.split(' - ')[0] if ' - ' in framework else framework

    print(f"\n✅ Selected: {framework_name}")

    return {'framework': framework_name}


def command_search_example():
    """Example: Command search with emojis and categories"""

    print("\n⌨️  Command Search Example\n")

    commands = [
        '📦 install - Install dependencies',
        '🚀 start - Start development server',
        '🏗️  build - Build for production',
        '🧪 test - Run tests',
        '🔍 lint - Check code quality',
        '✨ format - Format code',
        '📝 generate - Generate files',
        '🔄 update - Update dependencies',
        '🧹 clean - Clean build artifacts',
        '🚢 deploy - Deploy application',
        '📊 analyze - Analyze bundle size',
        '🐛 debug - Start debugger'
    ]

    command = questionary.autocomplete(
        "Search for a command:",
        choices=commands
    ).ask()

    # Extract command name
    command_name = command.split(' - ')[0].split(' ', 1)[1] if ' - ' in command else command

    print(f"\n✅ Running: {command_name}")

    return {'command': command_name}


def api_endpoint_search():
    """Example: API endpoint search"""

    print("\n🔍 API Endpoint Search\n")

    endpoints = [
        'GET /users - List all users',
        'GET /users/:id - Get user by ID',
        'POST /users - Create new user',
        'PUT /users/:id - Update user',
        'DELETE /users/:id - Delete user',
        'GET /posts - List all posts',
        'GET /posts/:id - Get post by ID',
        'POST /posts - Create new post',
        'GET /comments - List comments',
        'POST /auth/login - User login',
        'POST /auth/register - User registration',
        'POST /auth/logout - User logout'
    ]

    endpoint = questionary.autocomplete(
        "Search API endpoints:",
        choices=endpoints
    ).ask()

    # Extract endpoint path
    endpoint_path = endpoint.split(' - ')[0] if ' - ' in endpoint else endpoint

    print(f"\n✅ Selected endpoint: {endpoint_path}")

    return {'endpoint': endpoint_path}


def technology_stack_selection():
    """Example: Building technology stack with multiple autocomplete prompts"""

    print("\n🛠️  Technology Stack Selection\n")

    # Programming languages
    languages = [
        'JavaScript', 'TypeScript', 'Python', 'Go', 'Rust',
        'Java', 'C++', 'Ruby', 'PHP', 'Swift', 'Kotlin'
    ]

    language = questionary.autocomplete(
        "Choose programming language:",
        choices=languages
    ).ask()

    # Frameworks based on language
    frameworks_by_language = {
        'JavaScript': ['React', 'Vue', 'Angular', 'Svelte', 'Express', 'Fastify'],
        'TypeScript': ['Next.js', 'Nest.js', 'Angular', 'Remix', 'tRPC'],
        'Python': ['Django', 'Flask', 'FastAPI', 'Tornado', 'Sanic'],
        'Go': ['Gin', 'Echo', 'Fiber', 'Chi', 'Gorilla'],
        'Rust': ['Actix', 'Rocket', 'Axum', 'Warp', 'Tide'],
        'Java': ['Spring', 'Micronaut', 'Quarkus', 'Vert.x'],
        'Ruby': ['Ruby on Rails', 'Sinatra', 'Hanami']
    }

    framework_choices = frameworks_by_language.get(language, ['None'])
    framework = questionary.autocomplete(
        f"Choose {language} framework:",
        choices=framework_choices
    ).ask()

    # Databases
    databases = [
        'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'SQLite',
        'Cassandra', 'DynamoDB', 'CouchDB', 'Neo4j', 'InfluxDB'
    ]

    database = questionary.autocomplete(
        "Choose database:",
        choices=databases
    ).ask()

    # Cloud providers
    cloud_providers = [
        'AWS', 'Google Cloud', 'Azure', 'DigitalOcean',
        'Heroku', 'Vercel', 'Netlify', 'Cloudflare'
    ]

    cloud = questionary.autocomplete(
        "Choose cloud provider:",
        choices=cloud_providers
    ).ask()

    stack = {
        'language': language,
        'framework': framework,
        'database': database,
        'cloud': cloud
    }

    print("\n✅ Technology Stack:")
    import json
    print(json.dumps(stack, indent=2))

    return stack


def file_path_autocomplete():
    """Example: File path autocomplete (simulated)"""

    print("\n📁 File Path Autocomplete Example\n")

    # Common project directories
    directories = [
        '/home/user/projects/web-app',
        '/home/user/projects/api-server',
        '/home/user/projects/cli-tool',
        '/var/www/html',
        '/opt/applications',
        '~/Documents/code',
        '~/workspace/nodejs',
        '~/workspace/python'
    ]

    project_path = questionary.autocomplete(
        "Select project directory:",
        choices=directories
    ).ask()

    # Common config files
    config_files = [
        'package.json',
        'tsconfig.json',
        'jest.config.js',
        'webpack.config.js',
        '.env',
        '.gitignore',
        'README.md',
        'Dockerfile',
        'docker-compose.yml'
    ]

    config_file = questionary.autocomplete(
        "Select config file:",
        choices=config_files
    ).ask()

    result = {
        'projectPath': project_path,
        'configFile': config_file
    }

    print("\n✅ Selected:")
    import json
    print(json.dumps(result, indent=2))

    return result


def main():
    """Run autocomplete prompt examples"""
    try:
        print("=== Autocomplete Examples ===")

        # Example 1: Basic autocomplete
        autocomplete_prompt_example()

        # Example 2: Framework search
        framework_search_example()

        # Example 3: Command search
        command_search_example()

        # Example 4: API endpoint search
        api_endpoint_search()

        # Example 5: Technology stack
        technology_stack_selection()

        # Example 6: File path autocomplete
        file_path_autocomplete()

        print("\n✅ Autocomplete examples complete!")

    except KeyboardInterrupt:
        print("\n\n❌ User interrupted prompt")
        exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
