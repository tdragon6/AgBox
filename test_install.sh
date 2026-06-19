#!/bin/bash
# ============================================================================
# AgBox Installer
# By tdragon6
# ============================================================================

set -e

export UV_NO_CONFIG=1

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

AGBOX_HOME="$HOME/.agbox"
AGBOX_BACKEND="$AGBOX_HOME/backend"
AGBOX_BIN="$AGBOX_HOME/bin"
AGBOX_UV=""
REPO_URL="https://github.com/tdragon6/AgBox.git"

log_info() {
    echo -e "${CYAN}→${NC} $1"
}

log_success() {
    echo -e "${GREEN}✓${NC} $1"
}

log_error() {
    echo -e "${RED}✗${NC} $1"
}

check_command() {
    command -v "$1" > /dev/null 2>&1
}

check_requirements() {
    log_info "Checking system requirements..."
    
    if ! check_command git; then
        log_error "git is required but not installed."
        exit 1
    fi
    
    log_success "Requirements check passed"
}

clone_repository() {
    log_info "Cloning AgBox..."
    
    if [ -d "$AGBOX_HOME" ]; then
        log_info "AgBox already exists at $AGBOX_HOME"
        log_info "Updating to latest..."
        cd "$AGBOX_HOME"
        git fetch origin > /dev/null
        git checkout main > /dev/null
        git pull origin main > /dev/null
        log_success "AgBox updated"
        return 0
    fi
    
    git clone --branch main --depth 1 "$REPO_URL" "$AGBOX_HOME" > /dev/null 2>&1 \
    || {
        log_error "Failed to clone AgBox"
        log_info "Please check your network connection"
        exit 1
    }
    
    log_success "AgBox cloned successfully"
}

install_uv() {
    log_info "Installing uv..."
    
    if check_command uv; then
        AGBOX_UV="uv"
        log_success "uv is already installed in system"
        return 0
    fi
    
    AGBOX_UV="$AGBOX_BIN/uv"

    if check_command "$AGBOX_UV"; then
        log_success "uv is already installed in $AGBOX_BIN"
    else
        curl -LsSf https://astral.sh/uv/install.sh | UV_INSTALL_DIR="$AGBOX_BIN" sh  > /dev/null
        if check_command "$AGBOX_UV"; then
            log_success "uv installed successfully"
        else
            log_error "Failed to install uv"
            exit 1
        fi
    fi
}

create_virtual_env() {
    log_info "Creating Python virtual environment..."
    
    cd "$AGBOX_BACKEND"
    
    if [ -d ".venv" ]; then
        log_info "Virtual environment already exists"
        return 0
    fi
    
    "$AGBOX_UV" venv -q
    
    log_success "Virtual environment created"
}

install_dependencies() {
    log_info "Installing Python dependencies..."
    
    cd "$AGBOX_BACKEND"
    "$AGBOX_UV" sync -q
    
    log_success "Dependencies installed successfully"
}

install_command() {
    log_info "Installing agbox command..."
    
    if [ -d "/usr/local/bin" ] && [ -w "/usr/local/bin" ]; then
        BIN_DIR="/usr/local/bin"
    else
        BIN_DIR="$HOME/.local/bin"
        if ! [ -d "$HOME/.local/bin" ]; then
            mkdir -p "$BIN_DIR"        
        fi
    fi

    cat > "$BIN_DIR/agbox" << 'COMMAND_EOF'
#!/bin/bash

AGBOX_HOME="$HOME/.agbox"
AGBOX_BACKEND="$AGBOX_HOME/backend"
VENV_PYTHON="$AGBOX_BACKEND/.venv/bin/python"

exec "$VENV_PYTHON" "$AGBOX_BACKEND/cli.py" "$@"
COMMAND_EOF
    
    chmod +x "$BIN_DIR/agbox"
    
    SHELL_RC=""
    if [ -n "$BASH_VERSION" ]; then
        SHELL_RC="$HOME/.bashrc"
    elif [ -n "$ZSH_VERSION" ]; then
        SHELL_RC="$HOME/.zshrc"
    fi
    
    if [ -n "$SHELL_RC" ] && [ -f "$SHELL_RC" ]; then
        if ! grep -q "$BIN_DIR" "$SHELL_RC" 2>/dev/null; then
            echo "" >> "$SHELL_RC"
            echo "# AgBox" >> "$SHELL_RC"
            echo "export PATH=\"$BIN_DIR:\$PATH\"" >> "$SHELL_RC"
        fi
    fi
    
    log_success "agbox command installed to $BIN_DIR/agbox"
}

verify_agbox() {
    if check_command agbox; then
        agbox --help
    else
        log_info "Please run 'source $SHELL_RC' to activate agbox"
    fi
}

main() {    
    log_info "Starting AgBox installation..."
    echo ""
    
    check_requirements
    # clone_repository
    install_uv
    create_virtual_env
    install_dependencies
    install_command
    
    log_success "AgBox is ready to use!"
    echo ""
    verify_agbox
}

main