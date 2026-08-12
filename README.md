# Deep Core Image

> 多模型 AI 图像生成技能栈 —— 按场景选模型，minimax 兜底。

## 项目定位

**Deep Core Image** 是一个面向 Web 应用、网站、小程序、日常配图、小图标、验证草图等场景的 AI 图像生成技能。它整合多个主流图像生成模型（gpt-image、minimax-image、qwen-image、qwen-image-flash），提供统一的调用入口、自动降级机制、场景化选型指导和 Prompt 最佳实践。

**核心目标**：

- **简单调用**：一条命令生成图片，自动处理多模型降级
- **场景化选型**：按复杂度和场景推荐最合适的模型，避免一刀切
- **成本可控**：80% 日常任务用 minimax-image 兜底，只在关键场景使用高价模型
- **质量稳定**：提供完整的 Prompt 模板、风格库和生成流程，确保输出可用

## 适用场景

| 场景类型 | 示例 | 推荐模型 |
|---------|------|---------|
| Web 应用 / 网站 | Hero 图、Banner、博客配图、404 插画 | minimax-image / gpt-image |
| 小程序 | 启动页、分享卡片、分类图标、弹窗图 | minimax-image / qwen-image-flash |
| 日常做图 | 公众号头图、PPT 配图、朋友圈海报 | minimax-image / gpt-image |
| 小图标 | App Icon、工具栏图标、功能图标 | qwen-image-flash / minimax-image |
| 验证草图 | 概念验证、A/B 测试、mood board | qwen-image-flash |
| 国风 / 东方美学 | 国风海报、中文书法、传统题材 | qwen-image |

## 模型矩阵

| 模型 | 能力档位 | 成本 | 速度 | 主用场景 | 当前状态 |
|------|---------|------|------|---------|---------|
| **gpt-image** | ⭐⭐⭐⭐⭐ S 级 | 高 | 慢 | 品牌主图、复杂海报、影视级美感 | ⚠️ 取决于端点（KMAGE 格式已适配） |
| **minimax-image** | ⭐⭐⭐⭐ A 级 | 中 | 中 | **日常主力、兜底模型** | ✅ 可用（响应解析已修复） |
| **qwen-image** | ⭐⭐⭐ A-级 | 中 | 中 | 国风、中文海报、东方美学 | ✅ 可用 |
| **qwen-image-flash** | ⭐⭐ B 级 | 低 | 快 | 图标、占位、迭代验证 | ✅ 可用（默认 b64_json） |

> **注意**：代码已按 KMAGE API 格式完成适配，支持文生图和图生图。`minimax-image` 与 `qwen-image` / `qwen-image-flash` 实测可用；`gpt-image` 能否使用取决于 `config.json` 中配置的 `base_url` 是否真的是 KMAGE 端点。

## 快速开始

### 1. 安装依赖

```bash
pip install -r scripts/requirements.txt
```

### 2. 配置 API 密钥

复制配置模板并填写密钥：

```bash
cp config.sample.json config.json
```

编辑 `config.json`：

```json
{
    "default_provider": "gpt-image",
    "providers": {
        "gpt-image": {
            "endpoints": [
                {
                    "base_url": "http://your-proxy-1/v1",
                    "api_key": "your-api-key-1"
                },
                {
                    "base_url": "http://your-proxy-2/v1",
                    "api_key": "your-api-key-2"
                }
            ],
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
            "model": "qwen-image-flash",
            "endpoint_type": "openai_compatible"
        },
        "minimax-image": {
            "api_key": "your-minimax-api-key",
            "base_url": "https://api.minimaxi.com/v1",
            "model": "image-01",
            "endpoint_type": "minimax"
        }
    },
    "fallback_order": ["gpt-image", "qwen-image", "minimax-image", "qwen-image-flash"]
}
```

> **gpt-image 多端点负载均衡**：`gpt-image` 支持配置多个 `endpoints`。脚本会按顺序尝试每个端点，单个端点失败时自动切换到下一个端点；如果所有端点都失败，再按 `fallback_order` 切换到其他 provider。适合为 gpt-image 配置多个代理或密钥，提高可用性。

### 3. 生成图片

```bash
# 基础使用（自动走默认 provider）
python scripts/generate_image.py --prompt "夕阳下的山脉" --output sunset.png

# 指定宽高比
python scripts/generate_image.py --prompt "美丽的风景" --ratio 16:9 --output landscape.png

# 指定模型
python scripts/generate_image.py --prompt "一只可爱的猫" --provider minimax-image --output cat.png

# 图生图
python scripts/generate_image.py \
  --prompt "将这只猫转换为水彩画风格" \
  --input cat.png \
  --output cat-watercolor.png
```

## 完整文档

- [SKILL.md](SKILL.md) - 技能主文档、使用示例、参数说明
- [references/image-creation-workflow.md](references/image-creation-workflow.md) - 图片创建完整流程
- [references/scene-model-selection-guide.md](references/scene-model-selection-guide.md) - 场景模型选型指南
- [references/style-guide.md](references/style-guide.md) - 风格关键词库
- [references/prompt-writing-guide.md](references/prompt-writing-guide.md) - Prompt 编写指南
- [references/best-practices.md](references/best-practices.md) - 最佳实践汇总
- [references/generate-image-guide.md](references/generate-image-guide.md) - `generate_image.py` 脚本构建与指定 provider 调用指南
- [references/cli-image-processing-guide.md](references/cli-image-processing-guide.md) - 跨平台 CLI 图像处理工具指南

