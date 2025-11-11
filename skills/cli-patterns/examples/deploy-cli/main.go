package main

import (
	"fmt"
	"log"
	"os"

	"github.com/urfave/cli/v2"
)

type DeployContext struct {
	Environment string
	AWSRegion   string
	Verbose     bool
}

func main() {
	app := &cli.App{
		Name:  "deploy",
		Usage: "Deployment automation CLI",
		Flags: []cli.Flag{
			&cli.StringFlag{
				Name:     "env",
				Aliases:  []string{"e"},
				Usage:    "Target environment",
				EnvVars:  []string{"DEPLOY_ENV"},
				Required: true,
			},
			&cli.StringFlag{
				Name:    "region",
				Usage:   "AWS region",
				EnvVars: []string{"AWS_REGION"},
				Value:   "us-east-1",
			},
			&cli.BoolFlag{
				Name:    "verbose",
				Aliases: []string{"v"},
				Usage:   "Enable verbose output",
			},
		},

		Before: func(c *cli.Context) error {
			env := c.String("env")
			region := c.String("region")
			verbose := c.Bool("verbose")

			if verbose {
				fmt.Println("🔧 Setting up deployment context...")
			}

			// Validate environment
			validEnvs := []string{"dev", "staging", "production"}
			valid := false
			for _, e := range validEnvs {
				if env == e {
					valid = true
					break
				}
			}
			if !valid {
				return fmt.Errorf("invalid environment: %s (must be dev, staging, or production)", env)
			}

			// Store context
			ctx := &DeployContext{
				Environment: env,
				AWSRegion:   region,
				Verbose:     verbose,
			}
			c.App.Metadata["ctx"] = ctx

			if verbose {
				fmt.Printf("Environment: %s\n", env)
				fmt.Printf("Region: %s\n", region)
			}

			return nil
		},

		Commands: []*cli.Command{
			// Build category
			{
				Name:     "build",
				Category: "Build",
				Usage:    "Build application",
				Flags: []cli.Flag{
					&cli.StringFlag{
						Name:  "tag",
						Usage: "Docker image tag",
						Value: "latest",
					},
				},
				Action: func(c *cli.Context) error {
					ctx := c.App.Metadata["ctx"].(*DeployContext)
					tag := c.String("tag")

					fmt.Printf("Building for environment: %s\n", ctx.Environment)
					fmt.Printf("Image tag: %s\n", tag)

					return nil
				},
			},
			{
				Name:     "test",
				Category: "Build",
				Usage:    "Run tests",
				Action: func(c *cli.Context) error {
					fmt.Println("Running test suite...")
					return nil
				},
			},

			// Deploy category
			{
				Name:     "deploy",
				Category: "Deploy",
				Usage:    "Deploy application",
				Flags: []cli.Flag{
					&cli.BoolFlag{
						Name:  "auto-approve",
						Usage: "Skip confirmation prompt",
					},
				},
				Action: func(c *cli.Context) error {
					ctx := c.App.Metadata["ctx"].(*DeployContext)
					autoApprove := c.Bool("auto-approve")

					fmt.Printf("Deploying to %s in %s...\n", ctx.Environment, ctx.AWSRegion)

					if !autoApprove {
						fmt.Print("Continue? (y/n): ")
						// In real app: read user input
						fmt.Println("y")
					}

					fmt.Println("Deployment started...")

					return nil
				},
			},
			{
				Name:     "rollback",
				Category: "Deploy",
				Usage:    "Rollback to previous version",
				Action: func(c *cli.Context) error {
					ctx := c.App.Metadata["ctx"].(*DeployContext)
					fmt.Printf("Rolling back %s deployment...\n", ctx.Environment)
					return nil
				},
			},

			// Monitor category
			{
				Name:     "logs",
				Category: "Monitor",
				Usage:    "View deployment logs",
				Flags: []cli.Flag{
					&cli.BoolFlag{
						Name:    "follow",
						Aliases: []string{"f"},
						Usage:   "Follow log output",
					},
				},
				Action: func(c *cli.Context) error {
					follow := c.Bool("follow")
					fmt.Println("Fetching logs...")
					if follow {
						fmt.Println("Following logs (Ctrl+C to stop)...")
					}
					return nil
				},
			},
			{
				Name:     "status",
				Category: "Monitor",
				Usage:    "Check deployment status",
				Action: func(c *cli.Context) error {
					ctx := c.App.Metadata["ctx"].(*DeployContext)
					fmt.Printf("Deployment Status (%s):\n", ctx.Environment)
					fmt.Println("  Status: Running")
					fmt.Println("  Instances: 3/3")
					fmt.Println("  Health: Healthy")
					return nil
				},
			},
		},
	}

	if err := app.Run(os.Args); err != nil {
		log.Fatal(err)
	}
}
