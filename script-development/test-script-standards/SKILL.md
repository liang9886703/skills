---
name: test-script-standards
description: Use when writing or refactoring shell test scripts, recovery scripts, or harness scripts that need clean environment setup, unified output layout, fail-fast behavior, structured logs, and clear script headers.
---

# Test Script Standards

用于编写或重构 `sh/bash` 测试脚本、恢复脚本、harness 脚本。

## 硬规则

- 启动前先做环境初始化，确保脚本可重复运行且不受旧环境污染。
- 一个测试任务只用一个统一输出目录；子步骤或子脚本输出放到这个目录下的不同子目录。
- 少用启动环境变量；大多数配置直接写在脚本最上方。
- 所有步骤封装成函数；全局只放常量、路径、简单 helper；最后由 `main` 串起来执行。
- 错误即停止；测试脚本的目标是暴露问题，不要吞错继续跑。
- 多行处理优先“结果先进变量，再用变量做解析或管道”。
- 调试信息必须持久化到文件，不只打在终端。
- 脚本内必须有注释，但注释应解释结构和意图，不要解释废话。
- 脚本最前面必须写：使用方式、原理、主流程函数调用图、输出文件清单和用途。

## 推荐结构

按这个顺序组织：

1. 脚本头部说明
2. 静态配置
3. 输出目录定义
4. 通用 helper
5. 环境初始化和清理函数
6. 步骤函数
7. `main`

## 头部说明必须包含

- Usage：怎么运行脚本
- Principle：脚本测什么、怎么测
- Main flow：只列主流程函数调用图，不展开细节
- Output files：运行后会产出哪些文件，每个文件做什么

## 环境初始化必须做

- 校验配置
- 清理旧输出目录
- 重建目录结构
- 清空日志文件
- 清理旧端口、旧 pid、旧 store、旧 db 或其他残留资源
- 记录本次运行配置

如果脚本拉起了后台进程，要配 `trap` 做退出清理。

## 输出目录要求

同一个测试任务统一放在一个根目录下，例如：

```text
test_out/<task-id>/
  <agent-or-case>/
    logs/
    http/
    turns/
    debug/
```

要求：

- `logs/` 放脚本、server、runner 等进程日志
- `http/` 放请求和响应
- `turns/` 放逐轮输入输出和结果表
- `debug/` 放 dump、poll trace、失败快照

## 日志要求

至少要有这些日志：

- 脚本主流程日志
- 子进程日志
- HTTP 请求日志
- HTTP 响应日志
- 每轮请求文件
- 每轮回答文件
- 每轮 debug dump
- 失败快照

HTTP 日志至少包含：

- 时间
- 方法
- URL
- 请求体或请求文件
- 响应状态码
- 响应头
- 响应体
- 客户端退出码

## 写法要求

- 默认 `set -eu`
- 运行步骤不要写在全局
- 不要写过长的裸管道
- 先取结果到变量，再解析
- 重要中间结果能落盘就落盘

## 工作顺序

1. 定义任务级输出目录
2. 把常量写到脚本顶部
3. 写环境初始化和清理
4. 拆主流程步骤函数
5. 加失败即停
6. 加持久化日志
7. 补头部说明
8. 最后做 `sh -n`

## 完成前检查

- 能重复运行，不受上次结果污染
- 输出目录统一且清晰
- 没有不必要的启动环境变量
- 主流程全部在函数里
- 出错会停
- 请求和响应有持久化日志
- 头部说明完整
- `sh -n` 通过
