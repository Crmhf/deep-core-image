# 图片生成脚本构建与调用指南

## 概述

本文档说明 `scripts/generate_image.py` 脚本的构建方式、初始化流程，以及如何在生成图片时**直接指定使用某个 provider**。该脚本是 deep-core-image 技能的核心执行入口，负责统一调用 `gpt-image`、`minimax-image`、`qwen-image`、`qwen-image-flash` 四个模型，并自动处理降级。

## 初始化时脚本状态

在 deep-core-image 项目初始化时（`init` commit），`scripts/` 目录并不存在。`generate_image.py` 是在后续迭代中创建并纳入版本控制的。因此：

- **旧仓库**：如果没有 `scripts/` 目录，需要按本文档重新创建
- **新仓库**：如果从最新版本拉取，`scripts/` 目录已包含完整脚本

## 脚本定位

```
deep-core-image/
├── scripts/
│   └── generate_image.py      # 核心图片生成脚本
├── config.json                # 本地配置文件（不提交）
├── config.sample.json         # 配置模板
└── references/
    └── generate-image-guide.md # 本指南
```

## 脚本初始化流程

### 第一步：确认 scripts 目录存在

```bash
mkdir -p /Users/diyuan/.cc-switch/skills/deep-core-image/scripts
```

### 第二步：创建 generate_image.py

将 `generate_image.py` 文件放入 `scripts/` 目录。该脚本的核心能力包括：

1. **读取配置**：从 `config.json` 加载 providers、fallback_order、默认参数
2. **解析参数**：命令行参数、环境变量、配置文件的优先级合并
3. **统一调用**：根据 provider 的 `endpoint_type` 分发到 OpenAI 兼容或 MiniMax 端点
4. **自动降级**：主 provider 失败时按 `fallback_order` 尝试下一个
5. **保存图片**：支持 `b64_json` 和 `url` 两种响应格式

### 第三步：安装依赖

```bash
pip install -r scripts/requirements.txt
```

`requirements.txt` 内容：

```
requests
```

### 第四步：配置 API 密钥

```bash
cp config.sample.json config.json
```

编辑 `config.json`，填写真实的 API key 和 base_url。

## 直接指定 Provider 调用

这是最常见的使用方式：**明确告诉技能用哪个模型生成图片**。

### 命令行方式

```bash
# 使用 qwen-image
python scripts/generate_image.py \
  --provider qwen-image \
  --prompt "一只可爱的猫" \
  --ratio 1:1 \
  --output output/cat.png

# 使用 minimax-image
python scripts/generate_image.py \
  --provider minimax-image \
  --prompt "一只可爱的猫" \
  --ratio 16:9 \
  --output output/cat-banner.png

# 使用 qwen-image-flash（快速验证）
python scripts/generate_image.py \
  --provider qwen-image-flash \
  --prompt "simple cat icon, flat design" \
  --ratio 1:1 \
  --output output/cat-icon.png

# 使用 gpt-image（KMAGE 端点）
python scripts/generate_image.py \
  --provider gpt-image \
  --prompt "cinematic portrait of a cat, 8k" \
  --ratio 3:4 \
  --output output/cat-cinematic.png
```

### 不指定 Provider（自动降级）

```bash
python scripts/generate_image.py \
  --prompt "一只可爱的猫" \
  --ratio 1:1 \
  --output output/cat.png
```

此时会按 `config.json` 中的 `fallback_order` 自动尝试：

```
gpt-image → qwen-image → minimax-image → qwen-image-flash
```

### 环境变量方式

```bash
export DEEP_CORE_IMAGE_DEFAULT_PROVIDER=minimax-image
python scripts/generate_image.py --prompt "一只可爱的猫" --output output/cat.png
```

### 配置文件方式

修改 `config.json` 中的 `default_provider`：

```json
{
  "default_provider": "minimax-image"
}
```

## Provider 选择速查

| 场景 | 推荐 Provider | 调用示例 |
|------|--------------|---------|
| 日常配图 / 兜底 | `minimax-image` | `--provider minimax-image` |
| 国风 / 东方美学 | `qwen-image` | `--provider qwen-image` |
| 快速验证 / 图标 | `qwen-image-flash` | `--provider qwen-image-flash` |
| 品牌 / 复杂 / 影视级 | `gpt-image` | `--provider gpt-image` |

