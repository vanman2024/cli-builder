#!/bin/bash
# Generate complete CLI with all patterns

set -euo pipefail

APP_NAME="${1:-myapp}"

echo "Generating full-featured CLI: $APP_NAME"

# Create project structure
mkdir -p "$APP_NAME"
cd "$APP_NAME"

# Initialize Go module
go mod init "$APP_NAME" 2>/dev/null || true

# Install dependencies
echo "Installing dependencies..."
go get github.com/urfave/cli/v2@latest

# Create main.go with all patterns
cat > main.go <<'EOF'
package main

import (
	"fmt"
	"log"
	"os"

	"github.com/urfave/cli/v2"
)

// AppContext holds shared state
type AppContext struct {
	Verbose bool
	Config  string
}

func main() {
	app := &cli.App{
		Name:    "APP_NAME_PLACEHOLDER",
		Usage:   "A full-featured CLI tool with all patterns",
		Version: "0.1.0",

		// Global flags available to all commands
		Flags: []cli.Flag{
			&cli.BoolFlag{
				Name:    "verbose",
				Aliases: []string{"v"},
				Usage:   "Enable verbose output",
				EnvVars: []string{"VERBOSE"},
			},
			&cli.StringFlag{
				Name:    "config",
				Aliases: []string{"c"},
				Usage:   "Path to config file",
				EnvVars: []string{"CONFIG_PATH"},
				Value:   "config.yaml",
			},
		},

		// Before hook - runs before any command
		Before: func(c *cli.Context) error {
			verbose := c.Bool("verbose")
			config := c.String("config")

			if verbose {
				fmt.Println("🚀 Initializing application...")
			}

			// Store context for use in commands
			ctx := &AppContext{
				Verbose: verbose,
				Config:  config,
			}
			c.App.Metadata["ctx"] = ctx

			return nil
		},

		// After hook - runs after any command
		After: func(c *cli.Context) error {
			if ctx, ok := c.App.Metadata["ctx"].(*AppContext); ok {
				if ctx.Verbose {
					fmt.Println("✅ Application finished successfully")
				}
			}
			return nil
		},

		// Commands organized by category
		Commands: []*cli.Command{
			{
				Name:     "build",
				Category: "Build",
				Usage:    "Build the project",
				Flags: []cli.Flag{
					&cli.StringFlag{
						Name:    "output",
						Aliases: []string{"o"},
						Usage:   "Output file path",
						Value:   "dist/app",
					},
					&cli.BoolFlag{
						Name:  "optimize",
						Usage: "Enable optimizations",
						Value: true,
					},
				},
				Before: func(c *cli.Context) error {
					fmt.Println("Preparing build...")
					return nil
				},
				Action: func(c *cli.Context) error {
					output := c.String("output")
					optimize := c.Bool("optimize")

					fmt.Printf("Building to: %s\n", output)
					if optimize {
						fmt.Println("Optimizations: enabled")
					}

					return nil
				},
				After: func(c *cli.Context) error {
					fmt.Println("Build complete!")
					return nil
				},
			},
			{
				Name:     "test",
				Category: "Build",
				Usage:    "Run tests",
				Flags: []cli.Flag{
					&cli.BoolFlag{
						Name:    "coverage",
						Aliases: []string{"cov"},
						Usage:   "Generate coverage report",
					},
				},
				Action: func(c *cli.Context) error {
					coverage := c.Bool("coverage")

					fmt.Println("Running tests...")
					if coverage {
						fmt.Println("Generating coverage report...")
					}

					return nil
				},
			},
			{
				Name:     "deploy",
				Category: "Deploy",
				Usage:    "Deploy the application",
				Flags: []cli.Flag{
					&cli.StringFlag{
						Name:     "env",
						Aliases:  []string{"e"},
						Usage:    "Target environment",
						Required: true,
						Value:    "staging",
					},
				},
				Action: func(c *cli.Context) error {
					env := c.String("env")
					fmt.Printf("Deploying to %s...\n", env)
					return nil
				},
			},
			{
				Name:     "rollback",
				Category: "Deploy",
				Usage:    "Rollback deployment",
				Action: func(c *cli.Context) error {
					fmt.Println("Rolling back deployment...")
					return nil
				},
			},
			{
				Name:     "logs",
				Category: "Monitor",
				Usage:    "View application logs",
				Flags: []cli.Flag{
					&cli.IntFlag{
						Name:    "tail",
						Aliases: []string{"n"},
						Usage:   "Number of lines to show",
						Value:   100,
					},
					&cli.BoolFlag{
						Name:    "follow",
						Aliases: []string{"f"},
						Usage:   "Follow log output",
					},
				},
				Action: func(c *cli.Context) error {
					tail := c.Int("tail")
					follow := c.Bool("follow")

					fmt.Printf("Showing last %d lines...\n", tail)
					if follow {
						fmt.Println("Following logs...")
					}

					return nil
				},
			},
			{
				Name:     "status",
				Category: "Monitor",
				Usage:    "Check application status",
				Action: func(c *cli.Context) error {
					fmt.Println("Application status: healthy")
					return nil
				},
			},
		},
	}

	if err := app.Run(os.Args); err != nil {
		log.Fatal(err)
	}
}
EOF

# Replace placeholder
sed -i "s/APP_NAME_PLACEHOLDER/$APP_NAME/g" main.go

# Create comprehensive README
cat > README.md <<EOF
# $APP_NAME

A full-featured CLI tool demonstrating all urfave/cli patterns.

## Features

- ✅ Global flags with environment variable fallbacks
- ✅ Command categories for organization
- ✅ Before/After hooks for lifecycle management
- ✅ Context management for shared state
- ✅ Comprehensive flag types
- ✅ Subcommands and aliases
- ✅ Help text and documentation

## Installation

\`\`\`bash
go install
\`\`\`

## Usage

### Build Commands

\`\`\`bash
$APP_NAME build
$APP_NAME build --output dist/myapp --optimize
$APP_NAME test --coverage
\`\`\`

### Deploy Commands

\`\`\`bash
$APP_NAME deploy --env staging
$APP_NAME deploy -e production
$APP_NAME rollback
\`\`\`

### Monitor Commands

\`\`\`bash
$APP_NAME logs
$APP_NAME logs --tail 50 --follow
$APP_NAME status
\`\`\`

### Global Flags

\`\`\`bash
$APP_NAME --verbose build
$APP_NAME --config custom.yaml deploy --env prod
\`\`\`

## Environment Variables

- \`VERBOSE\`: Enable verbose output
- \`CONFIG_PATH\`: Path to config file

## Examples

\`\`\`bash
# Build with optimizations
$APP_NAME -v build -o dist/app --optimize

# Deploy to production
$APP_NAME --config prod.yaml deploy -e production

# Follow logs
$APP_NAME logs -f -n 200
\`\`\`
EOF

# Build
echo "Building..."
go build -o "$APP_NAME" .

echo "✅ Full-featured CLI generated successfully!"
echo ""
echo "Try these commands:"
echo "  ./$APP_NAME --help"
echo "  ./$APP_NAME build --help"
echo "  ./$APP_NAME -v build"
