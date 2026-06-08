# skills

这是一个用于 [skillshare](https://github.com/runkids/skillshare) 的公开 skills 源仓库，供他人通过 HTTPS 匿名只读方式订阅同步。

## 订阅方法

```bash
skillshare init --remote https://github.com/liang9886703/skills.git
skillshare pull        # 首次本地非空时用 skillshare pull --force
```

## 目录结构

本仓库采用 `分类/技能名/SKILL.md` 的二级目录组织，每个 skill 都是一个独立目录，并包含唯一必需文件 `SKILL.md`。

```text
skills/
├── README.md
├── .gitignore
├── frontend/
│   └── react-performance/
│       └── SKILL.md
├── backend/
│   └── python-api-debugging/
│       └── SKILL.md
└── devops/
    └── github-actions-triage/
        └── SKILL.md
```
