# 图像生成最佳实践

## 概述

本文档汇总图像生成过程中的最佳实践，涵盖从需求分析到最终交付的全流程，帮助用户高效、稳定地生成高质量图片。

## 核心原则

### 1. 按场景选模型

```
复杂/品牌 → gpt-image
日常/通用/兜底 → minimax-image
国风/古风/中文书法 → qwen-image
图标/占位/快速验证 → qwen-image-flash
```

### 2. minimax 兜底

80% 的场景用 minimax-image 覆盖，它是日常主力和默认兜底模型。

### 3. 二八原则

```
80% 场景用 minimax-image
15% 场景用 gpt-image 提质
4% 场景用 qwen-image 走东方
1% 场景用 qwen-image-flash 验证
```

### 4. 先验证后精修

用 qwen-image-flash 快速验证 Prompt 方向，确认后再用目标模型精修，能省 60%+ 成本。

## 工作流程最佳实践

### Step 1: 需求分析

在写 Prompt 之前，先明确：

1. **用途**：用在哪里？
2. **尺寸/比例**：1:1、16:9、9:16、3:4？
3. **风格**：写实 / 插画 / 国风 / 极简 / 3D？
4. **主体**：图片里有什么？
5. **不可缺元素**：有没有必须出现的字、logo、人物？

### Step 2: 模型选择

根据场景复杂度选模型：

| 复杂度 | 模型 | 典型场景 |
|-------|------|---------|
| S 级 | gpt-image | 品牌主视觉、营销海报 |
| A 级 | minimax-image | 日常配图、社交媒体 |
| A- 级 | qwen-image | 国风、东方美学 |
| B 级 | qwen-image-flash | 图标、占位、验证 |

### Step 3: Prompt 编写

遵循黄金公式：

```
[主体] + [动作/状态] + [环境/背景] + [风格] + [光线/色调] + [构图] + [画质关键词]
```

**原则**：
- 具体明确，用具体名词
- 结构清晰，按公式组织
- 风格统一，1-2 个主风格
- 比例通过参数，不写入 Prompt

### Step 4: 生成策略

- **批量生成**：同 Prompt 跑 3-5 张，挑最好的
- **多版本对比**：同一主题，换 2-3 种风格跑一遍对比
- **固定种子**：满意结果保留种子便于复现

### Step 5: 质量评估

使用评估打分表：

| 维度 | 1 分 | 3 分 | 5 分 |
|------|------|------|------|
| 主体还原度 | 跑题 | 基本符合 | 1:1 还原 |
| 风格匹配 | 完全不符 | 部分符合 | 100% 命中 |
| 美感 | 丑 | 一般 | 惊艳 |
| 细节 | 模糊 | 清晰 | 8k 细腻 |
| 商业可用 | 没法用 | 需修改 | 直接上线 |

**标准：4 分以上才进入下一步，否则换模型或重写 Prompt。**

### Step 6: 迭代优化

三板斧：

1. **调 Prompt 措辞**：主体描述具体化、加细节
2. **换模型**：同样 Prompt 试不同模型对比
3. **加参考图**：用 image-to-image 功能锁风格

### Step 7: 后期处理

- **裁切/调比例**：适配不同平台
- **压缩/转格式**：WebP/AVIF 省流量
- **打 Logo/水印**：品牌保护
- **转矢量**：图标类永久清晰

## Prompt 编写最佳实践

### 1. 具体明确

**❌ 错误**：
```
A beautiful landscape
```

**✅ 正确**：
```
A serene mountain lake at sunrise,
snow-capped peaks reflected in crystal clear water,
pine forest on the shoreline,
golden morning light,
landscape photography, 8k
```

### 2. 结构清晰

**❌ 错误**：
```
cat cute sitting window sun warm
```

**✅ 正确**：
```
A cute orange tabby cat,
sitting on a windowsill,
basking in warm sunlight,
cozy home interior,
soft natural lighting,
photorealistic, 8k
```

### 3. 风格统一

**❌ 错误**：
```
A cat, photorealistic, cartoon, watercolor,
oil painting, digital art, minimalist, detailed
```

**✅ 正确**：
```
A cute cat,
flat illustration style,
pastel colors,
clean background,
modern design
```

### 4. 比例正确

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

### 5. 画质关键词

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

## 常见翻车与避坑

### 模型层面

| 翻车 | 原因 | 解决方案 |
|------|------|---------|
| 手画成六指 | 模型对细节手部易崩 | 用 gpt-image；加 "perfect hands, five fingers" |
| 文字鬼画符 | 文字渲染是普遍弱项 | 用 gpt-image 或 qwen-image（中文）；文字用后期合成 |
| 多人物关系混乱 | 主体越多越崩 | 控制主体 ≤ 2 个；或拆成多张合成 |
| 国风不像 | 西方模型对东方美学理解弱 | 切 qwen-image |
| 风格飘忽 | Prompt 风格词不精确 | 给风格参考图；用更具体的风格词 |

### Prompt 层面

| 翻车 | 原因 | 解决方案 |
|------|------|---------|
| 跑题 | 主体描述太抽象 | 加具体名词、颜色、场景 |
| 风格混乱 | 同时塞太多风格词 | 每次只定 1-2 个主风格 |
| 比例不对 | 没指定 aspect ratio | 显式声明 --ratio 16:9 |
| 元素缺失 | 重要东西没强调 | 用括号强调 (must include: logo) |

### 业务层面

