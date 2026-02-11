# Seedance 2.0 视频提示词撰写技能

[English](README.md)

为[即梦 Seedance 2.0](https://jimeng.jianying.com/) 多模态 AI 视频生成模型打造的 Claude Code 提示词撰写技能。

## 技能文件

| 文件 | 语言 | 说明 |
|---|---|---|
| [SKILL-en.md](SKILL-en.md) | English | Prompt writing guide for Seedance 2.0 |
| [SKILL-zh.md](SKILL-zh.md) | 中文 | Seedance 2.0 提示词撰写指南 |

两个版本内容一致，涵盖：输入约束、@ 引用语法、运镜语言、提示词结构模式，以及广告、短剧、MV、科普教育等场景的现成模版。

## 资料来源

本技能基于以下官方文档整理：

- [即梦 Seedance 2.0 使用手册（全新多模态创作体验）](https://bytedance.larkoffice.com/wiki/A5RHwWhoBiOnjukIIw6cu5ybnXQ) — 官方使用手册，涵盖参数说明、交互方式、多模态能力与示例提示词
- [小云雀 Seedance 2.0 实测案例](https://bytedance.larkoffice.com/wiki/LJXzwehluiFdzKkb1recZdfonZg) — 实测案例集，涵盖剧情制作、电商广告、舞蹈模仿、科普教学、AI MV 等场景

## 使用方法

将你需要的语言版本复制到用户级技能目录：

```bash
mkdir -p ~/.claude/skills

# 中文版
cp SKILL-zh.md ~/.claude/skills/

# 英文版
cp SKILL-en.md ~/.claude/skills/
```

然后在 Claude Code 中让它帮你撰写 Seedance 2.0 视频提示词即可。

## 技能格式

本技能遵循 [Anthropic Skill Creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) 规范，使用 YAML frontmatter（`name` + `description`）和 Markdown 正文。

## 许可证

[MIT](LICENSE)
