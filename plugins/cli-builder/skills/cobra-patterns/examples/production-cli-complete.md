# Complete Production CLI Example

A complete example demonstrating all production features: configuration management, error handling, logging, context support, and testing.

## Features

- ✅ Viper configuration management
- ✅ Structured logging (with levels)
- ✅ Context-aware commands (cancellation support)
- ✅ Proper error handling with wrapped errors
- ✅ Shell completion
- ✅ Unit and integration tests
- ✅ Dry-run support
- ✅ Multiple output formats
- ✅ Version information
- ✅ Configuration file support

## Complete Implementation

### main.go

```go
package main

import (
    "context"
    "os"
    "os/signal"
    "syscall"

    "github.com/example/myapp/cmd"
)

func main() {
    // Setup context with cancellation
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()

    // Handle interrupt signals gracefully
    sigChan := make(chan os.Signal, 1)
    signal.Notify(sigChan, os.Interrupt, syscall.SIGTERM)
    go func() {
        <-sigChan
        cancel()
    }()

    // Execute with context
    if err := cmd.ExecuteContext(ctx); err != nil {
        os.Exit(1)
    }
}
```

### cmd/root.go

```go
package cmd

import (
    "context"
    "fmt"
    "os"

    "github.com/spf13/cobra"
    "github.com/spf13/viper"
    "go.uber.org/zap"
    "go.uber.org/zap/zapcore"
)

var (
    cfgFile  string
    verbose  bool
    logLevel string
    logger   *zap.Logger
)

var rootCmd = &cobra.Command{
    Use:   "myapp",
    Short: "A production-grade CLI application",
    Long: `A complete production CLI with proper error handling,
configuration management, logging, and context support.`,
    Version: "1.0.0",
    PersistentPreRunE: func(cmd *cobra.Command, args []string) error {
        // Initialize logger based on flags
        return initLogger()
    },
}

func ExecuteContext(ctx context.Context) error {
    rootCmd.SetContext(ctx)
    return rootCmd.Execute()
}

func Execute() error {
    return rootCmd.Execute()
}

func init() {
    cobra.OnInitialize(initConfig)

    // Global flags
    rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file (default is $HOME/.myapp.yaml)")
    rootCmd.PersistentFlags().BoolVarP(&verbose, "verbose", "v", false, "verbose output")
    rootCmd.PersistentFlags().StringVar(&logLevel, "log-level", "info", "log level (debug|info|warn|error)")

    // Bind to viper
    viper.BindPFlag("verbose", rootCmd.PersistentFlags().Lookup("verbose"))
    viper.BindPFlag("log-level", rootCmd.PersistentFlags().Lookup("log-level"))
}

func initConfig() {
    if cfgFile != "" {
        viper.SetConfigFile(cfgFile)
    } else {
        home, err := os.UserHomeDir()
        cobra.CheckErr(err)

        viper.AddConfigPath(home)
        viper.AddConfigPath(".")
        viper.SetConfigType("yaml")
        viper.SetConfigName(".myapp")
    }

    viper.AutomaticEnv()

    if err := viper.ReadInConfig(); err == nil && verbose {
        fmt.Fprintln(os.Stderr, "Using config file:", viper.ConfigFileUsed())
    }
}

func initLogger() error {
    // Parse log level
    level := zapcore.InfoLevel
    if err := level.UnmarshalText([]byte(logLevel)); err != nil {
        return fmt.Errorf("invalid log level: %w", err)
    }

    // Create logger config
    config := zap.NewProductionConfig()
    config.Level = zap.NewAtomicLevelAt(level)

    if verbose {
        config = zap.NewDevelopmentConfig()
    }

    // Build logger
    var err error
    logger, err = config.Build()
    if err != nil {
        return fmt.Errorf("failed to initialize logger: %w", err)
    }

    return nil
}

func GetLogger() *zap.Logger {
    if logger == nil {
        // Fallback logger
        logger, _ = zap.NewProduction()
    }
    return logger
}
```

### cmd/process.go (Context-Aware Command)

```go
package cmd

import (
    "context"
    "fmt"
    "time"

    "github.com/spf13/cobra"
)

var (
    processTimeout time.Duration
    processDryRun  bool
    processWorkers int
)

var processCmd = &cobra.Command{
    Use:   "process [files...]",
    Short: "Process files with context support",
    Long: `Process files with proper context handling,
