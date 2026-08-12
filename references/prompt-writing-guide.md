# Prompt 编写指南

## 概述

本文档提供 Prompt 编写的系统方法论，帮助用户写出高质量、可复用的 Prompt，生成符合预期的图片。好的 Prompt 是好图片的一半。

## Prompt 黄金公式

```
[主体] + [动作/状态] + [环境/背景] + [风格] + [光线/色调] + [构图] + [画质关键词]
```

### 公式分解

| 要素 | 说明 | 示例 |
|------|------|------|
| 主体 | 图片的核心对象 | a young woman, a modern laptop, a cute cat |
| 动作/状态 | 主体在做什么 | sitting, working, flying, sleeping |
| 环境/背景 | 场景在哪里 | in a coffee shop, on a mountain, in space |
| 风格 | 视觉风格 | flat illustration, photorealistic, watercolor |
| 光线/色调 | 光影和色彩 | warm lighting, golden hour, neon glow |
| 构图 | 画面布局 | centered, rule of thirds, close-up |
| 画质 | 质量关键词 | 8k, ultra-detailed, masterpiece |

## Prompt 模板

### 正面 Prompt 模板

```
[main subject description],
[action or state],
[environment/background],
[style keywords],
[lighting and color tone],
[composition],
[quality keywords: 8k, ultra-detailed, masterpiece]
```

### 负面 Prompt 模板（避免常见翻车）

```
ugly, deformed, noxious, bad anatomy, extra limbs,
blurry, low quality, pixelated, watermark, text, signature,
oversaturated, distorted proportions
```

## 分场景 Prompt 模板

### 营销 Banner

```
[product/brand] hero banner,
modern minimal style, gradient background,
centered composition, eye-catching,
professional photography, studio lighting,
8k, ultra-detailed
```

**示例**：
```
Tech startup hero banner,
modern minimal style,
blue gradient background,
centered composition,
eye-catching design,
professional photography, studio lighting,
8k, ultra-detailed
```

### 公众号头图

```
[topic] themed illustration,
editorial illustration style, warm colors,
balanced composition, soft lighting,
subtle textures, professional quality
```

**示例**：
```
AI technology themed illustration,
editorial illustration style,
blue and white color scheme,
balanced composition, soft lighting,
subtle textures, professional quality
```

### App Icon

```
single icon design of [subject],
flat design, rounded square,
solid background, minimal details,
modern app icon style, vector art,
centered, clean composition
```

**示例**：
```
single icon design of a camera,
flat design, rounded square,
solid white background, minimal details,
modern app icon style, vector art,
centered, clean composition
```

### 国风插画

```
[scene] in traditional Chinese painting style,
shuimo ink wash, xieyi brushwork,
muted earthy tones, silk texture,
Song Dynasty aesthetic, vertical scroll,
subtle red seal stamp
```

**示例**：
```
山水之间，一位隐士独坐亭中，
traditional Chinese painting style,
shuimo ink wash, xieyi brushwork,
muted earthy tones, silk texture,
Song Dynasty aesthetic, vertical scroll,
subtle red seal stamp
```

### 占位/验证图

```
simple [subject],
flat colors, minimal style,
centered, clean background,
low detail, quick sketch
```

**示例**：
```
simple house icon,
flat colors, minimal style,
centered, clean white background,
low detail, quick sketch
```

### 产品展示

```
[product] product photography,
clean white background,
studio lighting, soft shadows,
professional product shot,
high detail, commercial quality
```

**示例**：
```
A modern smartphone product photography,
clean white background,
studio lighting, soft shadows,
professional product shot,
high detail, commercial quality,
8k ultra-detailed
```

### 人物肖像

```
professional headshot of [person description],
studio lighting, soft background,
sharp focus on face,
photorealistic, portrait photography
```

**示例**：
```
professional headshot of a young business man,
studio lighting, soft gray background,
sharp focus on face,
photorealistic, portrait photography,
8k ultra-detailed
```

### 场景插画

```
[scene description],
[art style] illustration,
[color palette],
[composition],
[quality keywords]
```

