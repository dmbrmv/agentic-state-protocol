#!/bin/bash
# Agentic State Protocol v3.0 - Adoption Script
#
# Add the protocol to an existing project with a single command:
#   curl -sL https://raw.githubusercontent.com/USER/agentic-state-protocol/main/adopt.sh | bash
#
# Or run locally:
#   ./adopt.sh
#
# Options:
#   --minimal    Only copy .claude/ folder (no docs templates)
#   --full       Copy everything including doc templates (default)
#   --force      Overwrite existing files without prompting

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REPO_URL="${ASP_REPO_URL:-https://github.com/USER/agentic-state-protocol}"
BRANCH="${ASP_BRANCH:-main}"
MODE="full"
FORCE=false
LOCAL_PATH=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --minimal) MODE="minimal"; shift ;;
        --full) MODE="full"; shift ;;
        --force) FORCE=true; shift ;;
        --local) LOCAL_PATH="$2"; shift 2 ;;
        --help|-h)
            echo "Agentic State Protocol - Adoption Script"
            echo ""
            echo "Usage: ./adopt.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --minimal        Only copy .claude/ folder (commands, skills, agents)"
            echo "  --full           Copy everything including doc templates (default)"
            echo "  --force          Overwrite existing files without prompting"
            echo "  --local <path>   Use local repo path instead of downloading"
            echo "  --help           Show this help message"
            echo ""
            echo "Examples:"
            echo "  ./adopt.sh                           # Full install from GitHub"
            echo "  ./adopt.sh --minimal                 # Just .claude/ folder"
            echo "  ./adopt.sh --local /path/to/repo     # From local clone"
            exit 0
            ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║       Agentic State Protocol v3.0 - Adoption Script        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if we're in a git repo or project directory
if [ ! -d ".git" ] && [ ! -f "package.json" ] && [ ! -f "pyproject.toml" ] && [ ! -f "Cargo.toml" ] && [ ! -f "go.mod" ]; then
    echo -e "${YELLOW}Warning: This doesn't look like a project root directory.${NC}"
    echo "Current directory: $(pwd)"
    read -p "Continue anyway? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 1
    fi
fi

# Check for existing .claude directory
if [ -d ".claude" ] && [ "$FORCE" = false ]; then
    echo -e "${YELLOW}Found existing .claude/ directory.${NC}"
    read -p "Merge with existing? (existing files will be preserved) [Y/n] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Nn]$ ]]; then
        echo "Aborted. Use --force to overwrite."
        exit 1
    fi
fi

# Create temp directory for download (unless using local path)
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# Get the source files
if [ -n "$LOCAL_PATH" ]; then
    echo -e "${BLUE}Using local repository: $LOCAL_PATH${NC}"
    if [ ! -d "$LOCAL_PATH/.claude" ]; then
        echo -e "${RED}Error: $LOCAL_PATH/.claude not found${NC}"
        exit 1
    fi
    # Symlink to temp for consistent handling
    ln -s "$LOCAL_PATH" "$TEMP_DIR/repo"
    echo -e "${GREEN}✓ Found local files${NC}"
else
    echo -e "${BLUE}Downloading protocol files...${NC}"

    # Download the repository
    if command -v git &> /dev/null; then
        git clone --depth 1 --branch "$BRANCH" "$REPO_URL" "$TEMP_DIR/repo" 2>/dev/null || {
            echo -e "${YELLOW}Git clone failed, trying curl...${NC}"
            curl -sL "$REPO_URL/archive/$BRANCH.tar.gz" | tar xz -C "$TEMP_DIR"
            mv "$TEMP_DIR"/agentic-state-protocol-* "$TEMP_DIR/repo"
        }
    else
        curl -sL "$REPO_URL/archive/$BRANCH.tar.gz" | tar xz -C "$TEMP_DIR"
        mv "$TEMP_DIR"/agentic-state-protocol-* "$TEMP_DIR/repo"
    fi

    echo -e "${GREEN}✓ Downloaded${NC}"
