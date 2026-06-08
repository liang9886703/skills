# Skills 索引

本文件提供了所有可用 skills 的详细索引和描述。

## 📑 目录

- [代码阅读 (code-reading)](#代码阅读-code-reading)
- [功能开发 (feature-development)](#功能开发-feature-development)
- [前端开发 (frontend-development)](#前端开发-frontend-development)
- [元能力 (meta-skills)](#元能力-meta-skills)
- [计划中的分类](#计划中的分类)

---

## 代码阅读 (code-reading)

用于深度代码分析、理解复杂项目结构和追踪代码流向的技能。

### zeno-codex

**描述**: 递归分解的代码库分析工具，用于在不加载整个代码库的情况下进行深度分析

**主要特性**:
- 🔍 **证据优先**: 每个结论都附带文件和行号引用
- ♻️ **递归分解**: 将大问题分解为可审计的小查询
- 🎯 **确定性检索**: 通过 JSONL REPL 操作保持上下文精简和可复现
- 📊 **多种模式支持**: 代码考古、安全审计、架构映射、PR评审、技能生成、深度研究

**适用场景**:
- 大型仓库（数百或数千个文件）的代码分析
- 长日志或追踪的关键行提取
- 安全审计和并发问题检查
- 需要可复现且有证据支撑的分析

**位置**: `code-reading/zeno-codex/SKILL.md`

**相关资源**:
- 📚 完整文档: [zeno-codex/README.md](./code-reading/zeno-codex/README.md)
- 🛠️ 脚本工具: `scripts/` 目录下的各种辅助脚本
- 📖 参考文档: `references/` 目录下的协议、数据模型和安全指南

---

### graphify

**描述**: 代码结构可视化和分析工具，用于生成代码依赖图和结构可视化

**主要特性**:
- 🌳 **树形结构解析**: 支持多种编程语言的语法树解析
- 📡 **依赖关系映射**: 自动分析和可视化代码依赖
- 🔗 **多格式支持**: 支持代码、文档、视频等多种格式分析
- 📦 **离线安装**: 提供预编译的 wheel 包，支持完全离线安装

**适用场景**:
- 快速了解代码库的整体结构
- 分析模块间的依赖关系
- 生成项目的可视化文档
- 支持多语言项目的代码分析

**位置**: `code-reading/graphify/SKILL.md`

**相关资源**:
- 🔧 安装说明: [graphify/scripts/README.md](./code-reading/graphify/scripts/README.md)
- 📦 离线包: `packages/graphifyy-0.5.0+baidu1-py3-none-any.whl`

---

## 功能开发 (feature-development)

针对具体功能实现和开发工作流的技能。

### python-api-debugging

**描述**: Python API 调试和问题诊断技能，用于快速定位和解决 API 相关问题

**主要特性**:
- 🐛 **快速诊断**: 系统化的问题排查流程
- 📋 **调试清单**: 完整的检查项目和常见问题
- 🔧 **实战工具**: 调试脚本和工具示例
- 📚 **最佳实践**: API 设计和测试最佳实践

**适用场景**:
- 解决 Python API 的运行时错误
- 性能瓶颈分析和优化
- 集成测试失败的排查
- API 兼容性问题诊断

**位置**: `feature-development/python-api-debugging/SKILL.md`

---

## 前端开发 (frontend-development)

前端框架和组件优化相关的技能。

### react-performance

**描述**: React 应用性能优化技能，涵盖渲染优化、内存管理和性能监测

**主要特性**:
- ⚡ **渲染优化**: 减少不必要的重新渲染
- 🧠 **内存管理**: 防止内存泄漏和优化内存使用
- 📊 **性能监测**: 使用工具监测和分析性能指标
- 🎯 **最佳实践**: React 性能优化的实战建议

**适用场景**:
- 优化 React 应用的加载时间
- 减少运行时的性能瓶颈
- 提升用户交互体验
- 大型 React 项目的性能审查

**位置**: `frontend-development/react-performance/SKILL.md`

---

## 元能力 (meta-skills)

通用工具和流程自动化相关的技能。

### github-actions-triage

**描述**: GitHub Actions 工作流分类和自动化技能，用于管理和优化 CI/CD 流程

**主要特性**:
- 🤖 **工作流自动化**: 自动化 GitHub Actions 配置和管理
- 📌 **问题分类**: 自动分类和标记 issue 和 PR
- 🔍 **日志分析**: 快速定位失败的工作流
- 🏗️ **流程优化**: 优化 CI/CD 管道和构建流程

**适用场景**:
- 自动化 issue 和 PR 的分类标记
- 监控和优化 CI/CD 流程
- 减少手动维护工作
- 提高工程效率

**位置**: `meta-skills/github-actions-triage/SKILL.md`

---

## 计划中的分类

以下分类已建立但暂无 skills：

### 📊 data-visualization (图表与可视化)
计划添加数据可视化、图表生成相关的 skills。

### 📝 documentation-writing (文档编写)
计划添加技术文档、说明文档编写相关的 skills。

### 🔎 information-search (信息搜索)
计划添加信息查询、搜索和数据采集相关的 skills。

### 🔨 script-development (脚本开发)
计划添加脚本编写、任务自动化相关的 skills。

### 📦 other (其他)
用于分类的其他 skills。

---

## 快速开始

### 1. 查看 SKILL.md

每个 skill 都包含一个 `SKILL.md` 文件，记录了该 skill 的详细说明、用法和示例。

```bash
# 例如查看 zeno-codex 的详细文档
cat code-reading/zeno-codex/SKILL.md
```

### 2. 订阅和使用

```bash
# 订阅此 skills 仓库
skillshare init --remote https://github.com/liang9886703/skills.git

# 列出所有可用的 skills
skillshare list

# 加载特定的 skill
skillshare load zeno-codex
```

### 3. 贡献新的 Skill

如果你想贡献新的 skill：

1. Fork 此仓库
2. 在适当的分类目录下创建新目录
3. 在新目录中添加 `SKILL.md` 文件
4. 更新本 `SKILLS_INDEX.md` 文件
5. 提交 Pull Request

---

## 许可证

所有 skills 采用 MIT License，详见 [LICENSE](./LICENSE) 文件。

---

**最后更新**: 2026-06-08

如有问题或建议，欢迎提交 Issue 或 Pull Request！
