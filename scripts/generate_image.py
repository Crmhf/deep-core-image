#!/usr/bin/env python3
"""
Deep Core Image Generation Script (Multi-Provider Fallback)

Generate images using multiple AI image generation providers with automatic fallback.

Supported Providers (in fallback order):
1. GPT-Image-2 (OpenAI-compatible proxy)
2. Qwen-Image (OpenAI-compatible proxy)
3. MiniMax Image-01 (MiniMax API)

Supported Features:
- Text to Image (文生图)
- Image to Image (图生图)
- Multiple Images Generation (多图生图)
- Custom aspect ratios and sizes
- Automatic provider fallback on failure

Usage:
    # Text to Image with default provider
    python generate_image.py --prompt "A sunset" --output sunset.png

    # With specific aspect ratio
    python generate_image.py --prompt "A landscape" --ratio 16:9 --output landscape.png

    # With custom size
    python generate_image.py --prompt "A portrait" --size 1024x1792 --output portrait.png

    # Force specific provider
    python generate_image.py --prompt "A cat" --provider qwen-image --output cat.png

    # Image to Image
    python generate_image.py --prompt "Make it anime" --input photo.jpg --output anime.png

Configuration Priority (highest to lowest):
    1. Command line arguments
    2. Environment variables
    3. config.json file in skill directory
"""

import argparse
import base64
import os
import sys
import json
import time
from pathlib import Path
from typing import Optional, Dict, List, Any

try:
    import requests
except ImportError:
    print("Error: requests library not found. Install with: pip install requests")
    sys.exit(1)


def get_skill_dir():
    """Get the skill directory path."""
    script_dir = Path(__file__).parent
    return script_dir.parent


def load_config_file():
    """Load configuration from config.json file."""
    config_path = get_skill_dir() / "config.json"
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load config.json: {e}")
    return {}


def get_config():
    """
    Get configuration with priority: env vars > config file > defaults.

    Returns merged configuration from all sources.
    """
    # Load from config file
    file_config = load_config_file()

    # Defaults
    defaults = {
        "default_provider": "gpt-image",
        "providers": {},
        "fallback_order": ["gpt-image", "qwen-image", "qwen-image-flash", "minimax-image"],
        "default_size": "1024x1024",
        "default_quality": "high",
        "default_response_format": "b64_json",
        "supported_sizes": ["1024x1024", "1536x1024", "1024x1536", "1536x864", "864x1536", "1536x1152", "1152x1536", "2048x2048", "4096x4096"],
        "supported_ratios": {
            "1:1": "1024x1024",
            "16:9": "1536x864",
            "9:16": "864x1536",
            "4:3": "1536x1152",
            "3:4": "1152x1536",
            "3:2": "1536x1024",
            "2:3": "1024x1536"
        },
        "timeout": 180,
        "max_retries": 3
    }

    # Merge: defaults <- file_config
    config = {**defaults, **file_config}

    # Environment variables can override specific provider configs
    # Example: DEEP_CORE_IMAGE_API_KEY, DEEP_CORE_IMAGE_BASE_URL, etc.
    if os.environ.get("DEEP_CORE_IMAGE_API_KEY"):
        # Apply to all providers if env var is set
        for provider_name in config["providers"]:
            config["providers"][provider_name]["api_key"] = os.environ["DEEP_CORE_IMAGE_API_KEY"]
    if os.environ.get("DEEP_CORE_IMAGE_BASE_URL"):
        for provider_name in config["providers"]:
            config["providers"][provider_name]["base_url"] = os.environ["DEEP_CORE_IMAGE_BASE_URL"]
    if os.environ.get("DEEP_CORE_IMAGE_DEFAULT_PROVIDER"):
        config["default_provider"] = os.environ["DEEP_CORE_IMAGE_DEFAULT_PROVIDER"]

    return config


