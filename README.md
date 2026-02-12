# Seedance 2.0 Prompt Writing Skills

[中文](README-zh.md)

[Agent skills](https://agentskills.io) for writing effective video generation prompts for [Jimeng Seedance 2.0](https://jimeng.jianying.com/), ByteDance's multimodal AI video generation model. Works with Claude Code, Cursor, Cline, and other compatible agents.

Covers input constraints, @ reference syntax, camera language, prompt structure patterns, and ready-to-use templates for ads, dramas, MVs, educational content, and more.

## Install

**One command** (via [skills.sh](https://skills.sh/)):

```bash
npx skills add dexhunter/seedance2-skill
```

**Or manually:**

```bash
# English
curl -o ~/.claude/skills/seedance-prompt-en.md https://raw.githubusercontent.com/dexhunter/seedance2-skill/main/SKILL.md

# Chinese
curl -o ~/.claude/skills/seedance-prompt-zh.md https://raw.githubusercontent.com/dexhunter/seedance2-skill/main/zh/SKILL.md
```

Then ask your AI agent to help you write a Seedance 2.0 video prompt.

## Skills

| File | Language | Description |
|---|---|---|
| [SKILL.md](SKILL.md) | English | Prompt writing guide for Seedance 2.0 |
| [zh/SKILL.md](zh/SKILL.md) | 中文 | Seedance 2.0 提示词撰写指南 |

## Sources

Based on official ByteDance documentation:

- [Seedance 2.0 User Manual](https://bytedance.larkoffice.com/wiki/A5RHwWhoBiOnjukIIw6cu5ybnXQ) — Parameters, interaction methods, multimodal capabilities, and example prompts
- [Seedance 2.0 Real-world Cases](https://bytedance.larkoffice.com/wiki/LJXzwehluiFdzKkb1recZdfonZg) — Drama production, e-commerce ads, dance imitation, science education, AI MVs, and more

## License

[MIT](LICENSE)