## 模型可用性分析

基于 2026-08-12 的实际测试：

### ✅ qwen-image（可用）

- **测试方式**：直接指定 provider 为 `qwen-image`
- **测试结果**：文生图、图生图均成功生成
- **输出示例**：
  - `output/test-scenarios/01-web-hero-banner.png`（16:9，Web Hero Banner）
  - `output/test-scenarios/02-chinese-landscape.png`（3:4，国风山水画）
  - `output/test-scenarios/03-camera-icon.png`（1:1，相机图标）
- **结论**：当前最稳定的模型，建议作为默认 provider

### ✅ minimax-image（可用）

- **测试方式**：直接指定 provider 为 `minimax-image`
- **测试结果**：文生图、图生图均成功生成
- **修复内容**：
  - 使用官方 `aspect_ratio` 参数替代 `width/height`
  - 支持 `response_format: base64`
  - 支持 `subject_reference` 图生图
  - 正确解析 `data.image_urls` 和 `data.image_base64`

### ⚠️ gpt-image（取决于端点）

- **适配内容**：
  - 移除默认 `style` 参数传递
  - 图生图字段从 `image` 改为 `reference_images`
  - 默认 `response_format` 改为 `b64_json`
  - 尺寸映射改为 KMAGE 支持的 `1536x864` / `864x1536`
- **当前状态**：当前 `config.json` 配置的 `base_url` 不是 KMAGE 端点，对该模型请求超时，需替换为真实 KMAGE 站点域名
- **建议**：将 `base_url` 替换为真实的 KMAGE 站点域名后再测试

### ✅ qwen-image-flash（可用）

- **测试方式**：直接指定 provider 为 `qwen-image-flash`
- **测试结果**：成功生成图片
- **修复内容**：默认 `response_format` 改为 `b64_json`

## 当前推荐用法

```bash
# 默认 provider 已设为 gpt-image，内部多 endpoint 自动负载均衡
python scripts/generate_image.py \
  --prompt "你的 Prompt" \
  --ratio 16:9 \
  --output output/项目名/图片.png

# 指定 minimax-image（日常主力）
python scripts/generate_image.py \
  --provider minimax-image \
  --prompt "你的 Prompt" \
  --ratio 16:9 \
  --output output/项目名/图片.png

# 图生图
python scripts/generate_image.py \
  --provider qwen-image \
  --input input/原图.png \
  --prompt "转换为水彩画风格" \
  --output output/项目名/水彩版.png
```

## 项目结构

```
deep-core-image/
├── README.md                       # 本文件
├── SKILL.md                        # 技能主文档
├── config.json                     # 配置文件（本地，不提交）
├── config.sample.json              # 配置模板
├── scripts/                        # 执行脚本
│   ├── generate_image.py           # 主生成脚本
│   ├── generate.sh                 # Unix 启动脚本
│   ├── generate.bat                # Windows 启动脚本
│   ├── example_usage.sh            # 使用示例
│   └── test_installation.py        # 安装测试
├── references/                     # 指南文档
│   ├── image-creation-workflow.md  # 图片创建完整流程
│   ├── scene-model-selection-guide.md  # 场景模型选型
│   ├── style-guide.md              # 风格关键词库
│   ├── prompt-writing-guide.md     # Prompt 编写指南
│   └── best-practices.md           # 最佳实践
├── output/                         # 最终输出目录
└── temp/                           # 过程文件目录
```

## 核心原则

```
复杂/品牌 → gpt-image
日常/通用/兜底 → minimax-image
国风/古风/中文书法 → qwen-image
图标/占位/快速验证 → qwen-image-flash
```

**二八原则**：

```
80% 场景用 minimax-image
15% 场景用 gpt-image 提质
4% 场景用 qwen-image 走东方
1% 场景用 qwen-image-flash 验证
```

## 命令行参数

```
--prompt, -p      图片描述（必填）
--output, -o      输出文件路径（必填）
--input, -i       图生图的输入图片
--size, -s        图片尺寸（如 1024x1024）
--ratio, -r       宽高比（如 16:9、1:1）
--quality, -q     图片质量（auto、low、medium、high、standard、hd）
--style           图片风格（vivid、natural，可选，部分端点支持）
--n, --num        图片数量（1-10）
--provider        强制指定提供商
--response-format 返回格式（url、b64_json，默认 b64_json）
--no-proxy        绕过系统代理
--verbose, -v     详细输出
```

## 支持的宽高比

| 比例 | 尺寸 | 适用场景 |
|------|------|---------|
| 1:1 | 1024x1024 | 方形，社交媒体头像 |
| 16:9 | 1536x864 | 宽屏，横幅，风景 |
| 9:16 | 864x1536 | 竖屏，手机壁纸，海报 |
| 4:3 | 1536x1152 | 标准比例 |
| 3:4 | 1152x1536 | 竖屏标准 |
| 3:2 | 1536x1024 | 摄影比例 |
| 2:3 | 1024x1536 | 竖屏摄影 |

## 许可证

本技能按原样提供，用于与 Claude Code 配合使用。