graceful cancellation, and timeout support.`,
    Args: cobra.MinimumNArgs(1),
    RunE: func(cmd *cobra.Command, args []string) error {
        ctx := cmd.Context()
        logger := GetLogger()

        // Apply timeout if specified
        if processTimeout > 0 {
            var cancel context.CancelFunc
            ctx, cancel = context.WithTimeout(ctx, processTimeout)
            defer cancel()
        }

        logger.Info("Starting process",
            zap.Strings("files", args),
            zap.Int("workers", processWorkers),
            zap.Bool("dry-run", processDryRun))

        if processDryRun {
            logger.Info("Dry run mode - no changes will be made")
            return nil
        }

        // Process with context
        if err := processFiles(ctx, args, processWorkers); err != nil {
            logger.Error("Processing failed", zap.Error(err))
            return fmt.Errorf("process failed: %w", err)
        }

        logger.Info("Processing completed successfully")
        return nil
    },
}

func init() {
    rootCmd.AddCommand(processCmd)

    processCmd.Flags().DurationVar(&processTimeout, "timeout", 0, "processing timeout")
    processCmd.Flags().BoolVar(&processDryRun, "dry-run", false, "simulate without changes")
    processCmd.Flags().IntVarP(&processWorkers, "workers", "w", 4, "number of workers")
}

func processFiles(ctx context.Context, files []string, workers int) error {
    logger := GetLogger()

    for _, file := range files {
        // Check context cancellation
        select {
        case <-ctx.Done():
            return ctx.Err()
        default:
        }

        logger.Debug("Processing file", zap.String("file", file))

        // Simulate work
        if err := processFile(ctx, file); err != nil {
            return fmt.Errorf("failed to process %s: %w", file, err)
        }
    }

    return nil
}

func processFile(ctx context.Context, file string) error {
    // Simulate processing with context awareness
    ticker := time.NewTicker(100 * time.Millisecond)
    defer ticker.Stop()

    for i := 0; i < 10; i++ {
        select {
        case <-ctx.Done():
            return ctx.Err()
        case <-ticker.C:
            // Do work
        }
    }

    return nil
}
```

### cmd/config.go (Configuration Management)

```go
package cmd

import (
    "fmt"

    "github.com/spf13/cobra"
    "github.com/spf13/viper"
)

var configCmd = &cobra.Command{
    Use:   "config",
    Short: "Manage configuration",
}

var configViewCmd = &cobra.Command{
    Use:   "view",
    Short: "View current configuration",
    RunE: func(cmd *cobra.Command, args []string) error {
        settings := viper.AllSettings()

        fmt.Println("Current Configuration:")
        fmt.Println("=====================")
        for key, value := range settings {
            fmt.Printf("%s: %v\n", key, value)
        }

        return nil
    },
}

var configSetCmd = &cobra.Command{
    Use:   "set KEY VALUE",
    Short: "Set configuration value",
    Args:  cobra.ExactArgs(2),
    RunE: func(cmd *cobra.Command, args []string) error {
        key := args[0]
        value := args[1]

        viper.Set(key, value)

        if err := viper.WriteConfig(); err != nil {
            if err := viper.SafeWriteConfig(); err != nil {
                return fmt.Errorf("failed to write config: %w", err)
            }
        }

        fmt.Printf("Set %s = %s\n", key, value)
        return nil
    },
}

func init() {
    rootCmd.AddCommand(configCmd)
    configCmd.AddCommand(configViewCmd)
    configCmd.AddCommand(configSetCmd)
}
```

### cmd/version.go

```go
package cmd

import (
    "fmt"
    "runtime"

    "github.com/spf13/cobra"
)

var (
    Version   = "dev"
    Commit    = "none"
    BuildTime = "unknown"
)

var versionCmd = &cobra.Command{
    Use:   "version",
    Short: "Print version information",
    Run: func(cmd *cobra.Command, args []string) {
        fmt.Printf("myapp version %s\n", Version)
        fmt.Printf("  Commit:     %s\n", Commit)
        fmt.Printf("  Built:      %s\n", BuildTime)
        fmt.Printf("  Go version: %s\n", runtime.Version())
        fmt.Printf("  OS/Arch:    %s/%s\n", runtime.GOOS, runtime.GOARCH)
    },
}

func init() {
    rootCmd.AddCommand(versionCmd)
}
```