**示例**：
```
A cozy reading nook with bookshelves,
flat illustration style,
warm pastel colors,
balanced composition,
professional quality, clean lines
```

## Prompt 编写原则

### 1. 具体明确

**❌ 错误示例**：
```
A beautiful landscape
```

**✅ 正确示例**：
```
A serene mountain lake at sunrise,
snow-capped peaks reflected in crystal clear water,
pine forest on the shoreline,
golden morning light,
landscape photography, 8k
```

**原则**：用具体名词代替抽象描述，增加细节让模型更好理解。

### 2. 结构清晰

**❌ 错误示例**：
```
cat cute sitting window sun warm
```

**✅ 正确示例**：
```
A cute orange tabby cat,
sitting on a windowsill,
basking in warm sunlight,
cozy home interior,
soft natural lighting,
photorealistic, 8k
```

**原则**：按公式组织，层次分明，用逗号分隔不同要素。

### 3. 风格统一

**❌ 错误示例**：
```
A cat, photorealistic, cartoon style, watercolor,
oil painting, digital art, minimalist, detailed
```

**✅ 正确示例**：
```
A cute cat,
flat illustration style,
pastel colors,
clean background,
modern design
```

**原则**：每次只定 1-2 个主风格，避免风格词过多导致模型困惑。

### 4. 比例正确

**❌ 错误示例**：
```
9:16 竖屏，一位年轻程序员坐在电脑前
```

**✅ 正确示例**：
```
一位年轻程序员坐在电脑前，
现代办公室环境，
纯画面无边框
```

**原则**：比例通过参数指定，不在 Prompt 中写比例词（会诱发手机边框）。

## 中文 Prompt 编写

### 中文 Prompt 优势

- 中文模型（qwen-image、qwen-image-flash）对中文理解更好
- 国风、古风主题用中文更准确
- 中文文字渲染用中文 Prompt 效果更好

### 中文 Prompt 示例

**国风海报**：
```
龙凤呈祥，传统中国节日海报，
中国水墨画风格，
红金配色，
传统纹样装饰，
竖幅构图，
shuimo brushwork，
红色印章点缀
```

**现代插画**：
```
一位年轻女性在咖啡店工作，
扁平插画风格，
温暖的色调，
柔和的光线，
干净的构图，
现代设计感
```

**产品图**：
```
一部智能手机产品展示，
纯白背景，
专业摄影棚灯光，
柔和的阴影，
商业摄影风格，
8k 超清细节
```

## Prompt 优化技巧

### 1. 增加细节

**基础版**：
```
A dog
```

**优化版**：
```
A golden retriever puppy,
sitting in a garden,
soft sunlight filtering through trees,
happy expression, tongue out,
photorealistic, shallow depth of field,
8k ultra-detailed
```

### 2. 明确风格

**模糊版**：
```
A nice picture of a city
```

**明确版**：
```
A futuristic cityscape at night,
cyberpunk style,
neon lights reflecting on wet streets,
dramatic lighting,
cinematic composition,
8k ultra-detailed, digital art
```

### 3. 指定光线

**普通版**：
```
A portrait of a woman
```

**优化版**：
```
A portrait of a young woman,
golden hour lighting,
warm sunlight on face,
soft bokeh background,
professional portrait photography,
8k ultra-detailed
```

### 4. 控制构图

**随意版**：
```
A mountain landscape
```

**优化版**：
```
A majestic mountain landscape,
rule of thirds composition,
foreground elements (wildflowers),
midground (lake),
background (snow-capped peaks),
golden hour lighting,
landscape photography, 8k
```

## 常见 Prompt 错误

### 1. 描述太抽象

**❌ 错误**：
```
Something beautiful
```

**✅ 正确**：
```
A beautiful sunset over the ocean,
vibrant orange and pink colors,
reflecting on calm water,
photorealistic, 8k
```

### 2. 风格词过多

**❌ 错误**：
```
A cat, photorealistic, cartoon, watercolor,
oil painting, digital, minimalist, detailed,
vintage, modern, futuristic, retro
```

