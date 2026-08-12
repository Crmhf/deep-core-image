# 场景模型选型指南

## 概述

本文档提供不同场景下的模型选择建议，帮助用户根据具体需求选择最合适的图像生成模型。核心原则：**按场景复杂度选模型，minimax 兜底**。

## 四个模型速览

| 模型 | 能力档位 | 擅长 | 单次成本 | 速度 | 主用场景 |
|------|---------|------|---------|------|---------|
| **gpt-image** | ⭐⭐⭐⭐⭐ S 级 | 复杂构图、多主体、精细文字、长 prompt 还原、影视级美感 | 高 | 慢 | 营销主图、复杂海报、品牌视觉 |
| **minimax-image** | ⭐⭐⭐⭐ A 级 | 通用场景、中文理解、性价比、风格覆盖广 | 中 | 中 | **日常主力、兜底模型** |
| **qwen-image** | ⭐⭐⭐ A-级 | 东方美学、国风水墨、中文古风、文字渲染 | 中 | 中 | 国风、中文海报、传统题材 |
| **qwen-image-flash** | ⭐⭐ B 级 | 简单图、图标、占位、验证草图 | 低 | 快 | 图标、占位、迭代验证 |

## 选型速查（一行版）

```
复杂/品牌 → gpt-image
日常/通用/兜底 → minimax-image
国风/古风/中文书法 → qwen-image
图标/占位/快速验证 → qwen-image-flash
```

## 场景 → 模型选型对照表

### Web 应用 / 网站

| 场景 | 推荐模型 | 理由 |
|------|---------|------|
| 首页 Hero 大图 / 主视觉 | `gpt-image` | 视觉冲击、细节、光影、构图都要顶 |
| 营销 Landing Page 主图 | `gpt-image` | 转化率敏感，质感不能拉 |
| Banner / 活动图 | `minimax-image` | 通用场景稳定，够用且快 |
| 博客 / 文章配图 | `minimax-image` | 内容型，够用即可 |
| 404 / 占位插画 | `minimax-image` 或 `qwen-image-flash` | 不重要，快就行 |
| 头像 / 团队成员照（风格化） | `minimax-image` | 中等复杂度，效果稳定 |
| 插画 / 空状态插图 | `minimax-image` | 风格化插画稳定 |
| 网站 favicon / 导航图标 | `qwen-image-flash` | 简单矢量感，快速迭代 |

### 小程序

| 场景 | 推荐模型 | 理由 |
|------|---------|------|
| 启动页 / 首屏 | `gpt-image` | 第一印象关键 |
| 分享卡片封面 | `minimax-image` | 微信生态分享够用 |
| 分类图标 / 导航 | `qwen-image-flash` | 简单小图标 |
| 营销活动弹窗图 | `minimax-image` | 平衡质量和成本 |
| 会员卡 / 勋章 / 成就图标 | `qwen-image` | 风格化装饰，东方审美加分 |
| 错误页 / 加载占位 | `qwen-image-flash` | 快即可 |

### 日常做图（内容运营 / 自媒体 / 演示）

| 场景 | 推荐模型 | 理由 |
|------|---------|------|
| 公众号 / 知乎 / 小红书头图 | `gpt-image` | 流量入口，质感要顶 |
| 朋友圈海报 | `gpt-image` 或 `minimax-image` | 看预算 |
| 演示文稿封面 | `minimax-image` | 平衡 |
| 表情包 | `minimax-image` | 风格化够用 |
| 配图（阅读量驱动） | `minimax-image` | 性价比 |
| PPT 配图 | `minimax-image` | 通用稳定 |

### 小图标 / 验证类

| 场景 | 推荐模型 | 理由 |
|------|---------|------|
| 应用图标（App Icon） | `gpt-image` 或 `minimax-image` | 复杂图形需要细节 |
| 工具栏小图标 | `qwen-image-flash` | 简单 |
| 业务功能图标（16-64px） | `qwen-image-flash` | 快速迭代 |
| 验证 prompt 想法（草图） | `qwen-image-flash` | 速度优先，不在意细节 |
| 概念图 / mood board | `qwen-image-flash` 或 `minimax-image` | 看精度需求 |
| A/B 测试素材（多版本） | `qwen-image-flash` | 量大，成本低 |

## 按复杂度分级选型

### S 级复杂度（用 gpt-image）

**特征**：
- 多主体交互
- 精细文字渲染
- 复杂构图和光影
- 品牌级视觉要求
- 长 Prompt 还原

**典型场景**：
- 品牌主视觉
- 营销海报
- 复杂信息图
- 影视级概念图

**Prompt 示例**：
```
A professional marketing hero banner for a tech startup,
featuring a diverse team of 5 people collaborating around a futuristic holographic display,
modern office environment with floor-to-ceiling windows showing city skyline,
cinematic lighting with warm golden hour tones,
dynamic composition with depth,
8k ultra-detailed, photorealistic, professional photography
```

### A 级复杂度（用 minimax-image）

