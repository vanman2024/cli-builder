# Simple CLI - Basic Example

A minimal example for building a simple single-command CLI with Cobra.

## Use Case

Perfect for:
- Quick utility tools
- Single-purpose commands
- Personal automation scripts
- Simple wrappers around existing tools

## Complete Example

### main.go

```go
package main

import (
    "fmt"
    "os"

    "github.com/spf13/cobra"
)

var (
    // Flags
    input   string
    output  string
    verbose bool
    force   bool
)

var rootCmd = &cobra.Command{
    Use:   "mytool [file]",
    Short: "A simple utility tool",
    Long: `A simple command-line utility that processes files.

This tool demonstrates a basic Cobra CLI with:
- Flag management
- Argument validation
- Error handling
- Help generation`,
    Args: cobra.ExactArgs(1),
    RunE: func(cmd *cobra.Command, args []string) error {
        filename := args[0]

        if verbose {
            fmt.Printf("Processing file: %s\n", filename)
            fmt.Printf("  Input format: %s\n", input)
            fmt.Printf("  Output format: %s\n", output)
            fmt.Printf("  Force mode: %v\n", force)
        }

        // Process the file
        if err := processFile(filename, input, output, force); err != nil {
            return fmt.Errorf("failed to process file: %w", err)
        }

        fmt.Printf("Successfully processed: %s\n", filename)
        return nil
    },
}

func init() {
    // Define flags
    rootCmd.Flags().StringVarP(&input, "input", "i", "text", "input format (text|json|yaml)")
    rootCmd.Flags().StringVarP(&output, "output", "o", "text", "output format (text|json|yaml)")
    rootCmd.Flags().BoolVarP(&verbose, "verbose", "v", false, "verbose output")
    rootCmd.Flags().BoolVarP(&force, "force", "f", false, "force overwrite")

    // Set version
    rootCmd.Version = "1.0.0"
}

func processFile(filename, input, output string, force bool) error {
    // Your processing logic here
    if verbose {
        fmt.Printf("Processing %s: %s -> %s\n", filename, input, output)
    }
    return nil
}

func main() {
    if err := rootCmd.Execute(); err != nil {
        os.Exit(1)
    }
}
```

## Usage

```bash
# Build
go build -o mytool

# Show help
./mytool --help

# Process file
./mytool data.txt

# With options
./mytool data.txt --input json --output yaml --verbose

# Force mode
./mytool data.txt --force

# Show version
./mytool --version
```

## Key Features

### 1. Single Command Structure

Everything in one file - perfect for simple tools:
- Command definition
- Flag management
- Business logic
- Main function

### 2. Flag Types

```go
// String flags with shorthand
rootCmd.Flags().StringVarP(&input, "input", "i", "text", "input format")

// Boolean flags
rootCmd.Flags().BoolVarP(&verbose, "verbose", "v", false, "verbose output")

// Integer flags
var count int
rootCmd.Flags().IntVar(&count, "count", 1, "number of iterations")

// String slice flags
var tags []string
rootCmd.Flags().StringSliceVar(&tags, "tags", []string{}, "list of tags")
```

### 3. Argument Validation

```go
// Exactly one argument
Args: cobra.ExactArgs(1)

// No arguments
Args: cobra.NoArgs

// At least one argument
Args: cobra.MinimumNArgs(1)

// Between 1 and 3 arguments
Args: cobra.RangeArgs(1, 3)

// Any number of arguments
Args: cobra.ArbitraryArgs
```

### 4. Error Handling

```go
RunE: func(cmd *cobra.Command, args []string) error {
    // Return errors instead of os.Exit
    if err := validate(args); err != nil {
        return fmt.Errorf("validation failed: %w", err)
    }

    if err := process(); err != nil {
        return fmt.Errorf("processing failed: %w", err)
    }

    return nil
}
```

### 5. Auto-Generated Help

Cobra automatically generates help from your command definition:

