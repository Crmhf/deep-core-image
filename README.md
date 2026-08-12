# Deep Core Image Generation Skill

A robust image generation skill with multi-provider fallback support.

## Features

- **Multi-Provider Fallback**: Automatic fallback when primary provider fails
- **Multiple Providers**: GPT-Image-2, Qwen-Image, MiniMax Image-01
- **Custom Aspect Ratios**: Support for 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3
- **Flexible Sizes**: From 1024x1024 to 4096x4096
- **Text to Image**: Generate images from text descriptions
- **Image to Image**: Transform existing images
- **Multiple Images**: Generate multiple variations in one request

## Quick Start

### 1. Install Dependencies

```bash
pip install -r scripts/requirements.txt
```

### 2. Configure API Keys

Edit `config.json` with your API keys:

```json
{
    "providers": {
        "gpt-image": {
            "api_key": "your-api-key",
            "base_url": "http://your-proxy/v1",
            "model": "gpt-image-2"
        }
    }
}
```

### 3. Generate Images

```bash
# Basic usage
python scripts/generate_image.py --prompt "A sunset" --output sunset.png

# With aspect ratio
python scripts/generate_image.py --prompt "A landscape" --ratio 16:9 --output landscape.png

# With specific provider
python scripts/generate_image.py --prompt "A cat" --provider qwen-image --output cat.png
```

## Documentation

- [SETUP.md](SETUP.md) - Detailed setup and configuration guide
- [SKILL.md](SKILL.md) - Skill documentation and usage examples

## Supported Providers

| Provider | Model | Endpoint Type | Features |
|----------|-------|---------------|----------|
| gpt-image | GPT-Image-2 | OpenAI Compatible | Text-to-image, Image-to-image, Quality/Style |
| qwen-image | Qwen-Image | OpenAI Compatible | Text-to-image, Image-to-image, Quality/Style |
| minimax-image | Image-01 | MiniMax API | Text-to-image, Custom sizes |

## Supported Aspect Ratios

| Ratio | Size | Use Case |
|-------|------|----------|
| 1:1 | 1024x1024 | Square, social media |
| 16:9 | 1792x1024 | Widescreen, banners |
| 9:16 | 1024x1792 | Vertical, mobile |
| 4:3 | 1536x1152 | Standard |
| 3:4 | 1152x1536 | Portrait |
| 3:2 | 1536x1024 | Photo |
| 2:3 | 1024x1536 | Portrait photo |

## Command Line Options

```
--prompt, -p      Image description (required)
--output, -o      Output file path (required)
--input, -i       Input image for image-to-image
--size, -s        Image dimensions (e.g., 1024x1024)
--ratio, -r       Aspect ratio (e.g., 16:9, 1:1)
--quality, -q     Image quality (standard, hd)
--style           Image style (vivid, natural)
--n, --num        Number of images (1-10)
--provider        Force specific provider
--response-format Return format (url, b64_json)
--no-proxy        Bypass system proxy
--verbose, -v     Verbose output
```

## License

This skill is provided as-is for use with Claude Code.
