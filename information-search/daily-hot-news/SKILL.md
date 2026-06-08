---
name: daily-hot-news
description: 热榜查询技能。当用户询问微博热搜、B站热门、知乎热榜、抖音热点、百度热搜、今日头条、IT之家、掘金、GitHub趋势等任意平台实时热榜，或说「给我看今天的热榜」「现在热搜是什么」「看看各平台热榜」「今天有什么热点」「最近大家在讨论什么」「帮我查一下热门话题」「XX平台今天热门是什么」时使用。支持56个平台（微博/知乎/B站/抖音/百度/头条/腾讯/网易/澎湃/IT之家/少数派/CSDN/掘金/GitHub/原神/微信读书/豆瓣等），支持单平台查询、多平台汇总、按分类浏览。开箱即用，无需安装任何外部服务。
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - node
---

# 🔥 每日热榜

## 🎯 概述

提供 **56 个热榜源**（实际可用 **45 个**）的查询服务，基于 [DailyHotApi](https://github.com/imsyy/DailyHotApi) 项目。

**开箱即用**：运行时依赖已内置于 `engine/` 目录，无需安装任何外部服务。

**核心功能**：
- 📊 热榜查询 - 查询任意平台的热榜数据
- 📋 分类浏览 - 按分类列出所有支持的热榜源
- 🔄 实时获取 - 每次调用直接抓取最新数据
- 💾 内存缓存 - 1小时 TTL，避免重复请求

---

## 🏗️ 架构设计

```
用户请求
  ↓
daily-hot-news skill（Python fetcher.py）
  ↓ subprocess（临时进程，用完即退）
node engine/bundle.mjs <platform>
  ↓ mock Hono Context（注入默认参数）
DailyHotApi 编译代码（esbuild bundle）
  ↓
各平台实时数据
```

---

## 🎯 触发场景

以下用户输入均应使用本 skill：

- **直接问热榜**：「今天热榜」「现在热搜」「最近热点」「热门话题」「大家在讨论什么」
- **指定平台**：「微博热搜」「B站热门」「知乎热榜」「抖音热点」「百度热搜」「头条热搜」「IT之家热榜」「掘金热门」「GitHub trending」
- **泛化表达**：「给我看看热榜」「刷一下热搜」「看看今天发生了什么」「有什么新鲜事」「帮我查一下热门话题」「XX平台今天热门是什么」
- **分类查询**：「科技圈热点」「游戏圈热门」「今日新闻热点」「技术社区热门」
- **多平台汇总**：「各平台热榜汇总」「今日全网热点」「热榜摘要」

---

## 🚀 使用方法

```python
import sys
sys.path.insert(0, "~/.openclaw/skills/daily-hot-news")
from fetcher import fetch, fetch_multi, fetch_by_category, format_result, list_sources_by_category

# 检查可用性
is_available()  # True

# 查询单平台（自动缓存 1 小时）
result = fetch("weibo")
print(format_result(result, limit=10))

# 批量查询多平台
results = fetch_multi(["weibo", "zhihu", "bilibili"], limit=10)

# 按分类查询（video/social/news/tech/game/reading/tool）
results = fetch_by_category("tech", limit=10)

# 列出所有支持平台
print(list_sources_by_category())

# 强制刷新（忽略缓存）
result = fetch("weibo", no_cache=True)
```

---

## 📡 支持的热榜源（56个）

### 🎬 视频/直播平台
| 接口 | 名称 | 状态 |
|------|------|------|
| bilibili | 哔哩哔哩 | ✅ |
| acfun | AcFun | ✅ |
| douyin | 抖音 | ✅ |
| kuaishou | 快手 | ⚠️ 偶发不可达 |
| coolapk | 酷安 | ❌ 网络不可达 |

### 💬 社交媒体
| 接口 | 名称 | 状态 |
|------|------|------|
| weibo | 微博 | ✅ |
| zhihu | 知乎 | ✅ |
| zhihu-daily | 知乎日报 | ✅ |
| tieba | 百度贴吧 | ✅ |
| douban-group | 豆瓣讨论小组 | ✅ |
| v2ex | V2EX | ❌ 网络不可达 |
| ngabbs | NGA | ✅ |
| hupu | 虎扑 | ✅ |
| newsmth | 水木社区 | ✅ |
| linuxdo | Linux.do | ❌ 网络不可达 |

### 📰 新闻资讯
| 接口 | 名称 | 状态 |
|------|------|------|
| baidu | 百度热搜 | ✅ |
| thepaper | 澎湃新闻 | ✅ |
| toutiao | 今日头条 | ✅ |
| 36kr | 36氪 | ✅ |
| qq-news | 腾讯新闻 | ✅ |
| sina | 新浪网 | ✅ |
| sina-news | 新浪新闻 | ✅ |
| netease-news | 网易新闻 | ✅ |
| huxiu | 虎嗅 | ✅ |
| ifanr | 爱范儿 | ❌ stdout 截断，JSON 解析持续失败 |
| nytimes | 纽约时报 | ❌ 网络不可达 |

### 💻 科技/技术社区
| 接口 | 名称 | 状态 |
|------|------|------|
| ithome | IT之家 | ✅ |
| ithome-xijiayi | IT之家「喜加一」 | ✅ |
| sspai | 少数派 | ✅ |
| csdn | CSDN | ✅ |
| juejin | 稀土掘金 | ✅ |
| 51cto | 51CTO | ✅ |
| nodeseek | NodeSeek | ❌ 网络不可达 |
| hellogithub | HelloGitHub | ✅ |
| geekpark | 极客公园 | ✅ |
| dgtle | 数字尾巴 | ✅ |
| smzdm | 什么值得买 | ✅ |
| github | GitHub Trending | ✅ |
| hackernews | Hacker News | ❌ 网络不可达 |
| producthunt | Product Hunt | ❌ 网络不可达 |

### 🎮 游戏/ACG
| 接口 | 名称 | 状态 |
|------|------|------|
| genshin | 原神 | ✅ |
| miyoushe | 米游社 | ✅ |
| honkai | 崩坏3 | ✅ |
| starrail | 崩坏：星穹铁道 | ✅ |
| lol | 英雄联盟 | ✅ |
| yystv | 游研社 | ✅ |
| gameres | GameRes | ❌ 接口返回空 |

### 📚 阅读/文化
| 接口 | 名称 | 状态 |
|------|------|------|
| jianshu | 简书 | ✅ |
| guokr | 果壳 | ✅ |
| weread | 微信读书 | ✅ |
| douban-movie | 豆瓣电影 | ✅ |

### 🔧 工具/其他
| 接口 | 名称 | 状态 |
|------|------|------|
| 52pojie | 吾爱破解 | ⚠️ 偶发不可达 |
| hostloc | 全球主机交流 | ❌ 网络不可达 |
| weatheralarm | 中央气象台 | ✅ |
| earthquake | 中国地震台 | ❌ 网络不可达 |
| history | 历史上的今天 | ✅ |

---

## 📊 响应格式

```python
{
    "platform": "微博",
    "category": "social",
    "source_id": "weibo",
    "total": 52,
    "update_time": "2026-04-27 15:48:00",
    "from_cache": False,
    "data": [
        {
            "rank": 1,
            "title": "热搜标题",
            "desc": "",
            "hot": "1234万",
            "url": "https://..."
        }
    ]
}
```

---

## ⚙️ 配置项

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `CACHE_TTL` | 3600 秒 | 内存缓存时间 |
| `fetch(..., no_cache=True)` | — | 强制跳过缓存 |
| `fetch_multi(..., limit=10)` | 10 | 每平台返回条数 |

---

## 🔄 更新 DailyHotApi

skill 内置的是打包时的版本。如需升级到最新版：

```bash
cd /tmp
git clone https://github.com/imsyy/DailyHotApi.git dailyhot-rebuild
cd dailyhot-rebuild
npm install --omit=dev
npm run build

# 重新打包为单文件 bundle
ROUTES=$(ls dist/routes/*.js | grep -v '\.d\.ts' | xargs -I{} basename {} .js | sort)
{
  echo "import { createRequire } from 'module'; const require = createRequire(import.meta.url);"
  echo "import { fileURLToPath } from 'url'; import { dirname } from 'path';"
  echo "const __dirname = dirname(fileURLToPath(import.meta.url));"
  echo "process.env.NODE_ENV = 'cli';"
  for r in $ROUTES; do
    echo "import * as route_$(echo $r | tr '-' '_') from './dist/routes/${r}.js';"
  done
  echo "const ROUTES = {"
  for r in $ROUTES; do echo "  '${r}': route_$(echo $r | tr '-' '_'),"; done
  echo "};"
  cat <<'EOF'
const platform = process.argv[2];
if (!platform) { console.error(JSON.stringify({ error: "请指定平台" })); process.exit(1); }
const mockContext = { req: { query: (_key) => "" } };
try {
  const route = ROUTES[platform];
  if (!route) { console.error(JSON.stringify({ error: `未知平台: ${platform}` })); process.exit(1); }
  const result = await route.handleRoute(mockContext, false);
  console.log(JSON.stringify(result));
  process.exit(0);
} catch (e) { console.error(JSON.stringify({ error: e.message || String(e) })); process.exit(1); }
EOF
} > entry_bundle.mjs

npx esbuild entry_bundle.mjs \
  --bundle --platform=node --format=esm \
  --outfile=~/.openclaw/skills/daily-hot-news/engine/bundle.mjs \
  --external:node:* \
  --banner:js="import { createRequire } from 'module'; const require = createRequire(import.meta.url);"
```

---

## 📁 文件结构

```
hot-news/
├── SKILL.md              # 本说明
├── fetcher.py            # 核心抓取模块
└── engine/
    └── bundle.mjs        # esbuild 打包产物（DailyHotApi + 所有依赖，~8MB）
```

---

## ⚠️ 常见问题

### node 未安装
```
FileNotFoundError: [Errno 2] No such file or directory: 'node'
```
解决：安装 Node.js 16+，`node --version` 验证。

### 平台返回空数据
部分平台（如 `gameres`）接口本身返回空，与 skill 无关，属已知限制。

### 网络不可达的平台
`36kr`、`hackernews`、`v2ex` 等平台因服务器网络策略无法访问，非 skill 问题。
