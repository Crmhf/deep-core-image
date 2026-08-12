#!/bin/bash
# Deep Core Image Generation Script (Linux/macOS)
# Usage: ./generate.sh "prompt" output.png [ratio] [provider]

if [ -z "$1" ]; then
    echo "Usage: ./generate.sh \"prompt\" output.png [ratio] [provider]"
    echo ""
    echo "Examples:"
    echo "  ./generate.sh \"A sunset\" sunset.png"
    echo "  ./generate.sh \"A landscape\" landscape.png 16:9"
    echo "  ./generate.sh \"A cat\" cat.png 1:1 qwen-image"
    exit 1
fi

if [ -z "$2" ]; then
    echo "Error: Output file is required"
    echo "Usage: ./generate.sh \"prompt\" output.png [ratio] [provider]"
    exit 1
fi

PROMPT="$1"
OUTPUT="$2"
RATIO="$3"
PROVIDER="$4"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -z "$RATIO" ]; then
    if [ -z "$PROVIDER" ]; then
        python3 "$SCRIPT_DIR/generate_image.py" --prompt "$PROMPT" --output "$OUTPUT"
    else
        python3 "$SCRIPT_DIR/generate_image.py" --prompt "$PROMPT" --output "$OUTPUT" --provider "$PROVIDER"
    fi
else
    if [ -z "$PROVIDER" ]; then
        python3 "$SCRIPT_DIR/generate_image.py" --prompt "$PROMPT" --output "$OUTPUT" --ratio "$RATIO"
    else
        python3 "$SCRIPT_DIR/generate_image.py" --prompt "$PROMPT" --output "$OUTPUT" --ratio "$RATIO" --provider "$PROVIDER"
    fi
fi