## 完整命令行参数

```
--prompt, -p       图片描述（必填）
--output, -o       输出文件路径（必填）
--input, -i        图生图的输入图片
--size, -s         图片尺寸（如 1024x1024）
--ratio, -r        宽高比（1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3）
--quality, -q      图片质量（auto/low/medium/high/standard/hd）
--style            图片风格（vivid/natural，可选）
--n, --num         图片数量（1-10）
--provider         强制指定 provider（关键参数）
--response-format  返回格式（url/b64_json，默认 b64_json）
--no-proxy         绕过系统代理
--verbose, -v      详细输出
```

## 图生图调用

### OpenAI 兼容 Provider（gpt-image / qwen-image / qwen-image-flash）

```bash
python scripts/generate_image.py \
  --provider qwen-image \
  --input input/photo.jpg \
  --prompt "转换为水彩画风格" \
  --ratio 1:1 \
  --output output/watercolor.png
```

内部使用 `reference_images` 字段传递 Base64 Data URL。

### MiniMax Provider

```bash
python scripts/generate_image.py \
  --provider minimax-image \
  --input input/photo.jpg \
  --prompt "保留人物主体，将背景改为雪山" \
  --ratio 1:1 \
  --output output/minimax-i2i.png
```

内部使用 `subject_reference` 字段传递 Base64 Data URL。

## 脚本核心逻辑

```python
def generate_image_with_fallback(config, prompt, size, quality, ...):
    providers = config.get("providers", {})
    fallback_order = config.get("fallback_order", [])
    
    for provider_name in provider_order:
        provider_config = providers[provider_name]
        endpoint_type = provider_config.get("endpoint_type")
        
        if endpoint_type == "openai_compatible":
            # 使用 /v1/images/generations
            # gpt-image: reference_images 图生图
            # qwen-image: 标准 OpenAI 格式
            images = generate_openai_compatible(...)
        elif endpoint_type == "minimax":
            # 使用 /v1/image_generation
            # aspect_ratio + subject_reference
            images = generate_minimax(...)
        
        if images:
            return provider_name, images
```

## 故障排查

### 脚本不存在

```bash
ls scripts/generate_image.py
# 如果报错，从仓库重新拉取或按本指南重建
```

### 指定 provider 后仍使用其他 provider

**原因**：指定的 provider 配置缺失或失败，触发了自动降级。

**解决**：检查 `config.json` 中该 provider 的 `api_key` 和 `base_url`。

### gpt-image 超时或失败

**原因**：gpt-image-2 对端点稳定性要求高，单个代理/端点可能出现超时或不可用。

**解决**：
1. 在 `config.json` 中为 `gpt-image` 配置多个 `endpoints`，脚本会自动按顺序做负载均衡和降级
2. 使用 `--no-proxy` 绕过系统代理
3. 增加 `config.json` 中的 `timeout`
4. 如果所有 gpt-image 端点都失败，脚本会自动按 `fallback_order` 降级到 `qwen-image` 或 `minimax-image`

### 401 Invalid API key

**原因**：API key 与 base_url 不匹配。

**解决**：确认 provider 的 key 对应正确的服务端点。

## 最佳实践

1. **明确指定 provider**：不要依赖自动降级，按需选择模型
2. **验证阶段用 flash**：`qwen-image-flash` 快速验证 prompt 方向
3. **正式输出用 minimax/qwen**：平衡质量与成本
4. **关键图用 gpt-image**：确认 KMAGE 端点可用后再使用
5. **后处理用 ImageMagick**：生成后用 CLI 工具裁切、压缩、加水印

## 参考

- [SKILL.md](../SKILL.md) - 技能主文档
- [场景模型选型指南](scene-model-selection-guide.md) - 按场景选模型
- [跨平台 CLI 图像处理工具指南](cli-image-processing-guide.md) - 生图后处理
- [图片创建完整流程](image-creation-workflow.md) - 从需求到输出的全流程
