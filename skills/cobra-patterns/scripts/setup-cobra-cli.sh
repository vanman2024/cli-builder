#!/bin/bash

# Setup Cobra CLI with chosen structure pattern
# Usage: ./setup-cobra-cli.sh <cli-name> <structure-type>

set -euo pipefail

CLI_NAME="${1:-}"
STRUCTURE_TYPE="${2:-flat}"

if [ -z "$CLI_NAME" ]; then
    echo "Error: CLI name required"
    echo "Usage: $0 <cli-name> <structure-type>"
    echo "Structure types: simple, flat, nested, plugin, hybrid"
    exit 1
fi

# Validate structure type
case "$STRUCTURE_TYPE" in
    simple|flat|nested|plugin|hybrid)
        ;;
    *)
        echo "Error: Invalid structure type: $STRUCTURE_TYPE"
        echo "Valid types: simple, flat, nested, plugin, hybrid"
        exit 1
        ;;
esac

echo "Creating Cobra CLI: $CLI_NAME with $STRUCTURE_TYPE structure..."

# Create directory structure
mkdir -p "$CLI_NAME"
cd "$CLI_NAME"

# Initialize Go module
go mod init "$CLI_NAME" 2>/dev/null || echo "Go module already initialized"

# Create base directories
mkdir -p cmd
mkdir -p internal

# Install Cobra
echo "Installing Cobra dependency..."
go get -u github.com/spf13/cobra@latest

case "$STRUCTURE_TYPE" in
    simple)
        # Single command CLI
        cat > main.go << 'EOF'
package main

import (
    "fmt"
    "os"

    "github.com/spf13/cobra"
)

var (
    verbose bool
)

var rootCmd = &cobra.Command{
    Use:   "CLI_NAME",
    Short: "A simple CLI tool",
    Long:  `A simple command-line tool built with Cobra.`,
    RunE: func(cmd *cobra.Command, args []string) error {
        if verbose {
            fmt.Println("Running in verbose mode")
        }
        fmt.Println("Hello from CLI_NAME!")
        return nil
    },
}

func init() {
    rootCmd.Flags().BoolVarP(&verbose, "verbose", "v", false, "verbose output")
}

func main() {
    if err := rootCmd.Execute(); err != nil {
        os.Exit(1)
    }
}
EOF
        sed -i "s/CLI_NAME/$CLI_NAME/g" main.go
        ;;

    flat)
        # Root with subcommands at one level
        cat > cmd/root.go << 'EOF'
package cmd

import (
    "os"

    "github.com/spf13/cobra"
)

var (
    cfgFile string
    verbose bool
)

var rootCmd = &cobra.Command{
    Use:   "CLI_NAME",
    Short: "A CLI tool with flat command structure",
    Long:  `A command-line tool with subcommands at a single level.`,
}

func Execute() error {
    return rootCmd.Execute()
}

func init() {
    rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file")
    rootCmd.PersistentFlags().BoolVarP(&verbose, "verbose", "v", false, "verbose output")
}
EOF

        cat > cmd/get.go << 'EOF'
package cmd

import (
    "fmt"

    "github.com/spf13/cobra"
)

var getCmd = &cobra.Command{
    Use:   "get [resource]",
    Short: "Get resources",
    Long:  `Retrieve and display resources`,
    Args:  cobra.MinimumNArgs(1),
    RunE: func(cmd *cobra.Command, args []string) error {
        fmt.Printf("Getting resource: %s\n", args[0])
        return nil
    },
}

func init() {
    rootCmd.AddCommand(getCmd)
}
EOF

        cat > cmd/create.go << 'EOF'
package cmd

import (
    "fmt"

    "github.com/spf13/cobra"
)

var (
    createName string
)

var createCmd = &cobra.Command{
    Use:   "create",
    Short: "Create resources",
    Long:  `Create new resources`,
    RunE: func(cmd *cobra.Command, args []string) error {
        if createName == "" {
            return fmt.Errorf("name is required")
        }
        fmt.Printf("Creating resource: %s\n", createName)
        return nil
    },
}

func init() {
    createCmd.Flags().StringVarP(&createName, "name", "n", "", "resource name (required)")
    createCmd.MarkFlagRequired("name")
    rootCmd.AddCommand(createCmd)
}
EOF

        cat > main.go << 'EOF'
