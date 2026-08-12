# Deep Core Image 技能创建总结

## 创建完成

已成功创建 `deep-core-image` 技能，位于 `/Users/diyuan/.cc-switch/skills/deep-core-image/`

## 技能特性

### 多提供商回退系统

按照以下顺序自动回退：

1. **GPT-Image-2** - 主提供商
2. **Qwen-Image** - 备用提供商
3. **MiniMax Image-01** - 最后备用

当主提供商失败时，系统会自动尝试下一个提供商，确保图像生成的可靠性。

### 支持的功能

- ✅ 文生图 (Text-to-Image)
- ✅ 图生图 (Image-to-Image)
- ✅ 多图生成 (Multiple Images)
- ✅ 自定义宽高比 (Custom Aspect Ratios)
- ✅ 自定义尺寸 (Custom Sizes)
- ✅ 指定提供商 (Provider Selection)
- ✅ 自动重试 (Automatic Retry)
- ✅ 指数退避 (Exponential Backoff)

### 支持的宽高比

| 比例 | 尺寸 | 用途 |
|------|------|------|
| 1:1 | 1024x1024 | 正方形，社交媒体 |
| 16:9 | 1792x1024 | 宽屏，横幅 |
| 9:16 | 1024x1792 | 竖屏，手机壁纸 |
| 4:3 | 1536x1152 | 标准比例 |
| 3:4 | 1152x1536 | 竖版标准 |
| 3:2 | 1536x1024 | 照片比例 |
| 2:3 | 1024x1536 | 竖版照片 |

## 文件结构

```
/Users/diyuan/.cc-switch/skills/deep-core-image/
├── config.json                 # 配置文件（API 密钥、提供商配置）
├── README.md                   # 项目概述
├── SETUP.md                    # 详细配置指南
├── SKILL.md                    # 技能文档
├── QUICKSTART.md               # 快速开始指南
├── CHANGELOG.md                # 更新日志
├── SUMMARY.md                  # 本文件
└── scripts/
    ├── generate_image.py       # 主生成脚本 (688 行)
    ├── generate.bat            # Windows 批处理脚本
    ├── generate.sh             # Linux/macOS Shell 脚本
    ├── test_installation.py    # 安装测试脚本
    ├── example_usage.sh        # 使用示例
    └── requirements.txt        # Python 依赖
```

## 快速开始

### 1. 验证安装

```bash
cd /Users/diyuan/.cc-switch/skills/deep-core-image
python3 scripts/test_installation.py
```

### 2. 生成图片

```bash
# 基本用法
python3 scripts/generate_image.py \
  --prompt "A beautiful sunset" \
  --output sunset.png

# 使用宽高比
python3 scripts/generate_image.py \
  --prompt "A landscape" \
  --ratio 16:9 \
  --output landscape.png

# 指定提供商
python3 scripts/generate_image.py \
  --prompt "A cat" \
  --provider qwen-image \
  --output cat.png
```

### 3. 查看帮助

```bash
python3 scripts/generate_image.py --help
```

## 配置说明

### API 配置

配置文件：`config.json`

```json
{
    "default_provider": "gpt-image",
    "providers": {
        "gpt-image": {
            "api_key": "sk-LevqgoSsx0T8uoARC17zTQjvkfJO9MFfv8X4Kk5R7Sd9RKxe",
            "base_url": "http://cf.douzimi.com:58728/v1",
            "model": "gpt-image-2",
            "endpoint_type": "openai_compatible"
        },
        "qwen-image": {
            "api_key": "sk-LevqgoSsx0T8uoARC17zTQjvkfJO9MFfv8X4Kk5R7Sd9RKxe",
            "base_url": "http://cf.douzimi.com:58728/v1",
            "model": "Qwen/Qwen-Image",
            "endpoint_type": "openai_compatible"
        },
        "minimax-image": {
            "api_key": "sk-cp-g2B6sEzavQ5nKqPszn6aqBE9ictkmXkWGYvYU6DjWYL9CxGzwkNSy3hwqrgjBlM54TL5nMPB13-W88kEb76-IavaQHysXVtNN-zogFFcANoiew-aXMYkl9Y",
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

```bash
# 覆盖所有提供商的 API Key
export DEEP_CORE_IMAGE_API_KEY="your-api-key"

# 覆盖所有提供商的 Base URL
export DEEP_CORE_IMAGE_BASE_URL="http://your-proxy/v1"

