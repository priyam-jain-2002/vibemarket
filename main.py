#!/usr/bin/env python3
"""
Vibe-Leads - Quality-First Lead Generation System

Entry point for running the web application.

Usage:
    python main.py                    # Run web server
    python main.py --port 3000        # Custom port
    python main.py --host 0.0.0.0     # Expose to network
"""

import os
import sys
import argparse


def main():
    """Main entry point for Vibe-Leads web application"""

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Vibe-Leads Web Application')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=8000, help='Port to run on (default: 8000)')
    parser.add_argument('--reload', action='store_true', default=True, help='Enable auto-reload (default: True)')
    parser.add_argument('--no-reload', dest='reload', action='store_false', help='Disable auto-reload')
    args = parser.parse_args()

    # Print banner
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                                ║
║                      🎯 VIBE-LEADS                            ║
║              Quality-First Lead Generation                     ║
║                                                                ║
║              Personal Lead Generator v0.9.0                    ║
║                                                                ║
╚═══════════════════════════════════════════════════════════════╝
""")

    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  Warning: .env file not found!")
        print("   Copy .env.example to .env and add your ANTHROPIC_API_KEY")
        print()

    # Import and run
    import uvicorn

    print(f"🚀 Starting Vibe-Leads...")
    print(f"📡 Server: http://{args.host}:{args.port}")
    print(f"📊 Dashboard: http://localhost:{args.port}/dashboard")
    print(f"📖 API Docs: http://localhost:{args.port}/docs")
    print()
    print("Press Ctrl+C to stop the server")
    print()

    # Run the application
    try:
        uvicorn.run(
            "web.main:app",
            host=args.host,
            port=args.port,
            reload=args.reload,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n👋 Vibe-Leads shutting down...")
        sys.exit(0)


if __name__ == "__main__":
    main()
