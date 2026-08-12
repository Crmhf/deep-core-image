# Deep Core Image - Quick Start Guide

## 5 分钟快速开始

### 1. 安装依赖

```bash
cd /Users/diyuan/.cc-switch/skills/deep-core-image
pip install -r scripts/requirements.txt
```

### 2. 验证安装

```bash
python3 scripts/test_installation.py
```

### 3. 生成第一张图片

```bash
python3 scripts/generate_image.py \
  --prompt "A beautiful sunset over mountains" \
  --output sunset.png
```

### 4. 使用宽高比

```bash
# 16:9 宽屏
python3 scripts/generate_image.py \
  --prompt "A wide landscape" \
  --ratio 16:9 \
  --output landscape.png

# 9:16 竖屏（手机壁纸）
python3 scripts/generate_image.py \
  --prompt "Mobile wallpaper" \
  --ratio 9:16 \
  --output mobile.png
```

### 5. 指定提供商

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

## 常用命令

### 基本文生图

```bash
python3 scripts/generate_image.py \
  --prompt "你的图片描述" \
  --output output.png
```

### 自定义尺寸

```bash
python3 scripts/generate_image.py \
  --prompt "你的图片描述" \
  --size 2048x2048 \
  --output output.png
```

### 图生图

```bash
python3 scripts/generate_image.py \
  --prompt "转换为水彩画风格" \
  --input photo.jpg \
  --output watercolor.png
```

### 生成多张图片

```bash
python3 scripts/generate_image.py \
  --prompt "Logo 设计方案" \
  --n 3 \
  --output logo_{n}.png
```

## 支持的宽高比

| 比例 | 尺寸 | 用途 |
|------|------|------|
| 1:1 | 1024x1024 | 正方形，社交媒体 |
| 16:9 | 1792x1024 | 宽屏，横幅 |
| 9:16 | 1024x1792 | 竖屏，手机壁纸 |
| 4:3 | 1536x1152 | 标准比例 |
| 3:4 | 1152x1536 | 竖版标准 |
| 3:2 | 1536x1024 | 照片比例 |
| 2:3 | 1024x1536 | 竖版照片 |

## 提供商回退顺序

1. **GPT-Image-2** (主提供商)
2. **Qwen-Image** (备用)
3. **MiniMax Image-01** (最后备用)

当主提供商失败时，系统会自动尝试下一个提供商。

## 查看示例

```bash
./scripts/example_usage.sh
```

## 更多文档

- [README.md](README.md) - 项目概述
- [SETUP.md](SETUP.md) - 详细配置指南
- [SKILL.md](SKILL.md) - 完整技能文档

## 获取帮助

```bash
python3 scripts/generate_image.py --help
```
