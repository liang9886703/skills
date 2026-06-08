# skills

这是一个用于 [skillshare](https://github.com/runkids/skillshare) 的公开 skills 源仓库，供他人通过 HTTPS 匿名只读方式订阅同步。

## 订阅方法

```bash
skillshare init --remote https://github.com/liang9886703/skills.git
skillshare pull        # 首次本地非空时用 skillshare pull --force
```

## 目录结构

本仓库采用 `分类/技能名/SKILL.md` 的二级目录组织，每个 skill 都是一个独立目录，并包含唯一必需文件 `SKILL.md`。

分类统一使用英文 kebab-case：

- `data-visualization`（图表与可视化）
- `documentation-writing`（文档编写）
- `information-search`（信息搜索）
- `meta-skills`（元能力）
- `code-reading`（代码阅读）
- `feature-development`（功能开发）
- `script-development`（脚本开发）
- `frontend-development`（前端开发）
- `other`（其他）

```text
skills/
├── README.md
├── .gitignore
├── data-visualization/
│   └── .gitkeep
├── documentation-writing/
│   └── .gitkeep
├── information-search/
│   └── .gitkeep
├── meta-skills/
│   └── github-actions-triage/
│       └── SKILL.md
├── code-reading/
│   └── .gitkeep
├── feature-development/
│   └── python-api-debugging/
│       └── SKILL.md
├── script-development/
│   └── .gitkeep
├── frontend-development/
│   └── react-performance/
│       └── SKILL.md
└── other/
    └── .gitkeep
```
