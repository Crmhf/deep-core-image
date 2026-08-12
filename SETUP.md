# Deep Core Image 技能配置指南

## 概述

此技能使用多个 AI 图像生成提供商，支持自动回退机制。当主提供商失败时，会自动尝试下一个提供商，确保图像生成的可靠性。

## 提供商配置

### 提供商列表（按回退顺序）

1. **GPT-Image-2** - OpenAI 兼容代理
2. **Qwen-Image** - OpenAI 兼容代理
3. **MiniMax Image-01** - MiniMax API

### 配置文件

配置文件位于技能目录下的 `config.json`：

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

### 环境变量（可选）

可以使用环境变量覆盖配置：

```bash
# 覆盖所有提供商的 API Key
export DEEP_CORE_IMAGE_API_KEY="your-api-key"

# 覆盖所有提供商的 Base URL
export DEEP_CORE_IMAGE_BASE_URL="http://your-proxy/v1"

# 设置默认提供商
export DEEP_CORE_IMAGE_DEFAULT_PROVIDER="qwen-image"
```

## 安装依赖

```bash
pip install -r scripts/requirements.txt
```

## 使用方法

### 基本文生图

```bash
python scripts/generate_image.py \
  --prompt "创建一张关于人工智能技术的专业信息图" \
  --output "ai-infographic.png"
```

### 使用特定宽高比

```bash
# 16:9 宽屏
python scripts/generate_image.py \
  --prompt "美丽的风景" \
  --ratio 16:9 \
  --output landscape.png

# 9:16 竖屏
python scripts/generate_image.py \
  --prompt "手机壁纸" \
  --ratio 9:16 \
  --output mobile_wallpaper.png
```

### 自定义尺寸

```bash
python scripts/generate_image.py \
  --prompt "产品照片" \
  --size 2048x2048 \
  --output product.png
```

### 指定提供商

```bash
python scripts/generate_image.py \
  --prompt "一只可爱的猫" \
  --provider qwen-image \
  --output cat.png
```

### 图生图

```bash
python scripts/generate_image.py \
  --prompt "转换为水彩画风格" \
  --input photo.jpg \
  --output watercolor.png
```

### 生成多张图片

```bash
python scripts/generate_image.py \
  --prompt "Logo 设计方案" \
  --n 3 \
  --output logo_{n}.png
```

## 支持的宽高比

| 比例 | 尺寸 | 用途 |
|------|------|------|
| 1:1 | 1024x1024 | 正方形，社交媒体头像 |
| 16:9 | 1792x1024 | 宽屏，横幅、风景 |
| 9:16 | 1024x1792 | 竖屏，手机壁纸、海报 |
| 4:3 | 1536x1152 | 标准比例 |
| 3:4 | 1152x1536 | 竖版标准 |
| 3:2 | 1536x1024 | 照片比例 |
| 2:3 | 1024x1536 | 竖版照片 |

## 支持的参数

| 参数 | 说明 | 可选值 | 默认值 |
|------|------|--------|--------|
| `--prompt`, `-p` | 图片描述 | - | 必填 |
| `--output`, `-o` | 输出文件路径 | - | 必填 |
| `--input`, `-i` | 输入图片（图生图） | - | 无 |
| `--size`, `-s` | 图片尺寸 | 1024x1024, 2048x2048 等 | 1024x1024 |
| `--ratio`, `-r` | 宽高比 | 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3 | 无 |
| `--quality`, `-q` | 图片质量 | standard, hd | hd |
| `--style` | 图片风格 | vivid, natural | vivid |
| `--n`, `--num` | 生成数量 | 1-10 | 1 |
| `--provider` | 指定提供商 | gpt-image, qwen-image, minimax-image | 自动回退 |
| `--response-format` | 返回格式 | url, b64_json | url |
| `--no-proxy` | 绕过代理 | - | false |
| `--verbose`, `-v` | 详细输出 | - | false |

## 回退机制

当主提供商失败时，系统会自动尝试下一个提供商：

1. **GPT-Image-2** → 失败后尝试 → **Qwen-Image**
2. **Qwen-Image** → 失败后尝试 → **MiniMax Image-01**
3. **MiniMax Image-01** → 失败后报错

每个提供商最多重试 3 次（可配置），使用指数退避策略。

## 最佳实践

1. **详细的提示词**: 提供具体、详细的图片描述可获得更好的结果
2. **选择合适的比例**: 根据用途选择合适的宽高比
3. **质量与速度权衡**: 使用 "standard" 快速预览，"hd" 用于最终输出
4. **风格选择**: "vivid" 适合鲜艳色彩，"natural" 适合写实风格
5. **指定提供商**: 如果你知道某个提供商对特定类型图片效果更好，可以强制指定

## 故障排除

### 所有提供商都失败

- 检查 API 密钥是否正确
- 确认网络连接正常
- 检查 API 服务是否可用
- 查看详细错误信息（使用 `--verbose`）

### 特定提供商失败

- 检查该提供商的配置是否正确
- 确认该提供商的服务状态
- 可以跳过该提供商，使用其他提供商

### 图片质量不理想

- 尝试使用不同的提供商
- 优化提示词，添加更多细节
- 尝试不同的风格设置

## API 端点类型

### OpenAI 兼容 (openai_compatible)

使用标准的 `/v1/images/generations` 端点，支持：
- 文生图
- 图生图
- 质量和风格参数

### MiniMax (minimax)

使用 MiniMax 的 `/v1/image_generation` 端点，支持：
- 文生图
- 自定义尺寸

## 集成其他技能

此技能可与其他技能配合使用：
- **docx skill**: 为 Word 文档生成图片
- **canvas-design**: 替代 PIL 的图片创建方式
- **pdf skill**: 为 PDF 报告创建视觉元素
- **image-enhancer**: 增强和改进生成的图片
