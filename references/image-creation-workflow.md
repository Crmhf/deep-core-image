# 图片创建完整流程指南

## 概述

本文档是 deep-core-image 的核心制作流程：从零开始创建一张高质量图片的完整步骤，涵盖从需求分析到最终输出的全流程。支持 Web 应用、网站、小程序、日常配图、小图标、验证草图等多种场景。

## 流程总览

```
1. 明确需求 → 2. 选择模型 → 3. 编写 Prompt → 4. 生成图片 → 5. 评估质量 → 6. 迭代优化 → 7. 后期处理
```

## 作品目录结构与文件命名（统一规范）

**过程内容**统一收敛到 `temp/<项目名>/` 文件夹内；**最终交付的图片**统一写入 `output/<项目名>/`。

```
temp/<项目名>/              # 过程内容（Prompt、中间产物、多版本尝试）
├── prompt-v1.md            # Prompt 版本
├── 概念图-v1.png           # 中间产物
├── 概念图-v2.png
└── ...

output/<项目名>/            # 最终交付的图片
├── <项目名>-主图-v1.png
├── <项目名>-图标-v1.png
└── ...
```

### 命名原则

- 文件名使用中文或英文皆可，保持清晰可读
- 版本号从 v1 起递增，每次迭代新增文件，不覆盖旧版本
- 场景明确时在文件名中标注用途（如"主图"、"图标"、"banner"）

## 第一步：明确需求（需求分析）

在写 Prompt 之前，先回答以下 5 个核心问题：

### 1.1 用途

图片用在哪里？

| 用途类型 | 示例 |
|---------|------|
| Web 应用/网站 | 首页 Hero 图、Banner、博客配图、404 页面 |
| 小程序 | 启动页、分享卡片、分类图标 |
| 日常做图 | 公众号头图、朋友圈海报、PPT 配图 |
| 小图标 | App Icon、工具栏图标、功能图标 |
| 验证草图 | 概念验证、A/B 测试素材、mood board |

### 1.2 尺寸/比例

根据发布平台选择合适的比例：

| 比例 | 尺寸 | 适用场景 |
|------|------|---------|
| 1:1 | 1024x1024 | 社交媒体头像、Instagram、方形 Banner |
| 16:9 | 1792x1024 | 横屏视频封面、YouTube、B站、网站 Hero |
| 9:16 | 1024x1792 | 竖屏海报、手机壁纸、抖音、小红书 |
| 4:3 | 1536x1152 | 传统屏幕比例、PPT 配图 |
| 3:4 | 1152x1536 | 竖屏海报、公众号头图 |
| 3:2 | 1536x1024 | 摄影比例、博客配图 |
| 2:3 | 1024x1536 | 竖屏摄影、Pinterest |

### 1.3 风格

确定视觉风格方向：

- **写实风格**：photorealistic、hyperrealistic、cinematic
- **插画风格**：flat illustration、vector art、watercolor
- **国风/东方**：Chinese ink painting、shuimo、traditional
- **商业/品牌**：clean corporate、Apple-style minimalism
- **科技/未来**：cyberpunk、futuristic UI、3D render
- **复古/怀旧**：vintage poster、retro illustration、pixel art

### 1.4 主体

图片里有什么？越具体越好：

- 主体对象（人物、物体、场景）
- 动作/状态
- 环境/背景
- 色彩基调

### 1.5 不可缺元素

有没有必须出现的元素：

- 文字内容
- Logo
- 特定人物/品牌元素
- 特定颜色/构图要求

## 第二步：选择模型

根据场景复杂度和需求选择合适的模型：

### 模型速查

```
复杂/品牌 → gpt-image
日常/通用/兜底 → minimax-image
国风/古风/中文书法 → qwen-image
图标/占位/快速验证 → qwen-image-flash
```

### 详细选型参考

完整的场景→模型选型对照表，请参考 [场景模型选型指南](scene-model-selection-guide.md)。

## 第三步：编写 Prompt

### Prompt 黄金公式

```
[主体] + [动作/状态] + [环境/背景] + [风格] + [光线/色调] + [构图] + [画质关键词]
```

### Prompt 模板

**正面 Prompt 模板：**

```
[main subject description],
[action or state],
[environment/background],
[style keywords],
[lighting and color tone],
[composition],
[quality keywords: 8k, ultra-detailed, masterpiece]
```

**负面 Prompt 模板（避免常见翻车）：**

```
ugly, deformed, noxious, bad anatomy, extra limbs,
blurry, low quality, pixelated, watermark, text, signature,
oversaturated, distorted proportions
```

### Prompt 编写原则

1. **具体明确**：用具体名词代替抽象描述
2. **结构清晰**：按公式组织，层次分明
3. **风格统一**：每次只定 1-2 个主风格
4. **比例正确**：通过参数指定，不在 Prompt 中写比例词

详细的 Prompt 编写指南，请参考 [Prompt 编写指南](prompt-writing-guide.md)。

## 第四步：生成图片

### 使用脚本生成

```bash
# 基础生成
python scripts/generate_image.py \
  --prompt "你的 Prompt 内容" \
  --ratio 16:9 \
  --output output/项目名/主图.png

# 指定模型
python scripts/generate_image.py \
  --prompt "你的 Prompt 内容" \
  --provider minimax-image \
  --ratio 1:1 \
  --output output/项目名/图标.png

# 图生图
python scripts/generate_image.py \
  --prompt "转换为水彩风格" \
  --input input/原图.jpg \
  --ratio 1:1 \
  --output output/项目名/水彩版.png
```

