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
| **gpt-image** | ⭐⭐⭐⭐⭐ S 级 | 高 | 慢 | 品牌主图、复杂海报、影视级美感 | 当前不可用（HTTP 400） |
| **minimax-image** | ⭐⭐⭐⭐ A 级 | 中 | 中 | **日常主力、兜底模型** | 当前不可用（响应格式解析问题） |
| **qwen-image** | ⭐⭐⭐ A-级 | 中 | 中 | 国风、中文海报、东方美学 | ✅ 可用 |
| **qwen-image-flash** | ⭐⭐ B 级 | 低 | 快 | 图标、占位、迭代验证 | 当前不可用（需 b64_json 格式） |

> **注意**：当前实测只有 `qwen-image` 可直接正常工作。`gpt-image`、`minimax-image`、`qwen-image-flash` 存在接口兼容性问题，需要后续修复。详细分析见 [模型可用性分析](#模型可用性分析)。

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
    "default_provider": "qwen-image",
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
    "fallback_order": ["qwen-image", "minimax-image", "gpt-image", "qwen-image-flash"]
}
```

### 3. 生成图片

```bash
# 基础使用（自动走默认 provider）
python scripts/generate_image.py --prompt "夕阳下的山脉" --output sunset.png

# 指定宽高比
python scripts/generate_image.py --prompt "美丽的风景" --ratio 16:9 --output landscape.png

# 指定模型
python scripts/generate_image.py --prompt "一只可爱的猫" --provider qwen-image --output cat.png
```

## 完整文档

- [SKILL.md](SKILL.md) - 技能主文档、使用示例、参数说明
- [references/image-creation-workflow.md](references/image-creation-workflow.md) - 图片创建完整流程
- [references/scene-model-selection-guide.md](references/scene-model-selection-guide.md) - 场景模型选型指南
- [references/style-guide.md](references/style-guide.md) - 风格关键词库
- [references/prompt-writing-guide.md](references/prompt-writing-guide.md) - Prompt 编写指南
- [references/best-practices.md](references/best-practices.md) - 最佳实践汇总

## 模型可用性分析

基于 2026-08-12 的实际测试：

### ✅ qwen-image（可用）

- **测试方式**：直接指定 provider 为 `qwen-image`
- **测试结果**：成功生成图片
- **输出示例**：
  - `output/test-scenarios/01-web-hero-banner.png`（16:9，Web Hero Banner）
  - `output/test-scenarios/02-chinese-landscape.png`（3:4，国风山水画）
  - `output/test-scenarios/03-camera-icon.png`（1:1，相机图标）
- **结论**：当前最稳定的模型，建议作为默认 provider

### ❌ gpt-image（不可用）

- **问题**：返回 `HTTP 400 - Invalid image generation request`
- **可能原因**：
  - 代理端点不支持 `gpt-image-2` 的特定参数
  - `quality` / `style` 参数不被当前端点接受
  - 模型名称或端点配置需要调整
- **建议**：排查代理端点兼容性，或参考 OpenAI Image API 最新文档调整请求参数

### ❌ minimax-image（不可用）

- **问题**：API 返回成功（`status_msg: success` 且包含 `image_urls`），但脚本提示 `Unexpected MiniMax response format`
- **可能原因**：
  - MiniMax 实际返回的响应格式与 `generate_image.py` 中解析的格式不一致
  - 脚本期望的字段名或响应结构已过时
- **建议**：更新 `generate_image.py` 中 MiniMax 响应解析逻辑，适配 `data.image_urls` 字段

### ❌ qwen-image-flash（不可用）

- **问题**：返回 `HTTP 400 - Only 'b64_json' or 'file' response format is supported, got: ***.URL`
- **可能原因**：`qwen-image-flash` 服务端不支持 `response_format: url`，只支持 `b64_json` 或 `file`
- **建议**：
  - 为 `qwen-image-flash` 单独设置 `response_format: b64_json`
  - 或在代码中根据模型自动切换 response_format

## 当前推荐用法

在三个模型修复之前，建议：

```bash
# 将默认 provider 设为 qwen-image
# 或每次生成时显式指定
python scripts/generate_image.py \
  --provider qwen-image \
  --prompt "你的 Prompt" \
  --ratio 16:9 \
  --output output/项目名/图片.png
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
--quality, -q     图片质量（standard、hd）
--style           图片风格（vivid、natural）
--n, --num        图片数量（1-10）
--provider        强制指定提供商
--response-format 返回格式（url、b64_json）
--no-proxy        绕过系统代理
--verbose, -v     详细输出
```

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

## 许可证

本技能按原样提供，用于与 Claude Code 配合使用。
