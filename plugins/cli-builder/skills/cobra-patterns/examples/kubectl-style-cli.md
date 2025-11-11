# Kubectl-Style CLI Example

This example demonstrates how to build a kubectl-style CLI with nested resource commands and consistent flag handling.

## Structure

```
myctl/
├── cmd/
│   ├── root.go                 # Root command with global flags
│   ├── get/
│   │   ├── get.go             # Parent "get" command
│   │   ├── pods.go            # Get pods subcommand
│   │   ├── services.go        # Get services subcommand
│   │   └── deployments.go     # Get deployments subcommand
│   ├── create/
│   │   ├── create.go          # Parent "create" command
│   │   ├── deployment.go      # Create deployment subcommand
│   │   └── service.go         # Create service subcommand
│   ├── delete/
│   │   └── delete.go          # Delete command (accepts any resource)
│   ├── apply.go               # Apply from file/stdin
│   └── completion.go          # Shell completion
└── main.go
```

## Usage Pattern

```bash
# Get resources
myctl get pods
myctl get pods my-pod
myctl get pods --namespace production
myctl get services --all-namespaces

# Create resources
myctl create deployment my-app --image nginx:latest --replicas 3
myctl create service my-svc --port 80 --target-port 8080

# Delete resources
myctl delete pod my-pod
myctl delete deployment my-app --force

# Apply configuration
myctl apply -f deployment.yaml
myctl apply -f config.yaml --dry-run
```

## Key Features

### 1. Resource-Based Organization

Commands are organized by resource type:
- `get <resource>` - Retrieve resources
- `create <resource>` - Create resources
- `delete <resource>` - Delete resources

### 2. Consistent Flag Handling

Global flags available to all commands:
- `--namespace, -n` - Target namespace
- `--all-namespaces, -A` - Query all namespaces
- `--output, -o` - Output format (json|yaml|text)
- `--verbose, -v` - Verbose logging

### 3. Command Groups

Organized help output:
```
Basic Commands:
  get         Display resources
  describe    Show detailed information

Management Commands:
  create      Create resources
  delete      Delete resources
  apply       Apply configuration
```

## Implementation Example

### Root Command (cmd/root.go)

```go
package cmd

import (
    "github.com/spf13/cobra"
    "myctl/cmd/get"
    "myctl/cmd/create"
    "myctl/cmd/delete"
)

var (
    namespace      string
    allNamespaces  bool
    output         string
)

var rootCmd = &cobra.Command{
    Use:   "myctl",
    Short: "Kubernetes-style resource management CLI",
}

func Execute() error {
    return rootCmd.Execute()
}

func init() {
    // Global flags
    rootCmd.PersistentFlags().StringVarP(&namespace, "namespace", "n", "default", "target namespace")
    rootCmd.PersistentFlags().BoolVarP(&allNamespaces, "all-namespaces", "A", false, "query all namespaces")
    rootCmd.PersistentFlags().StringVarP(&output, "output", "o", "text", "output format (text|json|yaml)")

    // Command groups
    rootCmd.AddGroup(&cobra.Group{ID: "basic", Title: "Basic Commands:"})
    rootCmd.AddGroup(&cobra.Group{ID: "management", Title: "Management Commands:"})

    // Register commands
    rootCmd.AddCommand(get.GetCmd)
    rootCmd.AddCommand(create.CreateCmd)
    rootCmd.AddCommand(delete.DeleteCmd)
}

// Helper to get global flags
func GetNamespace() string {
    return namespace
}

func GetAllNamespaces() bool {
    return allNamespaces
}

func GetOutput() string {
    return output
}
```

### Get Command Parent (cmd/get/get.go)

```go
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
    // Add resource subcommands
    GetCmd.AddCommand(podsCmd)
    GetCmd.AddCommand(servicesCmd)
    GetCmd.AddCommand(deploymentsCmd)
}
```

### Get Pods Subcommand (cmd/get/pods.go)

