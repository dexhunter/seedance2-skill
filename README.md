# Seedance 2.0 Prompt Writing Skills

[中文点我](README-zh.md)

Claude Code skills for writing effective video generation prompts for [Jimeng Seedance 2.0](https://jimeng.jianying.com/), ByteDance's multimodal AI video generation model.

## Skills

| File | Language | Description |
|---|---|---|
| [SKILL-en.md](SKILL-en.md) | English | Prompt writing guide for Seedance 2.0 |
| [SKILL-zh.md](SKILL-zh.md) | Chinese | Seedance 2.0 提示词撰写指南 |

Both versions cover the same content: input constraints, @ reference syntax, camera language, prompt structure patterns, and ready-to-use templates for ads, dramas, MVs, educational content, and more.

## Sources

These skills are based on the following official documents:

- [即梦 Seedance 2.0 使用手册（全新多模态创作体验）](https://bytedance.larkoffice.com/wiki/A5RHwWhoBiOnjukIIw6cu5ybnXQ) — Official user manual covering parameters, interaction methods, multimodal capabilities, and example prompts
- [小云雀 Seedance 2.0 实测案例](https://bytedance.larkoffice.com/wiki/LJXzwehluiFdzKkb1recZdfonZg) — Real-world test cases across drama production, e-commerce ads, dance imitation, science education, AI MVs, and more

## Usage

Copy your preferred language version to the user-level skills directory:

```bash
mkdir -p ~/.claude/skills

# English
cp SKILL-en.md ~/.claude/skills/

# Chinese
cp SKILL-zh.md ~/.claude/skills/
```

Then ask Claude Code to help you write a Seedance 2.0 video prompt.

## Skill Format

These skills follow the [Anthropic Skill Creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) format with YAML frontmatter (`name` + `description`) and markdown body.

## License

[MIT](LICENSE)
