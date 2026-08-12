# 跨平台 CLI 图像处理工具指南

## 概述

本文档介绍一款真正的跨平台命令行图像处理工具 —— **ImageMagick**。它支持 Windows、macOS、Linux，开箱即用，是 AI 生图后处理的"瑞士军刀"：裁切、改比例、压缩、转格式、批量处理、拼图、加水印，几行命令就能搞定。

## 工具对比

| 工具 | 跨平台 | 速度 | 上手难度 | 适合 |
|------|--------|------|---------|------|
| **ImageMagick** | ✅ Win/Mac/Linux | 中 | 低（命令多但常用就几条） | 瑞士军刀，啥都能干 |
| Photoshop | ❌ 需安装 | 慢 | 高 | 专业设计 |
| GIMP | ✅ 免费 | 中 | 中 | 免费替代 PS |
| FFmpeg | ✅ 跨平台 | 快 | 中 | 视频/批量处理 |
| Squoosh | ✅ Web | 慢 | 低 | 单次压缩 |

## 安装

### macOS

```bash
brew install imagemagick
```

### Ubuntu / Debian

```bash
sudo apt-get update
sudo apt-get install imagemagick
```

### Windows

1. 下载安装包：https://imagemagick.org/script/download.php#windows
2. 安装时勾选 "Add to PATH"
3. 重启终端

### 验证安装

```bash
magick --version
```

## 常用命令速查

### 1. 裁切 + 改比例 + 压缩一条龙

把图片裁切成 1920x1080，居中裁剪，输出为 WebP：

```bash
magick input.png \
  -resize 1920x1080^ \
  -gravity center \
  -extent 1920x1080 \
  -quality 85 \
  output.webp
```

参数说明：

| 参数 | 说明 |
|------|------|
| `-resize 1920x1080^` | 按比例缩放，短边至少填满目标尺寸 |
| `-gravity center` | 从中心裁切 |
| `-extent 1920x1080` | 扩展到指定尺寸 |
| `-quality 85` | WebP/JPEG 质量 85% |

### 2. 转 WebP 并压缩

```bash
magick input.png -quality 85 output.webp
```

### 3. 批量缩放

把当前目录所有 PNG 缩放到最大边 1024px：

```bash
magick mogrify -resize 1024x1024 *.png
```

> ⚠️ `mogrify` 会直接覆盖原图，建议先备份。

### 4. 拼图（4 张合成 2x2）

```bash
# 横向拼接 1.png 和 2.png
magick 1.png 2.png +append row1.png

# 横向拼接 3.png 和 4.png
magick 3.png 4.png +append row2.png

# 纵向拼接两行
magick row1.png row2.png -append out.png
```

或者直接用括号一次性完成：

```bash
magick \( 1.png 2.png +append \) \
       \( 3.png 4.png +append \) \
       -append out.png
```

### 5. 加水印

```bash
magick input.png \
  -gravity southeast \
  -fill "white" \
  -pointsize 24 \
  -annotate +20+20 "© MyBrand" \
  output.png
```

参数说明：

| 参数 | 说明 |
|------|------|
| `-gravity southeast` | 水印位置：右下角 |
| `-fill "white"` | 文字颜色 |
| `-pointsize 24` | 字体大小 |
| `-annotate +20+20` | 距离边缘 20px |

### 6. 抠图去背景（AI）

ImageMagick 本身不是 AI 抠图工具，但可以配合 `rembg` 使用：

```bash
# 安装 rembg
pip install rembg

# 抠图
rembg i input.png output.png
```

### 7. 调整图片尺寸（保持比例）

```bash
# 宽度调整为 800px，高度按比例缩放
magick input.png -resize 800x output.png

# 高度调整为 600px，宽度按比例缩放
magick input.png -resize x600 output.png

# 最大边不超过 1024px
magick input.png -resize 1024x1024\> output.png
```

### 8. 格式转换

```bash
magick input.png output.jpg
magick input.jpg output.webp
magick input.webp output.avif
```

### 9. 查看图片信息

```bash
magick identify input.png
```

### 10. 压缩 PNG

```bash
magick input.png -strip -quality 90 output.png
```