def resolve_size(ratio: Optional[str] = None, size: Optional[str] = None, config: Dict = None) -> str:
    """
    Resolve image size from ratio or size parameter.

    Args:
        ratio: Aspect ratio (e.g., "16:9", "1:1", "9:16")
        size: Direct size specification (e.g., "1024x1024")
        config: Configuration dict with supported_ratios

    Returns:
        Resolved size string (e.g., "1024x1024")
    """
    if size:
        return size

    if ratio and config:
        supported_ratios = config.get("supported_ratios", {})
        if ratio in supported_ratios:
            return supported_ratios[ratio]
        else:
            print(f"Warning: Unsupported ratio '{ratio}'. Supported: {list(supported_ratios.keys())}")
            print(f"Using default size: {config.get('default_size', '1024x1024')}")
            return config.get("default_size", "1024x1024")

    return config.get("default_size", "1024x1024") if config else "1024x1024"


def encode_image_to_base64(image_path: str) -> str:
    """
    Encode image file to base64 string.

    Args:
        image_path: Path to image file

    Returns:
        Base64 encoded string with data URL prefix
    """
    with open(image_path, "rb") as f:
        image_data = f.read()
    base64_string = base64.b64encode(image_data).decode("utf-8")
    # Determine MIME type
    ext = Path(image_path).suffix.lower()
    mime_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }
    mime_type = mime_types.get(ext, "image/png")
    return f"data:{mime_type};base64,{base64_string}"


def generate_openai_compatible(
    provider_config: Dict,
    prompt: str,
    size: str = "1024x1024",
    quality: str = "high",
    n: int = 1,
    response_format: str = "b64_json",
    input_image: Optional[str] = None,
    no_proxy: bool = False,
    timeout: int = 180
) -> List[Dict]:
    """
    Generate image using OpenAI-compatible API endpoint (e.g. KMAGE).

    Args:
        provider_config: Provider configuration dict
        prompt: Image description
        size: Image dimensions
        quality: Image quality (auto/low/medium/high, also compatible with standard/hd)
        n: Number of images
        response_format: "url" or "b64_json" (KMAGE defaults to b64_json)
        input_image: Path to input image for image-to-image
        no_proxy: Bypass system proxy
        timeout: Request timeout in seconds

    Returns:
        List of image data dicts
    """
    endpoint = f"{provider_config['base_url']}/images/generations"

    headers = {
        "Authorization": f"Bearer {provider_config['api_key']}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": provider_config["model"],
        "prompt": prompt,
        "size": size,
        "n": n,
    }

    if quality:
        payload["quality"] = quality
    if response_format:
        payload["response_format"] = response_format

    # Add input image(s) for image-to-image using reference_images
    if input_image:
        payload["reference_images"] = [encode_image_to_base64(input_image)]

    proxies = None
    if no_proxy:
        proxies = {"http": None, "https": None}

    response = requests.post(
        endpoint,
        headers=headers,
        json=payload,
        timeout=timeout,
        proxies=proxies
    )
    response.raise_for_status()

    result = response.json()
    if "data" not in result:
        raise ValueError(f"Unexpected API response format: {json.dumps(result, indent=2)}")

    return result["data"]


def size_to_minimax_aspect_ratio(size: str) -> str:
    """
    Map common pixel size to MiniMax aspect_ratio value.
    MiniMax aspect ratios:
      1:1  -> 1024x1024
      16:9 -> 1280x720
      4:3  -> 1152x864
      3:2  -> 1248x832
      2:3  -> 832x1248
      3:4  -> 864x1152
      9:16 -> 720x1280
    """
    mapping = {
        "1024x1024": "1:1",
        "1536x864": "16:9",
        "1280x720": "16:9",
        "1792x1024": "16:9",
        "864x1536": "9:16",
        "720x1280": "9:16",
        "1024x1792": "9:16",
        "1536x1152": "4:3",
        "1152x1536": "3:4",
        "1536x1024": "3:2",
        "1024x1536": "2:3",
    }
    return mapping.get(size, "1:1")


