---
name: deep-core-image
description: 使用多个 AI 提供商生成高质量图片，支持自动降级。适用于 Web 应用、网站、小程序、日常配图、小图标、验证草图等场景。支持 gpt-image、minimax-image、qwen-image、qwen-image-flash 四个模型，按场景复杂度选型，minimax 兜底。
---

# Deep Core Image Generation Skill

使用多个 AI 提供商生成高质量图片，支持自动降级，确保可靠的图片生成能力。

## 概述

本技能支持使用多个 AI 提供商生成图片，当主提供商失败时，系统自动尝试下一个提供商，确保图片生成的可靠性。

**核心原则：按场景复杂度选模型，minimax 兜底。**

## 支持的模型

| 模型 | 能力档位 | 擅长 | 单次成本 | 速度 | 主用场景 |
|------|---------|------|---------|------|---------|
| **gpt-image** | ⭐⭐⭐⭐⭐ S 级 | 复杂构图、多主体、精细文字、长 prompt 还原、影视级美感 | 高 | 慢 | 营销主图、复杂海报、品牌视觉 |
| **minimax-image** | ⭐⭐⭐⭐ A 级 | 通用场景、中文理解、性价比、风格覆盖广 | 中 | 中 | **日常主力、兜底模型** |
| **qwen-image** | ⭐⭐⭐ A-级 | 东方美学、国风水墨、中文古风、文字渲染 | 中 | 中 | 国风、中文海报、传统题材 |
| **qwen-image-flash** | ⭐⭐ B 级 | 简单图、图标、占位、验证草图 | 低 | 快 | 图标、占位、迭代验证 |

### 选型速查

```
复杂/品牌 → gpt-image
日常/通用/兜底 → minimax-image
国风/古风/中文书法 → qwen-image
图标/占位/快速验证 → qwen-image-flash
```

## 适用场景

使用本技能当：
- 用户需要生成图片，且要求可靠的质量
- 创建信息图、海报或视觉内容
- 为文档或演示生成插图
- 需要特定宽高比的图片
- 需要降级支持以确保可靠性
- 使用 AI 转换/变换现有图片

### 场景 → 模型对照

**Web 应用 / 网站**
- 首页 Hero 大图 → gpt-image
- Banner / 活动图 → minimax-image
- 博客配图 → minimax-image
- favicon / 图标 → qwen-image-flash

**小程序**
- 启动页 / 首屏 → gpt-image
- 分享卡片 → minimax-image
- 分类图标 → qwen-image-flash

**日常做图**
- 公众号头图 → gpt-image
- PPT 配图 → minimax-image
- 表情包 → minimax-image

**小图标 / 验证**
- App Icon → minimax-image
- 工具栏图标 → qwen-image-flash
- 验证草图 → qwen-image-flash

详细的场景选型请参考 [场景模型选型指南](references/scene-model-selection-guide.md)。

## 功能特性

- **多提供商降级** - 主提供商失败时自动降级
- **文生图** (Text to Image) - 从文字描述生成图片
- **图生图** (Image to Image) - 使用文字提示转换图片
- **多图生图** (Multiple Images) - 一次请求生成多张图片
- **自定义宽高比** - 支持 1:1、16:9、9:16、4:3、3:4、3:2、2:3
- **灵活尺寸** - 从 1024x1024 到 4096x4096
- **提供商选择** - 需要时可强制指定提供商

## 配置

### 配置文件

通过技能目录下的 `config.json` 配置：

```json
{
    "default_provider": "minimax-image",
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
        "qwen-image-flash": {
            "api_key": "your-api-key",
            "base_url": "http://your-proxy/v1",
            "model": "Qwen/Qwen-Image-Flash",
            "endpoint_type": "openai_compatible"
        },
        "minimax-image": {
            "api_key": "your-minimax-api-key",
            "base_url": "https://api.minimaxi.com/v1",
            "model": "image-01",
            "endpoint_type": "minimax"
        }
    },
    "fallback_order": ["minimax-image", "qwen-image-flash", "gpt-image", "qwen-image"],
    "default_size": "1024x1024",
    "default_quality": "hd",
    "default_style": "vivid",
    "timeout": 180,
    "max_retries": 3
}
```

### 环境变量

```bash
# 覆盖所有提供商的 API Key
export DEEP_CORE_IMAGE_API_KEY="your-api-key"

# 覆盖所有提供商的 Base URL
export DEEP_CORE_IMAGE_BASE_URL="http://your-proxy/v1"

# 设置默认提供商
export DEEP_CORE_IMAGE_DEFAULT_PROVIDER="minimax-image"
```

## 使用方法

### 文生图 (Text to Image)

基础图片生成：

