#!/usr/bin/env bash
set -e # This makes the script exit immediately if any command exits with a non-zero status.

IMAGE="ghcr.io/joaocb2002/object-nav-habitat/habitat-project:main"
WORKDIR="/workspace"

# Set up data and output directories in the current working directory by default.
DATA_DIR="${DATA_DIR:-$PWD/datasets}"
OUTPUT_DIR="${OUTPUT_DIR:-$PWD/outputs}"

# Create data and output directories if they don't exist. If they already exist, do nothing.
mkdir -p "$OUTPUT_DIR"
mkdir -p "$DATA_DIR"

# If no command is provided, drop into an interactive shell after installing the package.
if [ $# -eq 0 ]; then
  docker run --rm -it \
    --ipc=host \
    --gpus all \
    --user "$(id -u):$(id -g)" \
    -e HOME=/workspace \
    -e NVIDIA_DRIVER_CAPABILITIES=all \
    -e NVIDIA_VISIBLE_DEVICES=all \
    -v /etc/passwd:/etc/passwd:ro \
    -v /etc/group:/etc/group:ro \
    -v "$(pwd)":"$WORKDIR" \
    -v "$DATA_DIR":/data:ro \
    -v "$OUTPUT_DIR":/outputs \
    -w "$WORKDIR" \
    $IMAGE \
    bash -lc "pip install --user -e . && exec bash"
else
  # Run the provided command after installing the package.
  docker run --rm -it \
    --ipc=host \
    --gpus all \
    --user "$(id -u):$(id -g)" \
    -e HOME=/workspace \
    -e NVIDIA_DRIVER_CAPABILITIES=all \
    -e NVIDIA_VISIBLE_DEVICES=all \
    -v /etc/passwd:/etc/passwd:ro \
    -v /etc/group:/etc/group:ro \
    -v "$(pwd)":"$WORKDIR" \
    -v "$DATA_DIR":/data:ro \
    -v "$OUTPUT_DIR":/outputs \
    -w "$WORKDIR" \
    $IMAGE \
    bash -lc "pip install --user -e . && exec \"\$@\"" -- "$@"
fi

# Note: The use of 'bash -lc' ensures that the user's shell environment is loaded, allowing access to user-installed packages.

# Note: The use of 'exec "$@"' allows passing arbitrary commands to the container.

# Note: The use of --user "$(id -u):$(id -g)" runs the container with the same user and group IDs as the host user, preventing permission issues on mounted volumes.

# Note: The use of --ipc=host allows sharing the host's IPC namespace, which can be important for certain applications that require shared memory.

# Note: To enter container as root (for debugging, installing packages, etc.) run command in a seperate terminal:
# docker exec -it --user root <container_name_or_id> bash