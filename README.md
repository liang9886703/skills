# skills

这是一个用于 [skillshare](https://github.com/runkids/skillshare) 的公开 skills 源仓库，供他人通过 HTTPS 匿名只读方式订阅同步。

## 订阅方法

```bash
skillshare init --remote https://github.com/liang9886703/skills.git
skillshare pull        # 首次本地非空时用 skillshare pull --force
```

## 目录结构

本仓库采用 `分类/技能名` 的二级目录组织，每个 skill 都是一个独立目录，包含唯一必需文件 `SKILL.md`。

分类统一使用英文 kebab-case：

| 分类 | 中文描述 | 说明 |
|------|-------|------|
| `code-reading` | 代码阅读 | 代码分析、理解和追踪相关技能 |
| `data-visualization` | 图表与可视化 | 数据可视化和图表生成技能 |
| `documentation-writing` | 文档编写 | 技术文档和说明文档编写 |
| `feature-development` | 功能开发 | 功能实现和开发相关技能 |
| `frontend-development` | 前端开发 | 前端框架和组件开发 |
| `information-search` | 信息搜索 | 信息查询和搜索相关技能 |
| `meta-skills` | 元能力 | 通用工具和流程自动化 |
| `script-development` | 脚本开发 | 脚本编写和自动化 |
| `other` | 其他 | 其他技能 |

## Skills 索引

详见 [SKILLS_INDEX.md](./SKILLS_INDEX.md) 获取完整的 skills 列表和描述。

## 目录树示例

```text
skills/
├── README.md
├── SKILLS_INDEX.md
├── LICENSE
├── .gitignore
├── code-reading/
│   ├── zeno-codex/
│   │   └── SKILL.md
│   └── graphify/
│       └── SKILL.md
├── data-visualization/
├── documentation-writing/
├── feature-development/
├── frontend-development/
├── information-search/
├── meta-skills/
├── script-development/
└── other/
```

## 技术栈

![Python](https://img.shields.io/badge/Python-74.5%25-blue)
![HTML](https://img.shields.io/badge/HTML-13.9%25-orange)
![JavaScript](https://img.shields.io/badge/JavaScript-7.9%25-yellow)
![Shell](https://img.shields.io/badge/Shell-3.5%25-green)
![PLpgSQL](https://img.shields.io/badge/PLpgSQL-0.2%25-lightgrey)

## 许可证

本仓库采用 MIT License，详见 [LICENSE](./LICENSE) 文件。

---

**提示**: 这是一个活跃的 skills 仓库，欢迎通过 Fork 和 Pull Request 来贡献新的 skills！