```bash
python scripts/generate_image.py --prompt "夕阳下的山脉" --output sunset.png
```

指定宽高比：

```bash
python scripts/generate_image.py \
  --prompt "美丽的风景" \
  --ratio 16:9 \
  --output landscape.png
```

自定义尺寸：

```bash
python scripts/generate_image.py \
  --prompt "专业产品摄影" \
  --size 2048x2048 \
  --output product.png
```

### 图生图 (Image to Image)

转换现有图片：

```bash
python scripts/generate_image.py \
  --prompt "转换为水彩画风格" \
  --input photo.jpg \
  --output watercolor.png
```

### 多图生图 (Multiple Images)

生成多个变体：

```bash
python scripts/generate_image.py \
  --prompt "Logo 设计概念" \
  --n 3 \
  --output logo_{n}.png
```

### 强制指定提供商

```bash
python scripts/generate_image.py \
  --prompt "一只可爱的猫" \
  --provider qwen-image \
  --output cat.png
```

## 参数说明

| 参数 | 说明 | 默认值 | 可选值 |
|------|------|--------|--------|
| `--prompt`, `-p` | 图片描述 | 必填 | - |
| `--output`, `-o` | 输出文件路径 | 必填 | - |
| `--input`, `-i` | 用于图生图的输入图片 | null | - |
| `--size`, `-s` | 图片尺寸 | 1024x1024 | 1024x1024, 2048x2048 等 |
| `--ratio`, `-r` | 宽高比 | null | 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3 |
| `--quality`, `-q` | 图片质量 | hd | standard, hd |
| `--style` | 图片风格 | vivid | vivid, natural |
| `--n`, `--num` | 图片数量 | 1 | 1-10 |
| `--provider` | 强制指定提供商 | auto | gpt-image, qwen-image, minimax-image |
| `--response-format` | 返回格式 | url | url, b64_json |
| `--no-proxy` | 绕过系统代理 | false | - |
| `--verbose`, `-v` | 详细输出 | false | - |

## 支持的宽高比

| 比例 | 尺寸 | 适用场景 |
|------|------|---------|
| 1:1 | 1024x1024 | 方形，社交媒体头像 |
| 16:9 | 1792x1024 | 宽屏，横幅，风景 |
| 9:16 | 1024x1792 | 竖屏，手机壁纸，海报 |
| 4:3 | 1536x1152 | 标准比例 |
| 3:4 | 1152x1536 | 竖屏标准 |
| 3:2 | 1536x1024 | 摄影比例 |
| 2:3 | 1024x1536 | 竖屏摄影 |

## 降级机制

系统自动按顺序尝试提供商：

1. **minimax-image** → 如果失败 → **qwen-image-flash**
2. **qwen-image-flash** → 如果失败 → **gpt-image**
3. **gpt-image** → 如果失败 → **qwen-image**
4. **qwen-image** → 如果失败 → 错误

每个提供商最多重试 3 次，采用指数退避策略。

## Prompt 编写指南

### 黄金公式

```
[主体] + [动作/状态] + [环境/背景] + [风格] + [光线/色调] + [构图] + [画质关键词]
```

### 示例

**营销 Banner**：
```
[product/brand] hero banner,
modern minimal style, gradient background,
centered composition, eye-catching,
professional photography, studio lighting,
8k, ultra-detailed
```

**公众号头图**：
```
[topic] themed illustration,
editorial illustration style, warm colors,
balanced composition, soft lighting,
subtle textures, professional quality
```

**App Icon**：
```
single icon design of [subject],
flat design, rounded square,
solid background, minimal details,
modern app icon style, vector art,
centered, clean composition
```

**国风插画**：
```
[scene] in traditional Chinese painting style,
shuimo ink wash, xieyi brushwork,
muted earthy tones, silk texture,
Song Dynasty aesthetic, vertical scroll,
subtle red seal stamp
```

详细的 Prompt 编写指南请参考 [Prompt 编写指南](references/prompt-writing-guide.md)。

## 风格库

### 通用风格关键词

```
photorealistic, hyperrealistic, cinematic, professional photography
8k, ultra-detailed, sharp focus, studio lighting
soft light, golden hour, bokeh, depth of field
```

### 插画风格

```
flat illustration, isometric illustration, vector art
corporate memphis, geometric illustration
minimalist line art, line drawing, continuous line
watercolor illustration, gouache painting
```

### 国风/东方美学

```
Chinese ink painting, shuimo, sumi-e
traditional Chinese painting, gongbi style
Song Dynasty aesthetic, Tang Dynasty palace style
silk scroll painting, hanging scroll
```

### 商业/品牌风格

```
clean corporate style, professional brand aesthetic
Apple-style minimalism, Bauhaus design
Swiss design grid, modern editorial
luxury brand aesthetic, premium feel
```