fi

# Copy .claude directory (always)
echo -e "${BLUE}Installing .claude/ directory...${NC}"
mkdir -p .claude
cp -rn "$TEMP_DIR/repo/.claude/"* .claude/ 2>/dev/null || cp -r "$TEMP_DIR/repo/.claude/"* .claude/

echo -e "${GREEN}✓ Installed .claude/ (commands, skills, agents, hooks, contexts)${NC}"

# Full mode: also copy doc templates
if [ "$MODE" = "full" ]; then
    echo -e "${BLUE}Installing documentation templates...${NC}"

    # Create docs structure
    mkdir -p docs/logs
    mkdir -p docs/adrs

    # Copy MASTER_INDEX (always useful)
    if [ ! -f "docs/00_MASTER_INDEX.md" ]; then
        cp "$TEMP_DIR/repo/docs/00_MASTER_INDEX.md" docs/
        echo -e "${GREEN}  ✓ docs/00_MASTER_INDEX.md${NC}"
    else
        echo -e "${YELLOW}  ⊘ docs/00_MASTER_INDEX.md (exists, skipped)${NC}"
    fi

    # Copy templates for user to customize
    for template in "$TEMP_DIR/repo/docs/"*.template; do
        if [ -f "$template" ]; then
            basename=$(basename "$template" .template)
            if [ ! -f "docs/$basename" ]; then
                cp "$template" "docs/$basename.template"
                echo -e "${GREEN}  ✓ docs/$basename.template${NC}"
            else
                echo -e "${YELLOW}  ⊘ docs/$basename (exists, skipped)${NC}"
            fi
        fi
    done

    # Copy session context template
    if [ ! -f "docs/logs/session_context.md" ]; then
        if [ -f "$TEMP_DIR/repo/docs/logs/session_context.md.template" ]; then
            cp "$TEMP_DIR/repo/docs/logs/session_context.md.template" docs/logs/
            echo -e "${GREEN}  ✓ docs/logs/session_context.md.template${NC}"
        fi
    fi

    # Add .gitkeep to adrs
    touch docs/adrs/.gitkeep
fi

# Check/create CLAUDE.md
if [ ! -f "CLAUDE.md" ]; then
    if [ -f "$TEMP_DIR/repo/CLAUDE.md.template" ]; then
        cp "$TEMP_DIR/repo/CLAUDE.md.template" CLAUDE.md.template
        echo -e "${GREEN}✓ Created CLAUDE.md.template (rename to CLAUDE.md and customize)${NC}"
    fi
else
    echo -e "${YELLOW}⊘ CLAUDE.md exists - consider merging with protocol instructions${NC}"
fi

# Make hooks executable
chmod +x .claude/hooks/*.sh 2>/dev/null || true
chmod +x .claude/hooks/*.py 2>/dev/null || true

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║              Installation Complete!                        ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Summary
echo -e "${BLUE}What was installed:${NC}"
echo "  .claude/commands/     - 22 CLI commands (/boot, /tdd, /review, etc.)"
echo "  .claude/skills/       - 7 auto-enforced behaviors"
echo "  .claude/agents/       - 8 specialized subagents"
echo "  .claude/contexts/     - 3 working modes (dev, research, review)"
echo "  .claude/hooks/        - 5 automation hooks"

if [ "$MODE" = "full" ]; then
    echo "  docs/                 - Documentation templates"
fi

echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "  1. Rename *.template files and customize for your project"
echo "  2. If you have CLAUDE.md, merge protocol instructions into it"
echo "  3. Start a session with: /boot"
echo ""
echo -e "${BLUE}Quick commands to try:${NC}"
echo "  /boot          - Start session, load context"
echo "  /status        - Project health dashboard"
echo "  /tdd <feature> - Test-driven development"
echo "  /review        - Code review"
echo ""
echo -e "Documentation: ${BLUE}docs/00_MASTER_INDEX.md${NC}"
echo ""