def generate_minimax(
    provider_config: Dict,
    prompt: str,
    size: str = "1024x1024",
    quality: str = "high",
    n: int = 1,
    response_format: str = "url",
    input_image: Optional[str] = None,
    no_proxy: bool = False,
    timeout: int = 180
) -> List[Dict]:
    """
    Generate image using MiniMax API endpoint.

    Args:
        provider_config: Provider configuration dict
        prompt: Image description
        size: Image dimensions (e.g., "1024x1024")
        quality: Image quality (not used by MiniMax, kept for interface consistency)
        n: Number of images
        response_format: "url" or "base64" (MiniMax uses "base64", not "b64_json")
        input_image: Path to input image for image-to-image (subject_reference)
        no_proxy: Bypass system proxy
        timeout: Request timeout in seconds

    Returns:
        List of image data dicts with 'url' or 'b64_json' key
    """
    endpoint = f"{provider_config['base_url']}/image_generation"

    headers = {
        "Authorization": f"Bearer {provider_config['api_key']}",
        "Content-Type": "application/json",
    }

    aspect_ratio = size_to_minimax_aspect_ratio(size)

    payload = {
        "model": provider_config["model"],
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "n": n,
    }

    # MiniMax response_format uses "base64", not "b64_json"
    minimax_response_format = "base64" if response_format == "b64_json" else response_format
    if minimax_response_format:
        payload["response_format"] = minimax_response_format

    # Image-to-image via subject_reference (only character supported currently)
    if input_image:
        payload["subject_reference"] = [
            {
                "type": "character",
                "image_file": encode_image_to_base64(input_image)
            }
        ]

    proxies = None
    if no_proxy:
        proxies = {"http": None, "https": None}

    response = requests.post(
        endpoint,
        headers=headers,
        json=payload,
        timeout=timeout,
        proxies=proxies
    )
    response.raise_for_status()

    result = response.json()

    # MiniMax response format:
    # url format  -> data.image_urls
    # base64 format -> data.image_base64
    images = []
    if "data" in result:
        if "image_urls" in result["data"]:
            for url in result["data"]["image_urls"]:
                images.append({"url": url})
        elif "image_base64" in result["data"]:
            for b64 in result["data"]["image_base64"]:
                images.append({"b64_json": b64})
        elif "images" in result["data"]:
            for img in result["data"]["images"]:
                if "url" in img:
                    images.append({"url": img["url"]})
                elif "b64_json" in img:
                    images.append({"b64_json": img["b64_json"]})
    elif "images" in result:
        for img in result["images"]:
            if "url" in img:
                images.append({"url": img["url"]})
            elif "b64_json" in img:
                images.append({"b64_json": img["b64_json"]})
    else:
        raise ValueError(f"Unexpected MiniMax response format: {json.dumps(result, indent=2)}")

    return images