### 科技/互联网

```
cyberpunk, futuristic UI, holographic
glassmorphism, neumorphism, 3D render
low poly 3D, isometric 3D
tech illustration, blue gradient, neural network aesthetic
```

### 复古/怀旧

```
vintage poster, retro illustration, 80s synthwave
film grain, analog photography, polaroid
art deco, art nouveau, victorian engraving
pixel art, 8-bit, 16-bit retro game
```

完整的风格库请参考 [风格指南](references/style-guide.md)。

## 图片创建流程

```
1. 明确需求 → 2. 选择模型 → 3. 编写 Prompt → 4. 生成图片 → 5. 评估质量 → 6. 迭代优化 → 7. 后期处理
```

详细的创建流程请参考 [图片创建完整流程](references/image-creation-workflow.md)。

## 最佳实践

### 核心原则

1. **按场景选模型**：复杂才用 gpt-image，日常全靠 minimax 兜底
2. **二八原则**：80% minimax-image，15% gpt-image，4% qwen-image，1% qwen-image-flash
3. **先验证后精修**：用 qwen-image-flash 快速验证，确认后再用目标模型
4. **Prompt 要写好**：具体 + 结构 + 统一 + 迭代

### 成本控制

- gpt-image 用在最关键处（5%）
- minimax-image 承担 80% 日常
- qwen-image-flash 用于验证和图标
- 设置每用户/每日上限

### 质量保证

- 使用评估打分表（4 分以上才通过）
- 多版本对比选出最优
- 迭代优化直到满意

完整最佳实践请参考 [最佳实践](references/best-practices.md)。

## 示例

### 创建信息图

```bash
python scripts/generate_image.py \
  --prompt "创建一个关于 AI 技术趋势的专业信息图，使用现代蓝色配色方案" \
  --output infographic.png \
  --ratio 4:3 \
  --quality hd
```

### 手机壁纸

```bash
python scripts/generate_image.py \
  --prompt "美丽的银河系智能手机壁纸" \
  --ratio 9:16 \
  --output mobile_wallpaper.png
```

### 转换照片风格

```bash
python scripts/generate_image.py \
  --prompt "转换为动漫风格，使用鲜艳的色彩" \
  --input portrait.jpg \
  --output anime_portrait.png \
  --ratio 1:1
```

### 生成多个选项

```bash
python scripts/generate_image.py \
  --prompt "科技创业公司的 Logo 设计概念" \
  --n 5 \
  --output logo_concept_{n}.png \
  --ratio 1:1
```

### 强制指定提供商

```bash
python scripts/generate_image.py \
  --prompt "美丽的日落" \
  --provider minimax-image \
  --output sunset.png \
  --ratio 16:9
```

## API 集成

### OpenAI 兼容提供商

使用 `/v1/images/generations` 端点：

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

### MiniMax 提供商

使用 `/v1/image_generation` 端点：

```json
{
  "model": "image-01",
  "prompt": "A beautiful landscape",
  "width": 1792,
  "height": 1024,
  "num_images": 1
}
```

## 错误处理

脚本会处理：
- 缺少 API 凭证
- 网络连接问题
- 无效参数
- API 速率限制
- 文件未找到（输入图片）
- 提供商失败自动降级

## 与其他技能的集成

本技能可与以下技能配合：
- **docx skill**：为 Word 文档生成图片
- **canvas-design**：基于 PIL 的图片创建替代方案
- **pdf skill**：为 PDF 报告创建视觉元素
- **image-enhancer**：增强和改进生成的图片

## 限制

- 需要活动的互联网连接
- API 速率限制可能基于您的提供商
- 图片内容策略适用（无 NSFW 内容）
- 最大提示长度可能受 API 限制
- 大图片可能需要更长时间生成
- MiniMax 提供商不支持图生图

## 故障排除

### 所有提供商失败

- 检查 API 密钥是否正确
- 验证网络连接
- 检查 API 服务状态
- 使用 `--verbose` 获取详细错误信息

### 特定提供商失败

- 检查提供商配置
- 验证提供商服务状态
- 自动跳过到下一个提供商

### 图片质量问题

- 尝试不同的提供商
- 使用更多细节优化提示
- 尝试不同的风格设置

## 参考文档

- [图片创建完整流程](references/image-creation-workflow.md) - 从需求到输出的全流程
- [场景模型选型指南](references/scene-model-selection-guide.md) - 不同场景的模型选择
- [风格指南](references/style-guide.md) - 丰富的风格关键词库
- [Prompt 编写指南](references/prompt-writing-guide.md) - 系统的 Prompt 编写方法
- [最佳实践](references/best-practices.md) - 汇总最佳实践