```bash
$ ./mytool --help
A simple command-line utility that processes files.

This tool demonstrates a basic Cobra CLI with:
- Flag management
- Argument validation
- Error handling
- Help generation

Usage:
  mytool [file] [flags]

Flags:
  -f, --force           force overwrite
  -h, --help            help for mytool
  -i, --input string    input format (text|json|yaml) (default "text")
  -o, --output string   output format (text|json|yaml) (default "text")
  -v, --verbose         verbose output
      --version         version for mytool
```

## Enhancements

### Add Configuration File Support

```go
import "github.com/spf13/viper"

func init() {
    cobra.OnInitialize(initConfig)
    rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file")
}

func initConfig() {
    if cfgFile != "" {
        viper.SetConfigFile(cfgFile)
    } else {
        home, _ := os.UserHomeDir()
        viper.AddConfigPath(home)
        viper.SetConfigName(".mytool")
        viper.SetConfigType("yaml")
    }

    viper.AutomaticEnv()
    viper.ReadInConfig()
}
```

### Add Dry Run Mode

```go
var dryRun bool

func init() {
    rootCmd.Flags().BoolVar(&dryRun, "dry-run", false, "simulate without making changes")
}

func processFile(filename string) error {
    if dryRun {
        fmt.Printf("DRY RUN: Would process %s\n", filename)
        return nil
    }

    // Actual processing
    return nil
}
```

### Add Progress Indication

```go
import "github.com/schollz/progressbar/v3"

func processFile(filename string) error {
    bar := progressbar.Default(100)

    for i := 0; i < 100; i++ {
        // Do work
        bar.Add(1)
        time.Sleep(10 * time.Millisecond)
    }

    return nil
}
```

## Testing

```go
package main

import (
    "bytes"
    "testing"
)

func TestRootCommand(t *testing.T) {
    // Reset command for testing
    rootCmd.SetArgs([]string{"test.txt", "--verbose"})

    // Capture output
    buf := new(bytes.Buffer)
    rootCmd.SetOut(buf)
    rootCmd.SetErr(buf)

    // Execute
    err := rootCmd.Execute()
    if err != nil {
        t.Errorf("Expected no error, got %v", err)
    }

    // Check output
    output := buf.String()
    if !bytes.Contains([]byte(output), []byte("Processing file")) {
        t.Errorf("Expected verbose output, got: %s", output)
    }
}

func TestRootCommandRequiresArgument(t *testing.T) {
    rootCmd.SetArgs([]string{})

    err := rootCmd.Execute()
    if err == nil {
        t.Error("Expected error when no argument provided")
    }
}

func TestFlagParsing(t *testing.T) {
    rootCmd.SetArgs([]string{"test.txt", "--input", "json", "--output", "yaml"})

    err := rootCmd.Execute()
    if err != nil {
        t.Errorf("Expected no error, got %v", err)
    }

    // Verify flags were parsed
    if input != "json" {
        t.Errorf("Expected input=json, got %s", input)
    }
    if output != "yaml" {
        t.Errorf("Expected output=yaml, got %s", output)
    }
}
```

## go.mod

```go
module github.com/example/mytool

go 1.21

require github.com/spf13/cobra v1.8.0

require (
    github.com/inconshreveable/mousetrap v1.1.0 // indirect
    github.com/spf13/pflag v1.0.5 // indirect
)
```

## Build and Distribution

### Simple Build

```bash
go build -o mytool
```

### Cross-Platform Build

```bash
# Linux
GOOS=linux GOARCH=amd64 go build -o mytool-linux

# macOS
GOOS=darwin GOARCH=amd64 go build -o mytool-macos

# Windows
GOOS=windows GOARCH=amd64 go build -o mytool.exe
```

### With Version Info

```bash
VERSION=$(git describe --tags --always)
go build -ldflags "-X main.version=$VERSION" -o mytool
```

## Best Practices

1. **Keep It Simple**: Single file is fine for simple tools
2. **Use RunE**: Always return errors instead of os.Exit
3. **Provide Defaults**: Set sensible default flag values
4. **Add Examples**: Include usage examples in Long description
5. **Version Info**: Always set a version
6. **Test Thoroughly**: Write tests for command execution and flags
7. **Document Flags**: Provide clear flag descriptions

This example provides a solid foundation for building simple, production-ready CLI tools with Cobra.