def generate_image_with_fallback(
    config: Dict,
    prompt: str,
    size: str = "1024x1024",
    quality: str = "high",
    n: int = 1,
    response_format: str = "b64_json",
    input_image: Optional[str] = None,
    no_proxy: bool = False,
    preferred_provider: Optional[str] = None
) -> tuple:
    """
    Generate image with automatic provider fallback.

    Args:
        config: Full configuration dict
        prompt: Image description
        size: Image dimensions
        quality: Image quality
        n: Number of images
        response_format: "url" or "b64_json"
        input_image: Path to input image
        no_proxy: Bypass system proxy
        preferred_provider: Force specific provider

    Returns:
        Tuple of (provider_name, image_data_list)
    """
    providers = config.get("providers", {})
    fallback_order = config.get("fallback_order", list(providers.keys()))
    timeout = config.get("timeout", 180)
    max_retries = config.get("max_retries", 3)

    # Determine provider order
    if preferred_provider and preferred_provider in providers:
        provider_order = [preferred_provider] + [p for p in fallback_order if p != preferred_provider]
    else:
        provider_order = fallback_order

    last_error = None

    for provider_name in provider_order:
        if provider_name not in providers:
            print(f"Warning: Provider '{provider_name}' not configured, skipping...")
            continue

        provider_config = providers[provider_name]
        endpoint_type = provider_config.get("endpoint_type", "openai_compatible")

        print(f"\n{'='*60}")
        print(f"Trying provider: {provider_name} ({provider_config['model']})")
        print(f"Endpoint type: {endpoint_type}")
        print(f"{'='*60}")

        for attempt in range(max_retries):
            try:
                if endpoint_type == "openai_compatible":
                    images = generate_openai_compatible(
                        provider_config=provider_config,
                        prompt=prompt,
                        size=size,
                        quality=quality,
                        n=n,
                        response_format=response_format,
                        input_image=input_image,
                        no_proxy=no_proxy,
                        timeout=timeout
                    )
                elif endpoint_type == "minimax":
                    images = generate_minimax(
                        provider_config=provider_config,
                        prompt=prompt,
                        size=size,
                        quality=quality,
                        n=n,
                        response_format=response_format,
                        input_image=input_image,
                        no_proxy=no_proxy,
                        timeout=timeout
                    )
                else:
                    raise ValueError(f"Unknown endpoint type: {endpoint_type}")

                print(f"✓ Successfully generated image(s) with {provider_name}")
                return provider_name, images

            except requests.exceptions.Timeout:
                last_error = f"Provider {provider_name}: Request timed out"
                print(f"✗ Attempt {attempt + 1}/{max_retries}: Request timed out")
            except requests.exceptions.ConnectionError as e:
                last_error = f"Provider {provider_name}: Connection error - {e}"
                print(f"✗ Attempt {attempt + 1}/{max_retries}: Connection error")
            except requests.exceptions.HTTPError as e:
                last_error = f"Provider {provider_name}: HTTP error - {e}"
                try:
                    error_detail = e.response.json()
                    print(f"✗ Attempt {attempt + 1}/{max_retries}: HTTP {e.response.status_code}")
                    print(f"  Error: {json.dumps(error_detail, indent=2)}")
                except:
                    print(f"✗ Attempt {attempt + 1}/{max_retries}: HTTP {e.response.status_code}")
            except Exception as e:
                last_error = f"Provider {provider_name}: {str(e)}"
                print(f"✗ Attempt {attempt + 1}/{max_retries}: {str(e)}")

            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"  Waiting {wait_time}s before retry...")
                time.sleep(wait_time)

        print(f"✗ Provider {provider_name} failed after {max_retries} attempts")

    raise RuntimeError(f"All providers failed. Last error: {last_error}")


