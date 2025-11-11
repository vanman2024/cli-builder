package main

import (
	"database/sql"
	"fmt"
	"log"
	"os"

	"github.com/urfave/cli/v2"
)

// AppContext holds shared state across commands
type AppContext struct {
	Config  *Config
	DB      *sql.DB
	Verbose bool
}

// Config represents application configuration
type Config struct {
	Host     string
	Port     int
	Database string
}

func main() {
	app := &cli.App{
		Name:  "context-demo",
		Usage: "Demonstration of context and state management",
		Flags: []cli.Flag{
			&cli.BoolFlag{
				Name:    "verbose",
				Aliases: []string{"v"},
				Usage:   "Enable verbose output",
			},
			&cli.StringFlag{
				Name:    "config",
				Aliases: []string{"c"},
				Usage:   "Path to config file",
				Value:   "config.yaml",
			},
		},

		// Initialize shared context
		Before: func(c *cli.Context) error {
			verbose := c.Bool("verbose")
			configPath := c.String("config")

			if verbose {
				fmt.Printf("Loading config from: %s\n", configPath)
			}

			// Create application context
			appCtx := &AppContext{
				Config: &Config{
					Host:     "localhost",
					Port:     5432,
					Database: "mydb",
				},
				Verbose: verbose,
			}

			// Simulate database connection
			// In real app: appCtx.DB, err = sql.Open("postgres", connStr)
			if verbose {
				fmt.Println("Connected to database")
			}

			// Store context in app metadata
			c.App.Metadata["ctx"] = appCtx

			return nil
		},

		// Cleanup shared resources
		After: func(c *cli.Context) error {
			if ctx, ok := c.App.Metadata["ctx"].(*AppContext); ok {
				if ctx.DB != nil {
					// ctx.DB.Close()
					if ctx.Verbose {
						fmt.Println("Database connection closed")
					}
				}
			}
			return nil
		},

		Commands: []*cli.Command{
			{
				Name:  "query",
				Usage: "Execute a database query",
				Action: func(c *cli.Context) error {
					// Retrieve context
					ctx := c.App.Metadata["ctx"].(*AppContext)

					if ctx.Verbose {
						fmt.Printf("Connecting to %s:%d/%s\n",
							ctx.Config.Host,
							ctx.Config.Port,
							ctx.Config.Database)
					}

					fmt.Println("Executing query...")
					// Use ctx.DB for actual query

					return nil
				},
			},

			{
				Name:  "migrate",
				Usage: "Run database migrations",
				Action: func(c *cli.Context) error {
					// Retrieve context
					ctx := c.App.Metadata["ctx"].(*AppContext)

					if ctx.Verbose {
						fmt.Println("Running migrations with context...")
					}

					fmt.Printf("Migrating database: %s\n", ctx.Config.Database)
					// Use ctx.DB for migrations

					return nil
				},
			},

			{
				Name:  "status",
				Usage: "Check database status",
				Action: func(c *cli.Context) error {
					// Retrieve context
					ctx := c.App.Metadata["ctx"].(*AppContext)

					fmt.Printf("Database: %s\n", ctx.Config.Database)
					fmt.Printf("Host: %s:%d\n", ctx.Config.Host, ctx.Config.Port)
					fmt.Println("Status: Connected")

					if ctx.Verbose {
						fmt.Println("Verbose mode: enabled")
					}

					return nil
				},
			},
		},
	}

	if err := app.Run(os.Args); err != nil {
		log.Fatal(err)
	}
}