### Testing (cmd/root_test.go)

```go
package cmd

import (
    "bytes"
    "context"
    "testing"
    "time"
)

func TestProcessCommand(t *testing.T) {
    // Reset command for testing
    processCmd.SetArgs([]string{"file1.txt", "file2.txt"})

    // Capture output
    buf := new(bytes.Buffer)
    processCmd.SetOut(buf)
    processCmd.SetErr(buf)

    // Execute
    err := processCmd.Execute()
    if err != nil {
        t.Errorf("Expected no error, got %v", err)
    }
}

func TestProcessCommandWithContext(t *testing.T) {
    ctx, cancel := context.WithTimeout(context.Background(), 1*time.Second)
    defer cancel()

    processCmd.SetContext(ctx)
    processCmd.SetArgs([]string{"file1.txt"})

    err := processCmd.Execute()
    if err != nil {
        t.Errorf("Expected no error, got %v", err)
    }
}

func TestProcessCommandCancellation(t *testing.T) {
    ctx, cancel := context.WithCancel(context.Background())

    processCmd.SetContext(ctx)
    processCmd.SetArgs([]string{"file1.txt", "file2.txt"})

    // Cancel context immediately
    cancel()

    err := processCmd.Execute()
    if err == nil {
        t.Error("Expected context cancellation error")
    }
}

func TestConfigViewCommand(t *testing.T) {
    configViewCmd.SetArgs([]string{})

    buf := new(bytes.Buffer)
    configViewCmd.SetOut(buf)

    err := configViewCmd.Execute()
    if err != nil {
        t.Errorf("Expected no error, got %v", err)
    }

    output := buf.String()
    if output == "" {
        t.Error("Expected output, got empty string")
    }
}
```

### Configuration File (.myapp.yaml)

```yaml
# Application configuration
verbose: false
log-level: info
timeout: 30s

# Custom settings
api:
  endpoint: https://api.example.com
  timeout: 10s
  retries: 3

database:
  host: localhost
  port: 5432
  name: myapp

features:
  experimental: false
  beta: true
```

### Makefile

```makefile
VERSION := $(shell git describe --tags --always --dirty)
COMMIT := $(shell git rev-parse HEAD)
BUILD_TIME := $(shell date -u '+%Y-%m-%d_%H:%M:%S')

LDFLAGS := -X github.com/example/myapp/cmd.Version=$(VERSION) \
           -X github.com/example/myapp/cmd.Commit=$(COMMIT) \
           -X github.com/example/myapp/cmd.BuildTime=$(BUILD_TIME)

.PHONY: build
build:
	go build -ldflags "$(LDFLAGS)" -o myapp

.PHONY: test
test:
	go test -v ./...

.PHONY: coverage
coverage:
	go test -coverprofile=coverage.out ./...
	go tool cover -html=coverage.out

.PHONY: lint
lint:
	golangci-lint run

.PHONY: install
install:
	go install -ldflags "$(LDFLAGS)"

.PHONY: clean
clean:
	rm -f myapp coverage.out
```

## Usage Examples

```bash
# Basic usage with verbose logging
myapp process file.txt -v

# With timeout and workers
myapp process *.txt --timeout 30s --workers 8

# Dry run
myapp process file.txt --dry-run

# Custom config file
myapp --config prod.yaml process file.txt

# View configuration
myapp config view

# Set configuration
myapp config set api.timeout 15s

# Version information
myapp version

# Shell completion
myapp completion bash > /etc/bash_completion.d/myapp
```

## Key Patterns

1. **Context Awareness**: All long-running operations respect context cancellation
2. **Structured Logging**: Use zap for performance and structure
3. **Configuration Management**: Viper for flexible config handling
4. **Error Wrapping**: Use fmt.Errorf with %w for error chains
5. **Testing**: Comprehensive unit and integration tests
6. **Build Info**: Version, commit, and build time injection

This example provides a complete production-ready CLI that you can use as a foundation for your own applications.