| 翻车 | 原因 | 解决方案 |
|------|------|---------|
| AI 痕迹太重 | 风格太"标准 AI" | 加胶片颗粒、不完美质感词 |
| 版权风险 | 风格撞名画家 | 避免 "in the style of [living artist]" |
| 主体像真人 | 肖像权风险 | 虚构描述、加 "fictional character" |
| 批量风格不统一 | 每次 Prompt 漂移 | 提取"风格种子 Prompt" 复用 |

## 成本控制最佳实践

### 1. 分级使用

```
gpt-image：5% 关键图（品牌主视觉、营销海报）
minimax-image：80% 日常（配图、社交媒体、博客）
qwen-image：4% 国风（东方美学、中文海报）
qwen-image-flash：1% 验证（图标、占位、草图）
```

### 2. 先验证后精修

```python
# 流程
1. 用 qwen-image-flash 快速验证 Prompt 方向
2. 确认方向后，用目标模型精修
3. 能省 60%+ 成本
```

### 3. 批量对比

```python
# 策略
1. 同一主题，跑 3-5 张
2. 多模型对比，选出最优
3. 避免单次生成不满意反复重试
```

### 4. 缓存复用

```python
# 优化
1. 相同 Prompt 命中缓存，省 token
2. 建立 Prompt 库，复用验证过的 Prompt
3. 避免重复生成相同内容
```

### 5. 成本监控

```python
# 措施
1. 设置每用户/每日上限
2. 监控各模型使用量
3. 及时调整策略
```

## 团队协作最佳实践

### 1. 建立 Prompt 库

- 把验证过的好 Prompt 沉淀下来
- 标签化管理（场景、风格、模型）
- 团队共享，提高效率

### 2. 统一风格词表

- 用同一份"风格关键词表"
- 保证多人生成风格统一
- 避免风格漂移

### 3. 案例库

- 把团队满意的图存起来
- 作为下次 reference
- 标注使用的 Prompt 和模型

### 4. A/B 测试

- 同主题 3 种风格对比
- 数据说话，选出最优
- 避免主观判断

## 自动化最佳实践

### 1. 批量生成脚本

```bash
# 一次生成多张对比
python scripts/generate_image.py \
  --prompt "你的 Prompt" \
  --n 5 \
  --output output/项目名/对比_{n}.png
```

### 2. 自动裁切

- 上传时按目标位置自动裁切不同比例
- 避免手动裁切
- 提高效率

### 3. CDN 缓存

- 相同 Prompt 命中缓存
- 省 token
- 加快响应

### 4. 尺寸预设

- 为每个场景预设尺寸
- 避免每次手填
- 减少错误

## 质量保证最佳实践

### 1. 评估打分

每次生成后评估：

| 维度 | 评分标准 |
|------|---------|
| 主体还原度 | 是否符合需求 |
| 风格匹配 | 是否符合预期风格 |
| 美感 | 视觉效果如何 |
| 细节 | 清晰度和细节程度 |
| 商业可用 | 能否直接使用 |

### 2. 迭代优化

```
生成 → 评估 → 优化 → 生成 → 评估 → ...
```

直到评分 ≥ 4 分。

### 3. 多版本对比

- 同一主题，多模型对比
- 同一模型，多 Prompt 对比
- 选出最优方案

### 4. 团队评审

- 关键图片团队评审
- 避免个人主观判断
- 集体决策

## 版权与合规最佳实践

### 1. 避免版权风险

**❌ 错误**：
```
A painting in the style of Picasso
```

**✅ 正确**：
```
A cubist style painting,
geometric shapes, bold colors,
abstract composition
```

**原则**：避免使用在世艺术家的名字。

### 2. 虚构人物

**❌ 错误**：
```
A portrait of [真实人物名]
```

**✅ 正确**：
```
A portrait of a young professional,
fictional character,
professional headshot
```

**原则**：使用虚构描述，避免肖像权问题。

### 3. 商用授权

- 确认生成图片的商用授权
- 避免使用有版权限制的风格
- 保留生成记录

### 4. 内容审核

- 避免生成敏感内容
- 遵守平台内容政策
- 建立审核流程

## 复盘 Checklist

每个项目跑完问自己：

- [ ] 是否建立了 Prompt 库？
- [ ] 是否记录了"哪个模型擅长什么场景"？
- [ ] 是否有兜底机制？
- [ ] 是否有成本监控？
- [ ] 是否有版权审核流程？
- [ ] 是否给团队做过 Prompt 培训？
- [ ] 是否有质量评估流程？
- [ ] 是否有迭代优化记录？

## 工具与资源

### 模型服务

| 模型 | 能力 | 成本 | 速度 | 主用场景 |
|------|------|------|------|---------|
| gpt-image | S 级 | 高 | 慢 | 品牌、营销 |
| minimax-image | A 级 | 中 | 中 | 日常主力 |
| qwen-image | A- 级 | 中 | 中 | 国风专属 |
| qwen-image-flash | B 级 | 低 | 快 | 验证、占位 |

### 参考文档

- [图片创建完整流程](image-creation-workflow.md)
- [场景模型选型指南](scene-model-selection-guide.md)
- [风格指南](style-guide.md)
- [Prompt 编写指南](prompt-writing-guide.md)

## 总结

- **按场景选模型**：复杂才用 gpt-image，日常全靠 minimax 兜底
- **Prompt 要写好**：具体 + 结构 + 统一 + 迭代
- **成本要控制**：二八原则，先验证后精修
- **质量要保证**：评估打分，迭代优化
- **团队要协作**：Prompt 库、风格词表、案例库
- **版权要注意**：避免风险，合规使用

**一句话：按场景选模型，Prompt 写具体，成本要控制，质量要保证。**
