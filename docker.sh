#!/bin/bash
# ============================================================================
# agbox docker cli wrapper
# By tdragon6
# ============================================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

AGBOX_IMAGE_NAME="tdragon6/agbox:latest"
AGBOX_HOME="$HOME/.agbox"
AGBOX_ENV="$AGBOX_HOME/backend/env"
AGBOX_STORE="$AGBOX_HOME/store"
AGBOX_WORKSPACE="$HOME/.agbox_workspace"
AGBOX_CONTAINER_HOME="/root/.agbox"
AGBOX_CONTAINER_ENV="$AGBOX_CONTAINER_HOME/backend/env"
AGBOX_CONTAINER_STORE="$AGBOX_CONTAINER_HOME/store"
AGBOX_CONTAINER_WORKSPACE="/root/.agbox_workspace"
DETACH="-it"

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

pull_image() {
    docker image inspect "$AGBOX_IMAGE_NAME" > /dev/null 2>&1 || docker pull "$AGBOX_IMAGE_NAME"
}

docker_cli() {
    docker run $DETACH --rm \
    -p 8000:8000 \
    -v "/etc/localtime:/etc/localtime:ro" \
    -v "/etc/timezone:/etc/timezone:ro" \
    -v "$AGBOX_ENV:$AGBOX_CONTAINER_ENV" \
    -v "$AGBOX_STORE:$AGBOX_CONTAINER_STORE" \
    -v "$AGBOX_WORKSPACE:$AGBOX_CONTAINER_WORKSPACE" \
    "$AGBOX_IMAGE_NAME" \
    "$@"
}

main() {
    if ! check_command "docker"; then
        log_error "Docker is not installed"
        exit 1
    fi

    if [[ "$1" == "-d" ]]; then
        DETACH="-d"
        shift
    fi

    if [[ "$1" == "start" ]]; then
        if [[ "$2" == "-d" || "$2" == "--daemon" ]]; then
            log_error "AgBox daemon mode is not supported in docker start"
            exit 1
        fi
    fi

    if [[ "$1" == "stop" ]]; then
        log_error "AgBox stop command is not supported in docker mode"
        exit 1
    fi

    pull_image
    
    docker_cli "$@"
}

main "$@"