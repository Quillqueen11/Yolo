#!/bin/bash
# ===========================================
# QUILL BOOTSTRAP — Auto Restore Script
# Run this when deploying on a new VPS
# ===========================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BOOTSTRAP_DIR="$PROJECT_ROOT/.bootstrap"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[BOOTSTRAP]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

echo ""
echo "==========================================="
echo "  🦊 QUILL BOOTSTRAP — Auto Restore"
echo "==========================================="
echo ""

# Step 1: Check prerequisites
log "Step 1: Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    error "Python3 not found. Install: sudo apt install python3"
fi

if ! command -v git &> /dev/null; then
    error "Git not found. Install: sudo apt install git"
fi

log "✅ Prerequisites OK"

# Step 2: Restore core identity files
log "Step 2: Restoring core identity files..."

if [ -f "$BOOTSTRAP_DIR/MEMORY.md" ]; then
    cp "$BOOTSTRAP_DIR/MEMORY.md" "$PROJECT_ROOT/MEMORY.md"
    log "✅ MEMORY.md restored"
else
    warn "⚠️ MEMORY.md not found in .bootstrap/"
fi

if [ -f "$BOOTSTRAP_DIR/SOUL.md" ]; then
    cp "$BOOTSTRAP_DIR/SOUL.md" "$PROJECT_ROOT/SOUL.md"
    log "✅ SOUL.md restored"
else
    warn "⚠️ SOUL.md not found in .bootstrap/"
fi

if [ -f "$BOOTSTRAP_DIR/PROFILE.md" ]; then
    cp "$BOOTSTRAP_DIR/PROFILE.md" "$PROJECT_ROOT/PROFILE.md"
    log "✅ PROFILE.md restored"
else
    warn "⚠️ PROFILE.md not found in .bootstrap/"
fi

# Step 3: Setup configuration
log "Step 3: Setting up configuration..."

if [ -f "$BOOTSTRAP_DIR/config.env.example" ]; then
    if [ ! -f "$PROJECT_ROOT/.env" ]; then
        cp "$BOOTSTRAP_DIR/config.env.example" "$PROJECT_ROOT/.env"
        warn "⚠️ Created .env from template"
        warn "    → Edit .env and fill in your API keys!"
    else
        log "✅ .env already exists"
    fi
else
    warn "⚠️ config.env.example not found"
fi

# Step 4: Create data directories
log "Step 4: Creating data directories..."

mkdir -p "$PROJECT_ROOT/data"
mkdir -p "$PROJECT_ROOT/survival/backup"
mkdir -p "$PROJECT_ROOT/survival/logs"
mkdir -p "$PROJECT_ROOT/survival/state"
log "✅ Directories created"

# Step 5: Install Python dependencies
log "Step 5: Installing Python dependencies..."

if [ -d "/app/venv" ]; then
    VENV_PYTHON="/app/venv/bin/python3"
elif command -v python3 &> /dev/null; then
    VENV_PYTHON="python3"
else
    error "Python3 not available"
fi

# Check if packages are installed
$VENV_PYTHON -c "import curl_cffi" 2>/dev/null || {
    warn "Installing curl_cffi..."
    $VENV_PYTHON -m pip install curl_cffi --quiet 2>/dev/null || true
}

$VENV_PYTHON -c "import fitz" 2>/dev/null || {
    warn "Installing PyMuPDF..."
    $VENV_PYTHON -m pip install PyMuPDF --quiet 2>/dev/null || true
}

$VENV_PYTHON -c "import chromadb" 2>/dev/null || {
    warn "Installing chromadb..."
    $VENV_PYTHON -m pip install chromadb --quiet 2>/dev/null || true
}

log "✅ Dependencies checked"

# Step 6: Run survival system test
log "Step 6: Running survival system test..."

if [ -f "$PROJECT_ROOT/survival/test_system.py" ]; then
    $VENV_PYTHON "$PROJECT_ROOT/survival/test_system.py" || {
        warn "⚠️ Some tests failed — check logs"
    }
else
    warn "⚠️ test_system.py not found"
fi

# Step 7: Summary
echo ""
echo "==========================================="
echo "  🦊 BOOTSTRAP COMPLETE!"
echo "==========================================="
echo ""
log "Quill has been restored!"
echo ""
echo "📋 Summary:"
echo "   • Identity files: RESTORED"
echo "   • Config: $([ -f "$PROJECT_ROOT/.env" ] && echo "CREATED" || echo "NEEDS SETUP")"
echo "   • Dependencies: CHECKED"
echo "   • System tests: RUN"
echo ""
echo "⚠️  Next steps:"
echo "   1. Edit .env and fill in API keys"
echo "   2. Run: python3 survival/check_health.py"
echo "   3. If L1: Quill is ready! 🚀"
echo ""
echo "📚 Documentation: https://github.com/Quillqueen11/Yolo"
echo ""

# Make bootstrap.sh executable
chmod +x "$SCRIPT_DIR/$(basename "$0")" 2>/dev/null || true