```go
package get

import (
    "fmt"

    "github.com/spf13/cobra"
    "myctl/cmd"
    "myctl/internal/client"
)

var (
    selector string
    watch    bool
)

var podsCmd = &cobra.Command{
    Use:   "pods [NAME]",
    Short: "Display pods",
    Long:  `Display one or many pods`,
    Args:  cobra.MaximumNArgs(1),
    ValidArgsFunction: func(cmd *cobra.Command, args []string, toComplete string) ([]string, cobra.ShellCompDirective) {
        // Dynamic completion: fetch pod names
        return client.ListPodNames(cmd.GetNamespace()), cobra.ShellCompDirectiveNoFileComp
    },
    RunE: func(cmd *cobra.Command, args []string) error {
        namespace := cmd.GetNamespace()
        allNamespaces := cmd.GetAllNamespaces()
        output := cmd.GetOutput()

        if len(args) == 0 {
            // List pods
            return listPods(namespace, allNamespaces, selector, output)
        }

        // Get specific pod
        podName := args[0]
        return getPod(namespace, podName, output)
    },
}

func init() {
    // Command-specific flags
    podsCmd.Flags().StringVarP(&selector, "selector", "l", "", "label selector")
    podsCmd.Flags().BoolVarP(&watch, "watch", "w", false, "watch for changes")
}

func listPods(namespace string, allNamespaces bool, selector string, output string) error {
    // Implementation
    fmt.Printf("Listing pods (namespace: %s, all: %v, selector: %s, format: %s)\n",
        namespace, allNamespaces, selector, output)
    return nil
}

func getPod(namespace, name, output string) error {
    // Implementation
    fmt.Printf("Getting pod: %s (namespace: %s, format: %s)\n", name, namespace, output)
    return nil
}
```

### Create Deployment (cmd/create/deployment.go)

```go
package create

import (
    "fmt"

    "github.com/spf13/cobra"
)

var (
    image    string
    replicas int
    port     int
)

var deploymentCmd = &cobra.Command{
    Use:   "deployment NAME",
    Short: "Create a deployment",
    Args:  cobra.ExactArgs(1),
    RunE: func(cmd *cobra.Command, args []string) error {
        name := args[0]

        if image == "" {
            return fmt.Errorf("--image is required")
        }

        fmt.Printf("Creating deployment: %s\n", name)
        fmt.Printf("  Image: %s\n", image)
        fmt.Printf("  Replicas: %d\n", replicas)
        if port > 0 {
            fmt.Printf("  Container Port: %d\n", port)
        }

        return createDeployment(name, image, replicas, port)
    },
}

func init() {
    deploymentCmd.Flags().StringVar(&image, "image", "", "container image (required)")
    deploymentCmd.Flags().IntVar(&replicas, "replicas", 1, "number of replicas")
    deploymentCmd.Flags().IntVar(&port, "port", 0, "container port")

    deploymentCmd.MarkFlagRequired("image")
}

func createDeployment(name, image string, replicas, port int) error {
    // Implementation
    return nil
}
```

## Best Practices

### 1. Consistent Flag Naming
- Use single-letter shortcuts for common flags (`-n`, `-o`, `-v`)
- Use descriptive long names (`--namespace`, `--output`, `--verbose`)
- Keep flag behavior consistent across commands

### 2. Dynamic Completion
Provide shell completion for resource names:

```go
ValidArgsFunction: func(cmd *cobra.Command, args []string, toComplete string) ([]string, cobra.ShellCompDirective) {
    return client.ListResourceNames(), cobra.ShellCompDirectiveNoFileComp
}
```

### 3. Error Messages
Provide helpful error messages with suggestions:

```go
if image == "" {
    return fmt.Errorf("--image is required. Example: --image nginx:latest")
}
```

### 4. Dry Run Support
Support `--dry-run` for preview:

```go
if dryRun {
    fmt.Printf("Would create deployment: %s\n", name)
    return nil
}
```

### 5. Output Formats
Support multiple output formats:

```go
switch output {
case "json":
    return printJSON(pods)
case "yaml":
    return printYAML(pods)
default:
    return printTable(pods)
}
```

## Testing

```go
func TestGetPodsCommand(t *testing.T) {
    cmd := get.GetCmd
    cmd.SetArgs([]string{"pods", "--namespace", "production"})

    err := cmd.Execute()
    if err != nil {
        t.Errorf("Expected no error, got %v", err)
    }
}
```

## Advanced Features

### 1. Watch Mode
```go
if watch {
    return watchPods(namespace, selector)
}
```

### 2. Label Selectors
```go
podsCmd.Flags().StringVarP(&selector, "selector", "l", "", "label selector (e.g., app=nginx)")
```

### 3. Field Selectors
```go
podsCmd.Flags().StringVar(&fieldSelector, "field-selector", "", "field selector (e.g., status.phase=Running)")
```

### 4. Multiple Output Formats
```go
podsCmd.Flags().StringVarP(&output, "output", "o", "text", "output format (text|json|yaml|wide)")
```

This example provides a complete kubectl-style CLI structure that you can adapt for your resource management needs.