package main

import (
    "os"
    "CLI_NAME/cmd"
)

func main() {
    if err := cmd.Execute(); err != nil {
        os.Exit(1)
    }
}
EOF
        sed -i "s/CLI_NAME/$CLI_NAME/g" main.go cmd/root.go
        ;;

    nested)
        # kubectl-style nested commands
        mkdir -p cmd/get cmd/create cmd/delete

        cat > cmd/root.go << 'EOF'
package cmd

import (
    "fmt"
    "os"

    "github.com/spf13/cobra"
)

var (
    cfgFile  string
    verbose  bool
    output   string
)

var rootCmd = &cobra.Command{
    Use:   "CLI_NAME",
    Short: "A production-grade CLI tool",
    Long: `A complete CLI application with nested command structure.

This CLI demonstrates kubectl-style command organization with
hierarchical commands and consistent flag handling.`,
}

func Execute() error {
    return rootCmd.Execute()
}

func init() {
    cobra.OnInitialize(initConfig)

    // Global flags
    rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file")
    rootCmd.PersistentFlags().BoolVarP(&verbose, "verbose", "v", false, "verbose output")
    rootCmd.PersistentFlags().StringVarP(&output, "output", "o", "text", "output format (text|json|yaml)")

    // Command groups
    rootCmd.AddGroup(&cobra.Group{
        ID:    "basic",
        Title: "Basic Commands:",
    })
    rootCmd.AddGroup(&cobra.Group{
        ID:    "management",
        Title: "Management Commands:",
    })
}

func initConfig() {
    if verbose {
        fmt.Fprintln(os.Stderr, "Verbose mode enabled")
    }
    if cfgFile != "" {
        fmt.Fprintf(os.Stderr, "Using config file: %s\n", cfgFile)
    }
}
EOF

        cat > cmd/get/get.go << 'EOF'
package get

import (
    "github.com/spf13/cobra"
)

var GetCmd = &cobra.Command{
    Use:     "get",
    Short:   "Display resources",
    Long:    `Display one or many resources`,
    GroupID: "basic",
}

func init() {
    GetCmd.AddCommand(podsCmd)
    GetCmd.AddCommand(servicesCmd)
}
EOF

        cat > cmd/get/pods.go << 'EOF'
package get

import (
    "fmt"

    "github.com/spf13/cobra"
)

var (
    namespace string
    allNamespaces bool
)

var podsCmd = &cobra.Command{
    Use:   "pods [NAME]",
    Short: "Display pods",
    Long:  `Display one or many pods`,
    Args:  cobra.MaximumNArgs(1),
    RunE: func(cmd *cobra.Command, args []string) error {
        if allNamespaces {
            fmt.Println("Listing pods in all namespaces")
        } else {
            fmt.Printf("Listing pods in namespace: %s\n", namespace)
        }
        if len(args) > 0 {
            fmt.Printf("Showing pod: %s\n", args[0])
        }
        return nil
    },
}

func init() {
    podsCmd.Flags().StringVarP(&namespace, "namespace", "n", "default", "namespace")
    podsCmd.Flags().BoolVarP(&allNamespaces, "all-namespaces", "A", false, "list across all namespaces")
}
EOF

        cat > cmd/get/services.go << 'EOF'
package get

import (
    "fmt"

    "github.com/spf13/cobra"
)

var servicesCmd = &cobra.Command{
    Use:   "services [NAME]",
    Short: "Display services",
    Long:  `Display one or many services`,
    Args:  cobra.MaximumNArgs(1),
    RunE: func(cmd *cobra.Command, args []string) error {
        fmt.Println("Listing services")
        if len(args) > 0 {
            fmt.Printf("Showing service: %s\n", args[0])
        }
        return nil
    },
}
EOF

        cat > cmd/create/create.go << 'EOF'
package create

import (
    "github.com/spf13/cobra"
)

var CreateCmd = &cobra.Command{
    Use:     "create",
    Short:   "Create resources",
    Long:    `Create resources from files or stdin`,
    GroupID: "management",
}

func init() {
    CreateCmd.AddCommand(deploymentCmd)
}
EOF

        cat > cmd/create/deployment.go << 'EOF'