**特征**：
- 单主体或简单多主体
- 通用场景
- 中等细节要求
- 性价比优先

**典型场景**：
- 博客配图
- 社交媒体封面
- 产品展示
- 风格化插画

**Prompt 示例**：
```
A cozy coffee shop scene,
warm ambient lighting,
flat illustration style,
soft pastel colors,
clean composition,
professional quality
```

### A- 级复杂度（用 qwen-image）

**特征**：
- 东方美学/国风主题
- 中文文字渲染
- 传统文化元素
- 水墨/书法风格

**典型场景**：
- 国风海报
- 中文标题图
- 传统节日配图
- 文化类内容

**Prompt 示例**：
```
山水之间，一位隐士独坐亭中，
中国传统水墨画风格，
shuimo ink wash painting,
muted earthy tones,
vertical scroll composition,
subtle red seal stamp,
Song Dynasty aesthetic
```

### B 级复杂度（用 qwen-image-flash）

**特征**：
- 简单图形
- 快速迭代
- 成本敏感
- 占位/验证用途

**典型场景**：
- 占位图
- 草图验证
- 简单图标
- A/B 测试素材

**Prompt 示例**：
```
simple flat icon of a house,
minimal design,
solid white background,
clean lines,
vector art style
```

## 兜底策略

### 三层兜底架构

```
第一选择: 按场景选最优模型
   ↓ 失败 / 超时 / 限流
第二选择: minimax-image（几乎所有场景都覆盖）
   ↓ 失败
第三选择: qwen-image-flash（快速简单图）
   ↓ 失败
最终: 返回本地占位图 / 错误占位
```

### 代码层兜底伪代码

```python
def generate_image(prompt, scene):
    models_priority = {
        "marketing":  ["gpt-image", "minimax-image", "qwen-image-flash"],
        "blog":       ["minimax-image", "gpt-image", "qwen-image-flash"],
        "icon":       ["qwen-image-flash", "minimax-image"],
        "chinese":    ["qwen-image", "minimax-image", "gpt-image"],
        "default":    ["minimax-image", "qwen-image-flash", "gpt-image"],
    }

    for model in models_priority.get(scene, models_priority["default"]):
        try:
            return call_model(model, prompt, timeout=30)
        except (RateLimitError, TimeoutError, ModelError):
            continue  # 试下一个

    return get_placeholder_image()  # 本地兜底
```

## 成本控制建议

### 二八原则

```
80% 场景用 minimax-image 兜底
15% 场景用 gpt-image 提质
4% 场景用 qwen-image 走东方
1% 场景用 qwen-image-flash 验证
```

### 成本优化策略

1. **先验证后精修**：用 qwen-image-flash 快速验证方向，确认后再用目标模型
2. **批量对比**：同一主题多模型对比，选出最优
3. **缓存复用**：相同 Prompt 命中缓存，省 token
4. **分级使用**：关键图用 S 级，普通图用 A 级，占位用 B 级

### 成本控制兜底

- **gpt-image 用在最关键处**：5% 的关键图用 S 级
- **minimax-image 承担 80% 日常**
- **qwen-image-flash 用于验证和图标**
- **设置每用户/每日上限**，防止单点刷爆

## 模型切换策略

### 何时切换模型

| 情况 | 建议 |
|------|------|
| 当前模型质量不达标 | 升级到更高档位模型 |
| 生成速度太慢 | 降级到更快模型 |
| 成本超预算 | 批量使用更低档位模型 |
| 特定风格不擅长 | 切换到擅长该风格的模型 |

### 切换示例

**场景 1：minimax-image 生成的国风图不够地道**
```
原模型: minimax-image
问题: 国风元素不够纯正
解决: 切换到 qwen-image
```

**场景 2：gpt-image 生成简单图标太慢**
```
原模型: gpt-image
问题: 简单图标不需要 S 级质量
解决: 切换到 qwen-image-flash
```

**场景 3：qwen-image-flash 生成的营销图质量不够**
```
原模型: qwen-image-flash
问题: 营销图需要更高质量
解决: 升级到 minimax-image 或 gpt-image
```

## 快速决策流程图

```
开始
  ↓
图片用途是什么？
  ├─ 品牌/营销关键图 → gpt-image
  ├─ 国风/东方美学 → qwen-image
  ├─ 简单图标/占位 → qwen-image-flash
  └─ 其他/不确定 → minimax-image
  ↓
生成并评估
  ↓
质量满意？
  ├─ 是 → 输出
  └─ 否 → 升级模型或优化 Prompt
```

## 总结

- **gpt-image**：关键时刻用，质量最高，成本最高，速度最慢
- **minimax-image**：日常主力，性价比最高，覆盖面最广，**默认兜底**
- **qwen-image**：国风专属，东方美学强项，中文文字渲染好
- **qwen-image-flash**：快速验证，成本最低，速度最快，占位专用

**一句话：按场景选模型，复杂才用 gpt-image，日常全靠 minimax 兜底，国风找 qwen，图标/验证用 qwen-flash。**
