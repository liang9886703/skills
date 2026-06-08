---
name: python-api-debugging
description: >-
  提供 Python API 故障定位流程，在用户提到 500 报错、超时、日志异常等关键词时触发。
---

# Python API 故障排查
帮助快速定位 Python API 的运行时错误与响应异常。

## When to Use
- 用户说 "接口 500" 时使用
- 不适用于 数据库权限未开通这类环境准备问题

## Instructions
### Step 1: 读取错误日志并提取关键信息
### Step 2: 最小化复现并检查输入与依赖
### Step 3: 验证结果

## Examples
**Example:** 支付接口突发 500
User: "这个 Python 接口一直报 500"
Actions: 1. 对齐请求参数与错误栈 2. 修复异常分支并补充保护
Result: 接口恢复 2xx 返回且错误日志消失

## Troubleshooting
**Error:** 无法稳定复现 / **Cause:** 仅在特定并发条件触发 / **Solution:** 增加请求采样与并发压测复现