**✅ 正确**：
```
A cute cat,
flat illustration style,
pastel colors,
clean design
```

### 3. 缺少画质词

**❌ 错误**：
```
A landscape with mountains
```

**✅ 正确**：
```
A landscape with mountains,
photorealistic, 8k ultra-detailed,
professional photography,
sharp focus
```

### 4. 比例词写入 Prompt

**❌ 错误**：
```
9:16 竖屏，一位程序员坐在电脑前
```

**✅ 正确**：
```
一位程序员坐在电脑前，
现代办公室环境，
纯画面无边框
```

**说明**：比例通过 API 参数指定，写入 Prompt 会诱发手机边框。

### 5. 负面 Prompt 缺失

**❌ 错误**：
```
A portrait of a person
```

**✅ 正确**：
```
正面：A portrait of a person, photorealistic, 8k
负面：ugly, deformed, blurry, low quality, extra limbs
```

## Prompt 复用与管理

### 建立 Prompt 库

1. **收集优秀 Prompt**：项目中效果好的 Prompt 都保存下来
2. **分类整理**：按场景、风格、用途分类
3. **标注效果**：记录哪些 Prompt 效果好，哪些需要改进
4. **持续迭代**：随项目积累不断优化

### Prompt 模板化

为常用场景建立模板，只需替换关键部分：

```markdown
## 产品展示模板

```
[产品名称] product photography,
clean white background,
studio lighting, soft shadows,
professional product shot,
high detail, commercial quality,
8k ultra-detailed
```

使用时只需替换 [产品名称]。
```

### 风格种子 Prompt

为常用风格建立"种子 Prompt"，确保风格统一：

```markdown
## 科技风格种子

```
[主体], tech illustration, blue gradient,
futuristic UI elements, clean lines,
modern design, professional quality
```

## 国风风格种子

```
[场景], Chinese ink painting style,
shuimo brushwork, muted earthy tones,
traditional composition, red seal stamp
```
```

## Prompt 调试流程

### Step 1: 基础版本

先写一个基础版本的 Prompt，测试基本方向：

```
A modern office workspace
```

### Step 2: 评估结果

生成图片后评估：
- 主体是否正确？
- 风格是否符合？
- 质量是否满意？

### Step 3: 优化迭代

根据评估结果优化：

```
A modern office workspace,
minimalist design,
natural lighting,
clean and organized,
professional photography, 8k
```

### Step 4: 重复评估

继续生成和评估，直到满意为止。

## 高级技巧

### 1. 权重控制

某些模型支持权重控制，用括号强调重要元素：

```
A (beautiful:1.2) sunset over the ocean,
(vibrant colors:1.1),
photorealistic, 8k
```

### 2. 多主体处理

**简单方式**：
```
A cat and a dog playing together in a park
```

**详细方式**：
```
A golden retriever puppy and an orange tabby cat,
playing together in a sunny park,
green grass, blue sky,
happy atmosphere,
photorealistic, 8k
```

### 3. 文字渲染

**普通 Prompt**：
```
A sign that says "Hello"
```

**优化 Prompt**（适合 gpt-image 或 qwen-image）：
```
A modern minimalist sign,
with clear readable text "Hello World",
white background, black text,
professional typography,
clean design
```

### 4. 风格混合

**安全方式**（选一个主导）：
```
A landscape, watercolor style with some digital elements
```

**风险方式**（可能冲突）：
```
A landscape, watercolor, oil painting, digital art, 3D render
```

## 总结

- **Prompt 是好图片的一半**：投入时间写好 Prompt
- **遵循黄金公式**：主体 + 动作 + 环境 + 风格 + 光线 + 构图 + 画质
- **具体明确**：用具体名词，增加细节
- **风格统一**：1-2 个主风格，不要堆砌
- **比例通过参数**：不要写入 Prompt
- **迭代优化**：写 → 生成 → 评估 → 优化 → 重复
- **建立 Prompt 库**：积累复用，提高效率

**一句话：好 Prompt = 具体 + 结构 + 统一 + 迭代。**