## AI 生图后处理流程

把 ImageMagick 接入 deep-core-image  workflow：

```bash
# 1. 生成图片
python scripts/generate_image.py \
  --prompt "a cute cat" \
  --ratio 1:1 \
  --output output/raw/cat.png

# 2. 裁切/改比例 + 压缩 + 转 WebP
magick output/raw/cat.png \
  -resize 1024x1024^ \
  -gravity center \
  -extent 1024x1024 \
  -quality 85 \
  output/web/cat.webp

# 3. 加 Logo 水印
magick output/web/cat.webp \
  -gravity southeast \
  -fill "white" \
  -pointsize 20 \
  -annotate +10+10 "© MyBrand" \
  output/final/cat.webp
```

## 批量处理脚本

### 批量生成多尺寸 WebP

```bash
#!/bin/bash
# generate_webp.sh

INPUT_DIR="output/raw"
OUTPUT_DIR="output/web"
mkdir -p "$OUTPUT_DIR"

for img in "$INPUT_DIR"/*.{png,jpg,jpeg}; do
  [ -f "$img" ] || continue
  filename=$(basename "$img" | sed 's/\.[^.]*$//')
  
  # 原尺寸 85% 质量 WebP
  magick "$img" -quality 85 "$OUTPUT_DIR/${filename}.webp"
  
  # 缩略图 512x512
  magick "$img" -resize 512x512^ -gravity center -extent 512x512 -quality 80 "$OUTPUT_DIR/${filename}_thumb.webp"
done

echo "Done!"
```

### 批量加水印

```bash
#!/bin/bash
# batch_watermark.sh

for img in output/web/*.webp; do
  magick "$img" \
    -gravity southeast \
    -fill "rgba(255,255,255,0.7)" \
    -pointsize 18 \
    -annotate +15+15 "© MyBrand" \
    "$img"
done
```

## 常见问题

### Q1: `magick: command not found`

**解决**：
- macOS: `brew install imagemagick`
- Linux: `sudo apt-get install imagemagick`
- Windows: 安装时勾选 "Add to PATH"

### Q2: 批量处理时覆盖原图

**解决**：使用 `convert` 而不是 `mogrify`，或先复制到输出目录：

```bash
cp input/*.png output/
magick mogrify -resize 1024x1024 output/*.png
```

### Q3: WebP 压缩后体积还是很大

**解决**：降低 quality 或调整 resize 尺寸：

```bash
magick input.png -resize 800x800 -quality 75 output.webp
```

### Q4: 裁切后主体被切掉

**解决**：改用 `-gravity` 指定裁切重心，或先调整尺寸再裁切：

```bash
magick input.png -resize 1920x1080^ -gravity north -extent 1920x1080 output.webp
```

## 推荐组合

| 场景 | 命令 |
|------|------|
| 网站配图压缩 | `magick input.png -resize 1200x -quality 80 output.webp` |
| 社交媒体头像 | `magick input.png -resize 400x400^ -gravity center -extent 400x400 output.jpg` |
| 电商主图 | `magick input.png -resize 800x800 -background white -gravity center -extent 800x800 output.jpg` |
| 拼接长图 | `magick *.png -append output.png` |
| 批量转 WebP | `for f in *.png; do magick "$f" -quality 85 "${f%.png}.webp"; done` |

## 与 deep-core-image 联动

| 想做的事 | 工具组合 |
|---------|---------|
| AI 生图 + 裁切压缩 | deep-core-image + ImageMagick |
| 批量生成多尺寸素材 | deep-core-image + ImageMagick 批量脚本 |
| 给生成图加水印 | deep-core-image + ImageMagick annotate |
| 生成图去背景 | deep-core-image + rembg |
| 生成图拼版展示 | deep-core-image + ImageMagick append |

## 总结

- **ImageMagick 是 AI 生图后处理的最佳 CLI 搭档**
- 一条命令完成裁切、改比例、压缩、转格式
- 跨平台、免费、功能极其丰富
- 掌握上面 10 条命令，能满足 90% 的日常图像处理需求

**一句话：AI 负责生成，ImageMagick 负责交付。**
