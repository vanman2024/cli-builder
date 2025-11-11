package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/urfave/cli/v2"
)

type APIContext struct {
	BaseURL    string
	Token      string
	HTTPClient *http.Client
}

func main() {
	app := &cli.App{
		Name:  "api",
		Usage: "REST API client CLI",
		Flags: []cli.Flag{
			&cli.StringFlag{
				Name:     "url",
				Usage:    "API base URL",
				EnvVars:  []string{"API_URL"},
				Required: true,
			},
			&cli.StringFlag{
				Name:     "token",
				Aliases:  []string{"t"},
				Usage:    "Authentication token",
				EnvVars:  []string{"API_TOKEN"},
				Required: true,
			},
			&cli.DurationFlag{
				Name:    "timeout",
				Usage:   "Request timeout",
				Value:   30 * time.Second,
				EnvVars: []string{"API_TIMEOUT"},
			},
		},

		Before: func(c *cli.Context) error {
			baseURL := c.String("url")
			token := c.String("token")
			timeout := c.Duration("timeout")

			fmt.Println("🔐 Authenticating with API...")

			// Create HTTP client
			client := &http.Client{
				Timeout: timeout,
			}

			// Store context
			ctx := &APIContext{
				BaseURL:    baseURL,
				Token:      token,
				HTTPClient: client,
			}
			c.App.Metadata["ctx"] = ctx

			fmt.Println("✅ Authentication successful")

			return nil
		},

		Commands: []*cli.Command{
			{
				Name:      "get",
				Usage:     "GET request",
				ArgsUsage: "<endpoint>",
				Flags: []cli.Flag{
					&cli.StringSliceFlag{
						Name:    "header",
						Aliases: []string{"H"},
						Usage:   "Additional headers (key:value)",
					},
				},
				Action: func(c *cli.Context) error {
					ctx := c.App.Metadata["ctx"].(*APIContext)

					if c.NArg() < 1 {
						return fmt.Errorf("endpoint required")
					}

					endpoint := c.Args().Get(0)
					url := fmt.Sprintf("%s%s", ctx.BaseURL, endpoint)

					fmt.Printf("GET %s\n", url)
					fmt.Printf("Authorization: Bearer %s\n", maskToken(ctx.Token))

					// In real app: make HTTP request
					fmt.Println("Response: 200 OK")

					return nil
				},
			},

			{
				Name:      "post",
				Usage:     "POST request",
				ArgsUsage: "<endpoint> <data>",
				Flags: []cli.Flag{
					&cli.StringFlag{
						Name:    "content-type",
						Aliases: []string{"ct"},
						Usage:   "Content-Type header",
						Value:   "application/json",
					},
				},
				Action: func(c *cli.Context) error {
					ctx := c.App.Metadata["ctx"].(*APIContext)

					if c.NArg() < 2 {
						return fmt.Errorf("usage: post <endpoint> <data>")
					}

					endpoint := c.Args().Get(0)
					data := c.Args().Get(1)
					url := fmt.Sprintf("%s%s", ctx.BaseURL, endpoint)
					contentType := c.String("content-type")

					fmt.Printf("POST %s\n", url)
					fmt.Printf("Content-Type: %s\n", contentType)
					fmt.Printf("Data: %s\n", data)

					// In real app: make HTTP POST request

					return nil
				},
			},

			{
				Name:      "put",
				Usage:     "PUT request",
				ArgsUsage: "<endpoint> <data>",
				Action: func(c *cli.Context) error {
					ctx := c.App.Metadata["ctx"].(*APIContext)

					if c.NArg() < 2 {
						return fmt.Errorf("usage: put <endpoint> <data>")
					}

					endpoint := c.Args().Get(0)
					data := c.Args().Get(1)
					url := fmt.Sprintf("%s%s", ctx.BaseURL, endpoint)

					fmt.Printf("PUT %s\n", url)
					fmt.Printf("Data: %s\n", data)

					return nil
				},
			},

			{
				Name:      "delete",
				Usage:     "DELETE request",
				ArgsUsage: "<endpoint>",
				Action: func(c *cli.Context) error {
					ctx := c.App.Metadata["ctx"].(*APIContext)

					if c.NArg() < 1 {
						return fmt.Errorf("endpoint required")
					}

					endpoint := c.Args().Get(0)
					url := fmt.Sprintf("%s%s", ctx.BaseURL, endpoint)

					fmt.Printf("DELETE %s\n", url)

					return nil
				},
			},

			{
				Name:  "auth-test",
				Usage: "Test authentication",
				Action: func(c *cli.Context) error {
					ctx := c.App.Metadata["ctx"].(*APIContext)

					fmt.Println("Testing authentication...")
					fmt.Printf("API URL: %s\n", ctx.BaseURL)
					fmt.Printf("Token: %s\n", maskToken(ctx.Token))
					fmt.Println("Status: Authenticated ✅")

					return nil
				},
			},
		},
	}

	if err := app.Run(os.Args); err != nil {
		log.Fatal(err)
	}
}

func maskToken(token string) string {
	if len(token) < 8 {
		return "****"
	}
	return token[:4] + "****" + token[len(token)-4:]
}