package create

import (
    "fmt"

    "github.com/spf13/cobra"
)

var (
    image    string
    replicas int
)

var deploymentCmd = &cobra.Command{
    Use:   "deployment NAME",
    Short: "Create a deployment",
    Long:  `Create a deployment with the specified name`,
    Args:  cobra.ExactArgs(1),
    RunE: func(cmd *cobra.Command, args []string) error {
        name := args[0]
        fmt.Printf("Creating deployment: %s\n", name)
        fmt.Printf("  Image: %s\n", image)
        fmt.Printf("  Replicas: %d\n", replicas)
        return nil
    },
}

func init() {
    deploymentCmd.Flags().StringVar(&image, "image", "", "container image (required)")
    deploymentCmd.Flags().IntVar(&replicas, "replicas", 1, "number of replicas")
    deploymentCmd.MarkFlagRequired("image")
}
EOF

        cat > cmd/delete/delete.go << 'EOF'
package delete

import (
    "fmt"

    "github.com/spf13/cobra"
)

var (
    force bool
)

var DeleteCmd = &cobra.Command{
    Use:     "delete",
    Short:   "Delete resources",
    Long:    `Delete resources by names, stdin, or resources`,
    GroupID: "management",
    Args:    cobra.MinimumNArgs(1),
    RunE: func(cmd *cobra.Command, args []string) error {
        for _, resource := range args {
            if force {
                fmt.Printf("Force deleting: %s\n", resource)
            } else {
                fmt.Printf("Deleting: %s\n", resource)
            }
        }
        return nil
    },
}

func init() {
    DeleteCmd.Flags().BoolVarP(&force, "force", "f", false, "force deletion")
}
EOF

        # Update root to add nested commands
        cat >> cmd/root.go << 'EOF'

func init() {
    // Add command imports at the top of your root.go:
    // import (
    //     "CLI_NAME/cmd/get"
    //     "CLI_NAME/cmd/create"
    //     "CLI_NAME/cmd/delete"
    // )

    // Uncomment after fixing imports:
    // rootCmd.AddCommand(get.GetCmd)
    // rootCmd.AddCommand(create.CreateCmd)
    // rootCmd.AddCommand(delete.DeleteCmd)
}
EOF

        cat > main.go << 'EOF'
package main

import (
    "os"
    "CLI_NAME/cmd"
    _ "CLI_NAME/cmd/get"
    _ "CLI_NAME/cmd/create"
    _ "CLI_NAME/cmd/delete"
)

func main() {
    if err := cmd.Execute(); err != nil {
        os.Exit(1)
    }
}
EOF
        sed -i "s/CLI_NAME/$CLI_NAME/g" main.go cmd/root.go
        ;;

    plugin)
        echo "Plugin structure not yet implemented"
        exit 1
        ;;

    hybrid)
        echo "Hybrid structure not yet implemented"
        exit 1
        ;;
esac

# Create .gitignore
cat > .gitignore << 'EOF'
# Binaries
*.exe
*.exe~
*.dll
*.so
*.dylib
/CLI_NAME

# Test binary
*.test

# Coverage
*.out
*.prof

# Go workspace
go.work
go.work.sum

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
EOF
sed -i "s/CLI_NAME/$CLI_NAME/g" .gitignore

# Create README
cat > README.md << 'EOF'
# CLI_NAME

A CLI tool built with Cobra.

## Installation

```bash
go install
```

## Usage

```bash
CLI_NAME --help
```

## Development

Build:
```bash
go build -o CLI_NAME
```

Run:
```bash
./CLI_NAME
```

Test:
```bash
go test ./...
```

## Structure

This CLI uses STRUCTURE_TYPE command structure.
EOF
sed -i "s/CLI_NAME/$CLI_NAME/g" README.md
sed -i "s/STRUCTURE_TYPE/$STRUCTURE_TYPE/g" README.md

# Initialize dependencies
echo "Downloading dependencies..."
go mod tidy

echo ""
echo "✓ CLI created successfully: $CLI_NAME"
echo ""
echo "Next steps:"
echo "  cd $CLI_NAME"
echo "  go build -o $CLI_NAME"
echo "  ./$CLI_NAME --help"
echo ""