# 设置默认提供商
export DEEP_CORE_IMAGE_DEFAULT_PROVIDER="qwen-image"
```

## 使用示例

### 示例 1：基本文生图

```bash
python3 scripts/generate_image.py \
  --prompt "Create a professional infographic about AI technology trends" \
  --output ai_infographic.png
```

### 示例 2：使用宽高比

```bash
# 16:9 宽屏
python3 scripts/generate_image.py \
  --prompt "A beautiful landscape" \
  --ratio 16:9 \
  --output landscape.png

# 9:16 竖屏（手机壁纸）
python3 scripts/generate_image.py \
  --prompt "Mobile wallpaper" \
  --ratio 9:16 \
  --output mobile.png
```

### 示例 3：指定提供商

```bash
# 使用 Qwen-Image
python3 scripts/generate_image.py \
  --prompt "A cute cat" \
  --provider qwen-image \
  --output cat.png

# 使用 MiniMax
python3 scripts/generate_image.py \
  --prompt "A dog" \
  --provider minimax-image \
  --output dog.png
```

### 示例 4：图生图

```bash
python3 scripts/generate_image.py \
  --prompt "Convert to anime style" \
  --input photo.jpg \
  --output anime.png
```

### 示例 5：生成多张图片

```bash
python3 scripts/generate_image.py \
  --prompt "Logo design concepts" \
  --n 3 \
  --output logo_{n}.png
```

### 示例 6：自定义尺寸

```bash
python3 scripts/generate_image.py \
  --prompt "High resolution product photo" \
  --size 2048x2048 \
  --output product.png
```

## 回退机制详解

### 工作流程

1. 尝试主提供商 (GPT-Image-2)
2. 如果失败，重试最多 3 次（指数退避）
3. 如果仍然失败，尝试下一个提供商 (Qwen-Image)
4. 重复上述过程
5. 如果所有提供商都失败，返回错误

### 重试策略

- 第 1 次重试：等待 1 秒
- 第 2 次重试：等待 2 秒
- 第 3 次重试：等待 4 秒

### 错误处理

系统会处理以下错误：
- 网络连接错误
- API 超时
- 认证失败
- 速率限制
- 无效参数

## 文档说明

- **README.md** - 项目概述和快速开始
- **SETUP.md** - 详细的配置和安装指南
- **SKILL.md** - 完整的技能文档和使用说明
- **QUICKSTART.md** - 5 分钟快速开始指南
- **CHANGELOG.md** - 版本更新日志
- **SUMMARY.md** - 本文件，创建总结

## 依赖要求

- Python 3.7+
- requests>=2.28.0

## 注意事项

1. **API 密钥安全**：请妥善保管 API 密钥，不要泄露到公共代码仓库
2. **速率限制**：不同提供商有不同的速率限制，请注意使用频率
3. **图片内容**：请遵守各提供商的内容政策，不要生成违规内容
4. **网络连接**：需要稳定的网络连接才能使用
5. **图片大小**：大尺寸图片（如 4096x4096）生成时间较长

## 故障排除

### 问题：所有提供商都失败

**解决方案：**
1. 检查 API 密钥是否正确
2. 验证网络连接
3. 使用 `--verbose` 查看详细错误信息
4. 检查 API 服务状态

### 问题：特定提供商失败

**解决方案：**
1. 检查该提供商的配置
2. 验证 API 密钥是否有效
3. 系统会自动跳过失败的提供商

### 问题：图片质量不理想

**解决方案：**
1. 尝试使用不同的提供商
2. 优化提示词，添加更多细节
3. 尝试不同的风格设置
4. 使用更高的质量设置

## 扩展和自定义

### 添加新提供商

1. 在 `config.json` 中添加新的提供商配置
2. 在 `fallback_order` 中添加提供商名称
3. 在 `generate_image.py` 中添加对应的生成函数

### 修改回退顺序

编辑 `config.json` 中的 `fallback_order` 数组：

```json
{
    "fallback_order": ["minimax-image", "gpt-image", "qwen-image"]
}
```

### 修改默认设置

编辑 `config.json` 中的默认值：

```json
{
    "default_size": "2048x2048",
    "default_quality": "standard",
    "default_style": "natural"
}
```

## 总结

`deep-core-image` 技能提供了一个强大、可靠的图像生成解决方案，通过多提供商回退机制确保高可用性。支持多种宽高比和尺寸，满足不同场景的需求。

技能已经完全配置好，可以直接使用。所有 API 密钥都已配置在 `config.json` 中。
