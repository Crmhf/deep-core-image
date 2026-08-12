#!/bin/bash
# Example usage script for Deep Core Image skill

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================="
echo "Deep Core Image - Example Usage"
echo "=========================================="

# Example 1: Basic text-to-image
echo ""
echo "Example 1: Basic text-to-image"
echo "-------------------------------------------"
echo "Command:"
echo "  python3 $SCRIPT_DIR/generate_image.py \\"
echo "    --prompt \"A beautiful sunset over mountains\" \\"
echo "    --output sunset.png"
echo ""
echo "To run this example, uncomment the lines below:"
# python3 "$SCRIPT_DIR/generate_image.py" \
#   --prompt "A beautiful sunset over mountains" \
#   --output sunset.png

# Example 2: With aspect ratio
echo ""
echo "Example 2: With 16:9 aspect ratio"
echo "-------------------------------------------"
echo "Command:"
echo "  python3 $SCRIPT_DIR/generate_image.py \\"
echo "    --prompt \"A wide landscape photo\" \\"
echo "    --ratio 16:9 \\"
echo "    --output landscape.png"
echo ""
echo "To run this example, uncomment the lines below:"
# python3 "$SCRIPT_DIR/generate_image.py" \
#   --prompt "A wide landscape photo" \
#   --ratio 16:9 \
#   --output landscape.png

# Example 3: With specific provider
echo ""
echo "Example 3: With specific provider"
echo "-------------------------------------------"
echo "Command:"
echo "  python3 $SCRIPT_DIR/generate_image.py \\"
echo "    --prompt \"A cute cat\" \\"
echo "    --provider qwen-image \\"
echo "    --output cat.png"
echo ""
echo "To run this example, uncomment the lines below:"
# python3 "$SCRIPT_DIR/generate_image.py" \
#   --prompt "A cute cat" \
#   --provider qwen-image \
#   --output cat.png

# Example 4: Image-to-image
echo ""
echo "Example 4: Image-to-image transformation"
echo "-------------------------------------------"
echo "Command:"
echo "  python3 $SCRIPT_DIR/generate_image.py \\"
echo "    --prompt \"Convert to anime style\" \\"
echo "    --input photo.jpg \\"
echo "    --output anime.png"
echo ""
echo "To run this example, uncomment the lines below:"
# python3 "$SCRIPT_DIR/generate_image.py" \
#   --prompt "Convert to anime style" \
#   --input photo.jpg \
#   --output anime.png

# Example 5: Multiple images
echo ""
echo "Example 5: Generate multiple images"
echo "-------------------------------------------"
echo "Command:"
echo "  python3 $SCRIPT_DIR/generate_image.py \\"
echo "    --prompt \"Logo design concepts\" \\"
echo "    --n 3 \\"
echo "    --output logo_{n}.png"
echo ""
echo "To run this example, uncomment the lines below:"
# python3 "$SCRIPT_DIR/generate_image.py" \
#   --prompt "Logo design concepts" \
#   --n 3 \
#   --output logo_{n}.png

# Example 6: Custom size
echo ""
echo "Example 6: Custom size"
echo "-------------------------------------------"
echo "Command:"
echo "  python3 $SCRIPT_DIR/generate_image.py \\"
echo "    --prompt \"High resolution product photo\" \\"
echo "    --size 2048x2048 \\"
echo "    --output product.png"
echo ""
echo "To run this example, uncomment the lines below:"
# python3 "$SCRIPT_DIR/generate_image.py" \
#   --prompt "High resolution product photo" \
#   --size 2048x2048 \
#   --output product.png

echo ""
echo "=========================================="
echo "For more information, see:"
echo "  - README.md for quick start"
echo "  - SETUP.md for detailed setup"
echo "  - SKILL.md for full documentation"
echo "=========================================="
