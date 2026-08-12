---
name: deep-core-image
description: Generate high-quality images using multiple AI providers with automatic fallback. Supports GPT-Image-2, Qwen-Image, and MiniMax Image-01. Use when the user requests image generation, creating infographics, posters, visual content, illustrations, or needs reliable image generation with fallback support.
---

# Deep Core Image Generation Skill

Generate high-quality images using multiple AI image generation providers with automatic fallback support.

## Overview

This skill enables Claude to generate images using multiple AI providers with automatic fallback. When the primary provider fails, the system automatically tries the next provider in the fallback chain, ensuring reliable image generation.

## Supported Providers

1. **GPT-Image-2** - OpenAI-compatible proxy (primary)
2. **Qwen-Image** - OpenAI-compatible proxy (secondary)
3. **MiniMax Image-01** - MiniMax API (tertiary)

## Features

- **Multi-Provider Fallback** - Automatic fallback when primary provider fails
- **Text to Image** (文生图) - Generate images from text descriptions
- **Image to Image** (图生图) - Transform images with text prompts
- **Multiple Images** (多图生图) - Generate multiple images in one request
- **Custom Aspect Ratios** - Support for 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3
- **Flexible Sizes** - From 1024x1024 to 4096x4096
- **Provider Selection** - Force specific provider when needed

## Triggers

Use this skill when:
- User requests image generation with reliable quality
- Creating infographics, posters, or visual content
- Generating illustrations for documents or presentations
- User needs images with specific aspect ratios
- When fallback support is important for reliability
- Converting/transforming existing images with AI

## Configuration

### Config File

Configure via `config.json` in the skill directory:

```json
{
    "default_provider": "gpt-image",
    "providers": {
        "gpt-image": {
            "api_key": "your-api-key",
            "base_url": "http://your-proxy/v1",
            "model": "gpt-image-2",
            "endpoint_type": "openai_compatible"
        },
        "qwen-image": {
            "api_key": "your-api-key",
            "base_url": "http://your-proxy/v1",
            "model": "Qwen/Qwen-Image",
            "endpoint_type": "openai_compatible"
        },
        "minimax-image": {
            "api_key": "your-minimax-api-key",
            "base_url": "https://api.minimaxi.com/v1",
            "model": "image-01",
            "endpoint_type": "minimax"
        }
    },
    "fallback_order": ["gpt-image", "qwen-image", "minimax-image"],
    "default_size": "1024x1024",
    "default_quality": "hd",
    "default_style": "vivid",
    "timeout": 180,
    "max_retries": 3
}
```

### Environment Variables

```bash
# Override all providers' API Key
export DEEP_CORE_IMAGE_API_KEY="your-api-key"

# Override all providers' Base URL
export DEEP_CORE_IMAGE_BASE_URL="http://your-proxy/v1"

# Set default provider
export DEEP_CORE_IMAGE_DEFAULT_PROVIDER="qwen-image"
```

## Usage

### Text to Image (文生图)

Basic image generation:

```bash
python generate_image.py --prompt "A sunset over mountains" --output sunset.png
```

With specific aspect ratio:

```bash
python generate_image.py \
  --prompt "A beautiful landscape" \
  --ratio 16:9 \
  --output landscape.png
```

With custom size:

```bash
python generate_image.py \
  --prompt "Professional product photography" \
  --size 2048x2048 \
  --output product.png
```

### Image to Image (图生图)

Transform an existing image:

```bash
python generate_image.py \
  --prompt "Make it look like a watercolor painting" \
  --input photo.jpg \
  --output watercolor.png
```

### Multiple Images (多图生图)

Generate multiple variations:

```bash
python generate_image.py \
  --prompt "Logo design concepts" \
  --n 3 \
  --output logo_{n}.png
```

### Force Specific Provider

```bash
python generate_image.py \
  --prompt "A cute cat" \
  --provider qwen-image \
  --output cat.png
```

## Parameters

