---
name: react-performance
description: >-
  提供 React 页面性能优化排查步骤，在用户提到卡顿、首屏慢、重渲染等关键词时触发。
# 可选字段：
# targets: [claude, cursor]
# license: MIT
# allowed-tools: "Bash(python:*) WebFetch"
# metadata:
#   author: liang9886703
#   version: 1.0.0
---

# React 性能优化
通过结构化排查快速定位 React 页面卡顿与渲染开销问题。

## When to Use
- 用户说 "页面卡顿" 时使用
- 不适用于 后端接口响应慢导致的纯网络瓶颈场景

## Instructions
### Step 1: 收集性能症状与复现路径
### Step 2: 使用 Profiler 与渲染日志定位热点组件
### Step 3: 验证结果

## Examples
**Example:** 列表页滚动明显掉帧
User: "我的 React 列表页滚动很卡"
Actions: 1. 复现并录制性能轨迹 2. 定位高频重渲染组件并优化
Result: 滚动帧率提升，交互延迟降低

## Troubleshooting
**Error:** 优化后仍卡顿 / **Cause:** 热点不在前端渲染链路 / **Solution:** 转向接口耗时与资源加载排查
