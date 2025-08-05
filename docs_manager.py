#!/usr/bin/env python3
"""
Documentation generation script for pyGCodeDecode.

This script automates the process of generating documentation using
pydoc-markdown and serving it with mkdocs.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a shell command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout.strip():
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr.strip()}")
        return False


def generate_docs():
    """Generate API documentation using pydoc-markdown."""
    print("📚 Generating API documentation...")

    # Change to project root directory
    project_root = Path(__file__).parent
    os.chdir(project_root)

    # Generate documentation
    if not run_command("pydoc-markdown", "Generating API documentation with pydoc-markdown"):
        return False

    print("✅ Documentation generation completed!")
    return True


def serve_docs():
    """Serve documentation using mkdocs."""
    print("🌐 Starting documentation server...")

    docs_dir = Path(__file__).parent / "docs"
    os.chdir(docs_dir)

    print("Starting mkdocs server at http://127.0.0.1:8000")
    print("Press Ctrl+C to stop the server")

    try:
        subprocess.run("mkdocs serve", shell=True, check=True)
    except KeyboardInterrupt:
        print("\n👋 Documentation server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start mkdocs server: {e}")
        return False

    return True


def build_docs():
    """Build static documentation files."""
    print("🏗️ Building static documentation...")

    docs_dir = Path(__file__).parent / "docs"
    os.chdir(docs_dir)

    return run_command("mkdocs build", "Building static documentation")


def main():
    """Handle command line arguments and execute requested actions."""
    if len(sys.argv) < 2:
        print("📖 pyGCodeDecode Documentation Manager")
        print("\nUsage:")
        print("  python docs_manager.py generate  - Generate API documentation")
        print("  python docs_manager.py serve     - Serve documentation locally")
        print("  python docs_manager.py build     - Build static documentation")
        print("  python docs_manager.py all       - Generate and serve documentation")
        return

    command = sys.argv[1].lower()

    if command == "generate":
        generate_docs()
    elif command == "serve":
        serve_docs()
    elif command == "build":
        if generate_docs():
            build_docs()
    elif command == "all":
        if generate_docs():
            serve_docs()
    else:
        print(f"❌ Unknown command: {command}")
        print("Available commands: generate, serve, build, all")


if __name__ == "__main__":
    main()