def save_image(image_data: Dict, output_path: str) -> None:
    """
    Save image data to file.

    Args:
        image_data: Dict containing 'b64_json' or 'url'
        output_path: Path to save the image
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if "b64_json" in image_data:
        # Base64 encoded image
        print("Decoding base64 image data...")
        image_bytes = base64.b64decode(image_data["b64_json"])
        with open(output_path, "wb") as f:
            f.write(image_bytes)
        print(f"Image saved to: {output_path}")
    elif "url" in image_data:
        # URL to download
        print(f"Downloading image from URL...")
        try:
            response = requests.get(
                image_data["url"],
                timeout=120,
                proxies={"http": None, "https": None}
            )
            response.raise_for_status()
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"Image saved to: {output_path}")
        except Exception as e:
            print(f"Error downloading image: {e}")
            raise
    else:
        raise ValueError(f"No image data found in response. Available keys: {image_data.keys()}")


def main():
    # Pre-load config for default values
    preconfig = get_config()

    parser = argparse.ArgumentParser(
        description="Generate images using Deep Core Image (multi-provider fallback)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Text to Image with default settings
    python generate_image.py --prompt "A sunset over mountains" --output sunset.png

  # With 16:9 aspect ratio
    python generate_image.py \\
      --prompt "A beautiful landscape" \\
      --ratio 16:9 \\
      --output landscape.png

  # With custom size
    python generate_image.py \\
      --prompt "A portrait" \\
      --size 1024x1792 \\
      --output portrait.png

  # Force specific provider
    python generate_image.py \\
      --prompt "A cat" \\
      --provider qwen-image \\
      --output cat.png

  # Image to Image
    python generate_image.py \\
      --prompt "Make it look like a watercolor painting" \\
      --input photo.jpg \\
      --output watercolor.png

  # Multiple images
    python generate_image.py \\
      --prompt "Logo design concepts" \\
      --n 3 \\
      --output logo_{n}.png

Supported Aspect Ratios:
  1:1   - Square (1024x1024)
  16:9  - Widescreen (1536x864)
  9:16  - Vertical (864x1536)
  4:3   - Standard (1536x1152)
  3:4   - Portrait (1152x1536)
  3:2   - Photo (1536x1024)
  2:3   - Portrait photo (1024x1536)

Providers (fallback order):
  1. gpt-image (GPT-Image-2)
  2. qwen-image (Qwen-Image)
  3. qwen-image-flash (Qwen-Image-Flash)
  4. minimax-image (MiniMax Image-01)
        """
    )

    # Required arguments
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Image description prompt"
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Output file path (e.g., output.png). Use {n} for multiple images."
    )

    # Image input for image-to-image
    parser.add_argument(
        "--input", "-i",
        help="Input image path for image-to-image generation"
    )

    # Size and ratio options
    parser.add_argument(
        "--size", "-s",
        default=None,
        help=f"Image dimensions (e.g., 1024x1024, 2048x1152). Default: {preconfig.get('default_size', '1024x1024')}"
    )
    parser.add_argument(
        "--ratio", "-r",
        default=None,
        help="Aspect ratio (e.g., 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3)"
    )

    # Quality option (KMAGE/MiniMax compatible)
    parser.add_argument(
        "--quality", "-q",
        default=preconfig.get("default_quality", "high"),
        choices=["auto", "low", "medium", "high", "standard", "hd"],
        help=f"Image quality (default: {preconfig.get('default_quality', 'high')})"
    )

    # Style option (kept for backward compatibility; not sent to KMAGE)
    parser.add_argument(
        "--style",
        default=None,
        choices=["vivid", "natural"],
        help="Image style (optional, provider-dependent; default: none)"
    )

    # Number of images
    parser.add_argument(
        "--n", "--num",
        type=int,
        default=1,
        help="Number of images to generate (default: 1)"
    )

    # Response format
    parser.add_argument(
        "--response-format",
        default=preconfig.get("default_response_format", "b64_json"),
        choices=["url", "b64_json"],
        help="Response format (default: b64_json)"
    )

    # Provider selection
    parser.add_argument(
        "--provider",
        default=None,
        choices=list(preconfig.get("providers", {}).keys()),
        help="Force specific provider (default: auto fallback)"
    )

    # Additional options
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--no-proxy",
        action="store_true",
        help="Bypass system proxy settings"
    )

    args = parser.parse_args()

    # Get configuration
    config = get_config()

    # Resolve size
    size = resolve_size(ratio=args.ratio, size=args.size, config=config)

    if args.verbose:
        print(f"Configuration:")
        print(f"  Default provider: {config['default_provider']}")
        print(f"  Fallback order: {config['fallback_order']}")
        print(f"  Size: {size}")
        print(f"  Quality: {args.quality}")
        print(f"  Response format: {args.response_format}")
        print()

    # Validate input image if provided
    if args.input:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: Input image not found: {args.input}")
            sys.exit(1)

    # Generate image with fallback
    try:
        provider_name, images = generate_image_with_fallback(
            config=config,
            prompt=args.prompt,
            size=size,
            quality=args.quality,
            n=args.n,
            response_format=args.response_format,
            input_image=args.input,
            no_proxy=args.no_proxy,
            preferred_provider=args.provider
        )

        # Save images
        if images:
            for i, img_data in enumerate(images):
                if args.n > 1:
                    # Support {n} placeholder in output filename
                    output_path = args.output.replace("{n}", str(i + 1))
                else:
                    output_path = args.output
                save_image(img_data, output_path)

            print(f"\n{'='*60}")
            print(f"✓ Success! Generated {len(images)} image(s) using {provider_name}")
            print(f"{'='*60}")
        else:
            print("Error: No images returned from API")
            sys.exit(1)

    except RuntimeError as e:
        print(f"\n{'='*60}")
        print(f"✗ Failed: {e}")
        print(f"{'='*60}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"✗ Unexpected error: {e}")
        print(f"{'='*60}")
        sys.exit(1)


if __name__ == "__main__":
    main()