| Parameter | Description | Default | Choices |
|-----------|-------------|---------|---------|
| `--prompt`, `-p` | Image description | required | - |
| `--output`, `-o` | Output file path | required | - |
| `--input`, `-i` | Input image for image-to-image | null | - |
| `--size`, `-s` | Image dimensions | 1024x1024 | 1024x1024, 2048x2048, etc. |
| `--ratio`, `-r` | Aspect ratio | null | 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3 |
| `--quality`, `-q` | Image quality | hd | standard, hd |
| `--style` | Image style | vivid | vivid, natural |
| `--n`, `--num` | Number of images | 1 | 1-10 |
| `--provider` | Force specific provider | auto | gpt-image, qwen-image, minimax-image |
| `--response-format` | Return format | url | url, b64_json |
| `--no-proxy` | Bypass system proxy | false | - |
| `--verbose`, `-v` | Verbose output | false | - |

## Supported Aspect Ratios

| Ratio | Size | Use Case |
|-------|------|----------|
| 1:1 | 1024x1024 | Square, social media avatars |
| 16:9 | 1792x1024 | Widescreen, banners, landscapes |
| 9:16 | 1024x1792 | Vertical, mobile wallpapers, posters |
| 4:3 | 1536x1152 | Standard ratio |
| 3:4 | 1152x1536 | Portrait standard |
| 3:2 | 1536x1024 | Photo ratio |
| 2:3 | 1024x1536 | Portrait photo |

## Fallback Mechanism

The system automatically tries providers in order:

1. **GPT-Image-2** → If fails → **Qwen-Image**
2. **Qwen-Image** → If fails → **MiniMax Image-01**
3. **MiniMax Image-01** → If fails → Error

Each provider is retried up to 3 times with exponential backoff.

## Examples

### Create an Infographic

```bash
python generate_image.py \
  --prompt "Create a professional infographic about AI technology trends with modern blue color scheme" \
  --output infographic.png \
  --ratio 4:3 \
  --quality hd
```

### Mobile Wallpaper

```bash
python generate_image.py \
  --prompt "Beautiful galaxy wallpaper for smartphone" \
  --ratio 9:16 \
  --output mobile_wallpaper.png
```

### Transform Photo Style

```bash
python generate_image.py \
  --prompt "Convert to anime style with vibrant colors" \
  --input portrait.jpg \
  --output anime_portrait.png \
  --ratio 1:1
```

### Generate Multiple Options

```bash
python generate_image.py \
  --prompt "Logo design concepts for a tech startup" \
  --n 5 \
  --output logo_concept_{n}.png \
  --ratio 1:1
```

### Force Specific Provider

```bash
python generate_image.py \
  --prompt "A beautiful sunset" \
  --provider minimax-image \
  --output sunset.png \
  --ratio 16:9
```

## Best Practices

1. **Detailed Prompts**: Provide specific, detailed descriptions for better results
2. **Aspect Ratio Selection**: Choose the right ratio for your use case
3. **Provider Selection**: Use `--provider` if you know which works best for your content
4. **Quality Setting**: Use "hd" for final outputs, "standard" for drafts
5. **Style Choice**: "vivid" for vibrant colors, "natural" for realistic rendering

## API Integration

### OpenAI-Compatible Providers

Uses `/v1/images/generations` endpoint:

```json
{
  "model": "gpt-image-2",
  "prompt": "A beautiful landscape",
  "size": "1792x1024",
  "quality": "hd",
  "style": "vivid",
  "n": 1,
  "response_format": "url"
}
```

### MiniMax Provider

Uses `/v1/image_generation` endpoint:

```json
{
  "model": "image-01",
  "prompt": "A beautiful landscape",
  "width": 1792,
  "height": 1024,
  "num_images": 1
}
```

## Error Handling

The script handles:
- Missing API credentials
- Network connectivity issues
- Invalid parameters
- API rate limits
- File not found (for input images)
- Provider failures with automatic fallback

## Integration with Other Skills

This skill works well with:
- **docx skill**: Generate images for Word documents
- **canvas-design**: Alternative to PIL-based image creation
- **pdf skill**: Create visual elements for PDF reports
- **image-enhancer**: Enhance and improve generated images

## Limitations

- Requires active internet connection
- API rate limits may apply based on your provider
- Image content policies apply (no NSFW content)
- Maximum prompt length may be limited by the API
- Large images may take longer to generate
- MiniMax provider doesn't support image-to-image

## Troubleshooting

### All Providers Failed

- Check API keys are correct
- Verify network connection
- Check API service status
- Use `--verbose` for detailed error info

### Specific Provider Failed

- Check provider configuration
- Verify provider service status
- Skip to next provider automatically

### Image Quality Issues

- Try different providers
- Optimize prompt with more details
- Try different style settings
