#!/usr/bin/env python3
"""
Argument groups for better organization and help output.

Usage:
    python argument-groups.py --host 192.168.1.1 --port 8080 --ssl
    python argument-groups.py --db-host localhost --db-port 5432 --db-name mydb
    python argument-groups.py --log-level debug --log-file app.log
"""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        description='Organized arguments with groups',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # ===== Server Configuration Group =====
    server_group = parser.add_argument_group(
        'server configuration',
        'Options for configuring the web server'
    )

    server_group.add_argument(
        '--host',
        default='127.0.0.1',
        help='Server host address (default: %(default)s)'
    )

    server_group.add_argument(
        '--port', '-p',
        type=int,
        default=8080,
        help='Server port (default: %(default)s)'
    )

    server_group.add_argument(
        '--workers',
        type=int,
        default=4,
        help='Number of worker processes (default: %(default)s)'
    )

    server_group.add_argument(
        '--ssl',
        action='store_true',
        help='Enable SSL/TLS'
    )

    server_group.add_argument(
        '--cert',
        help='Path to SSL certificate (required if --ssl is set)'
    )

    server_group.add_argument(
        '--key',
        help='Path to SSL private key (required if --ssl is set)'
    )

    # ===== Database Configuration Group =====
    db_group = parser.add_argument_group(
        'database configuration',
        'Options for database connection'
    )

    db_group.add_argument(
        '--db-host',
        default='localhost',
        help='Database host (default: %(default)s)'
    )

    db_group.add_argument(
        '--db-port',
        type=int,
        default=5432,
        help='Database port (default: %(default)s)'
    )

    db_group.add_argument(
        '--db-name',
        required=True,
        help='Database name (required)'
    )

    db_group.add_argument(
        '--db-user',
        help='Database username'
    )

    db_group.add_argument(
        '--db-password',
        help='Database password'
    )

    db_group.add_argument(
        '--db-pool-size',
        type=int,
        default=10,
        help='Database connection pool size (default: %(default)s)'
    )

    # ===== Logging Configuration Group =====
    log_group = parser.add_argument_group(
        'logging configuration',
        'Options for logging and monitoring'
    )

    log_group.add_argument(
        '--log-level',
        choices=['debug', 'info', 'warning', 'error', 'critical'],
        default='info',
        help='Logging level (default: %(default)s)'
    )

    log_group.add_argument(
        '--log-file',
        help='Log to file instead of stdout'
    )

    log_group.add_argument(
        '--log-format',
        choices=['text', 'json'],
        default='text',
        help='Log format (default: %(default)s)'
    )

    log_group.add_argument(
        '--access-log',
        action='store_true',
        help='Enable access logging'
    )

    # ===== Cache Configuration Group =====
    cache_group = parser.add_argument_group(
        'cache configuration',
        'Options for caching layer'
    )

    cache_group.add_argument(
        '--cache-backend',
        choices=['redis', 'memcached', 'memory'],
        default='memory',
        help='Cache backend (default: %(default)s)'
    )

    cache_group.add_argument(
        '--cache-host',
        default='localhost',
        help='Cache server host (default: %(default)s)'
    )

    cache_group.add_argument(
        '--cache-port',
        type=int,
        default=6379,
        help='Cache server port (default: %(default)s)'
    )

    cache_group.add_argument(
        '--cache-ttl',
        type=int,
        default=300,
        help='Default cache TTL in seconds (default: %(default)s)'
    )

    # ===== Security Configuration Group =====
    security_group = parser.add_argument_group(
        'security configuration',
        'Security and authentication options'
    )

    security_group.add_argument(
        '--auth-required',
        action='store_true',
        help='Require authentication for all requests'
    )

    security_group.add_argument(
        '--jwt-secret',
        help='JWT secret key'
    )

    security_group.add_argument(
        '--cors-origins',
        nargs='+',
        help='Allowed CORS origins'
    )

    security_group.add_argument(
        '--rate-limit',
        type=int,
        default=100,
        help='Rate limit (requests per minute, default: %(default)s)'
    )

    # Parse arguments
    args = parser.parse_args()

    # Validate SSL configuration
    if args.ssl and (not args.cert or not args.key):
        parser.error("--cert and --key are required when --ssl is enabled")

    # Display configuration
    print("Configuration Summary:")

    print("\nServer:")
    print(f"  Host: {args.host}:{args.port}")
    print(f"  Workers: {args.workers}")
    print(f"  SSL: {'Enabled' if args.ssl else 'Disabled'}")
    if args.ssl:
        print(f"  Certificate: {args.cert}")
        print(f"  Key: {args.key}")

    print("\nDatabase:")
    print(f"  Host: {args.db_host}:{args.db_port}")
    print(f"  Database: {args.db_name}")
    print(f"  User: {args.db_user or '(not set)'}")
    print(f"  Pool Size: {args.db_pool_size}")

    print("\nLogging:")
    print(f"  Level: {args.log_level}")
    print(f"  File: {args.log_file or 'stdout'}")
    print(f"  Format: {args.log_format}")
    print(f"  Access Log: {'Enabled' if args.access_log else 'Disabled'}")

    print("\nCache:")
    print(f"  Backend: {args.cache_backend}")
    print(f"  Host: {args.cache_host}:{args.cache_port}")
    print(f"  TTL: {args.cache_ttl}s")

    print("\nSecurity:")
    print(f"  Auth Required: {'Yes' if args.auth_required else 'No'}")
    print(f"  CORS Origins: {args.cors_origins or '(not set)'}")
    print(f"  Rate Limit: {args.rate_limit} req/min")

    return 0


if __name__ == '__main__':
    sys.exit(main())