### 生成策略

- **批量生成**：同 Prompt 跑 3-5 张，挑最好的
- **多版本对比**：同一主题，换 2-3 种风格跑一遍对比
- **迭代优化**：不满意时调整 Prompt 重新生成

## 第五步：评估质量

### 评估打分表

| 维度 | 1 分 | 3 分 | 5 分 |
|------|------|------|------|
| 主体还原度 | 跑题 | 基本符合 | 1:1 还原 |
| 风格匹配 | 完全不符 | 部分符合 | 100% 命中 |
| 美感 | 丑 | 一般 | 惊艳 |
| 细节 | 模糊 | 清晰 | 8k 细腻 |
| 商业可用 | 没法用 | 需修改 | 直接上线 |

**评估标准：4 分以上才进入下一步，否则换模型或重写 Prompt。**

### 常见质量问题

| 问题 | 可能原因 | 解决方案 |
|------|---------|---------|
| 手画成六指 | 模型对细节手部易崩 | 用 gpt-image；加 "perfect hands, five fingers" |
| 文字鬼画符 | 文字渲染是普遍弱项 | 用 gpt-image 或 qwen-image（中文）；文字用后期合成 |
| 风格飘忽 | Prompt 风格词不精确 | 给风格参考图；用更具体的风格词 |
| 主体跑题 | 描述太抽象 | 加具体名词、颜色、场景 |

## 第六步：迭代优化

### 三板斧

1. **调 Prompt 措辞**：主体描述具体化、加细节
2. **换模型**：同样 Prompt 试不同模型对比
3. **加参考图**：用 image-to-image 功能锁风格

### 迭代记录

每次迭代记录：

```markdown
## 迭代记录

### v1
- Prompt: [原始 Prompt]
- 模型: minimax-image
- 问题: 主体不够突出
- 评分: 3/5

### v2
- Prompt: [优化后 Prompt]
- 模型: minimax-image
- 改进: 增加了主体描述细节
- 评分: 4/5
```

## 第七步：后期处理（可选）

### 常见后期处理

| 处理类型 | 工具建议 | 适用场景 |
|---------|---------|---------|
| 裁切/调比例 | Figma、Photoshop | 适配不同平台 |
| 压缩/转格式 | Squoosh、TinyPNG | Web 性能优化 |
| 打 Logo/水印 | Figma、Canva | 品牌保护 |
| 转矢量 | Illustrator、Vectorizer | 图标类永久清晰 |
| 文字合成 | Figma、Photoshop | 避免 AI 文字鬼画符 |

### 输出格式建议

| 用途 | 推荐格式 | 理由 |
|------|---------|------|
| Web 展示 | WebP、AVIF | 体积小，加载快 |
| 印刷 | PNG、TIFF | 无损，质量高 |
| 社交媒体 | JPEG、PNG | 兼容性好 |
| 图标 | SVG | 矢量，无限缩放 |

## 质量检查清单

### 视觉质量

- [ ] 画面清晰，无模糊
- [ ] 风格一致，符合需求
- [ ] 主体突出，构图合理
- [ ] 色彩协调，光影自然

### 内容质量

- [ ] 主体还原度高
- [ ] 无明显 AI 痕迹
- [ ] 无版权风险元素
- [ ] 商业可用

### 技术质量

- [ ] 分辨率满足需求
- [ ] 文件格式正确
- [ ] 文件大小合理
- [ ] 命名规范

## 常见问题

### Q1: 生成的图片总是不满意

**解决方案**：
- 先用 qwen-image-flash 快速验证 Prompt 方向
- 确认方向后再用目标模型精修
- 参考优秀案例的 Prompt 写法

### Q2: 不同图片风格不统一

**解决方案**：
- 建立"风格种子 Prompt"，统一复用
- 使用同一组风格关键词
- 保存满意的图片作为参考

### Q3: 生成速度太慢

**解决方案**：
- 验证阶段用 qwen-image-flash（快）
- 正式生成用 minimax-image（平衡）
- 只有关键图才用 gpt-image（慢但质量高）

### Q4: 成本太高

**解决方案**：
- 遵循二八原则：80% 用 minimax-image
- 验证阶段用 qwen-image-flash
- 只有 5% 关键图用 gpt-image

## 工具和资源

### 模型服务

| 模型 | 能力档位 | 擅长 | 单次成本 | 速度 |
|------|---------|------|---------|------|
| gpt-image | ⭐⭐⭐⭐⭐ S 级 | 复杂构图、精细文字、影视级美感 | 高 | 慢 |
| minimax-image | ⭐⭐⭐⭐ A 级 | 通用场景、中文理解、性价比 | 中 | 中 |
| qwen-image | ⭐⭐⭐ A-级 | 东方美学、国风水墨、文字渲染 | 中 | 中 |
| qwen-image-flash | ⭐⭐ B 级 | 简单图、图标、占位、验证草图 | 低 | 快 |

### 参考文档

- [场景模型选型指南](scene-model-selection-guide.md)
- [风格指南](style-guide.md)
- [Prompt 编写指南](prompt-writing-guide.md)
- [最佳实践](best-practices.md)
