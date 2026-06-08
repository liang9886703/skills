---
name: github-actions-triage
description: >-
  提供 GitHub Actions 失败诊断流程，在用户提到 CI 红灯、workflow failed、构建失败等关键词时触发。
# 可选字段：
# targets: [claude, cursor]
# license: MIT
# allowed-tools: "Bash(python:*) WebFetch"
# metadata:
#   author: liang9886703
#   version: 1.0.0
---

# GitHub Actions 故障分诊
用于快速识别 CI 失败根因并给出最小修复路径。

## When to Use
- 用户说 "CI 挂了" 时使用
- 不适用于 与代码仓库无关的外部服务全局故障

## Instructions
### Step 1: 确认失败 workflow、job 与首个报错点
### Step 2: 按依赖、环境、测试失败三类定位根因
### Step 3: 验证结果

## Examples
**Example:** PR 检查状态为失败
User: "这个 workflow failed，帮我看下"
Actions: 1. 获取失败 job 日志 2. 修复配置或代码并重跑验证
Result: workflow 恢复通过，PR 状态转绿

## Troubleshooting
**Error:** 日志信息不足 / **Cause:** 日志被截断或步骤缺少输出 / **Solution:** 提高日志级别并增加关键步骤输出
