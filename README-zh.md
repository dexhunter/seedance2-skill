# Seedance 2.0 视频提示词撰写技能

[English](README.md)

为[即梦 Seedance 2.0](https://jimeng.jianying.com/) 多模态 AI 视频生成模型打造的 [Agent Skills](https://agentskills.io) 提示词撰写技能。支持 Claude Code、Cursor、Cline 等兼容的 AI 代理。

涵盖输入约束、@ 引用语法、运镜语言、提示词结构模式，以及广告、短剧、MV、科普教育等场景的现成模版。

## 安装

### 方式 A：手动复制（推荐）

克隆或下载本仓库，然后将技能文件复制到 Claude skills 目录：

```bash
mkdir -p ~/.claude/skills

# 中文版
cp zh/SKILL.md ~/.claude/skills/seedance-prompt-zh.md

# 英文版
cp SKILL.md ~/.claude/skills/seedance-prompt-en.md
```

### 方式 B：通过 skills CLI

```bash
npx skills add dexhunter/seedance2-skill
```

然后让你的 AI 代理帮你撰写 Seedance 2.0 视频提示词即可。

## 技能文件

| 文件 | 语言 | 说明 |
|---|---|---|
| [SKILL.md](SKILL.md) | English | Prompt writing guide for Seedance 2.0 |
| [zh/SKILL.md](zh/SKILL.md) | 中文 | Seedance 2.0 提示词撰写指南 |

## 资料来源

基于字节跳动官方文档整理：

- [即梦 Seedance 2.0 使用手册](https://bytedance.larkoffice.com/wiki/A5RHwWhoBiOnjukIIw6cu5ybnXQ) — 参数说明、交互方式、多模态能力与示例提示词
- [小云雀 Seedance 2.0 实测案例](https://bytedance.larkoffice.com/wiki/LJXzwehluiFdzKkb1recZdfonZg) — 剧情制作、电商广告、舞蹈模仿、科普教学、AI MV 等场景

## 许可证

[MIT](LICENSE)
