#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hot-news skill 核心抓取模块

通过 node 直接调用 DailyHotApi 编译代码抓取热榜数据，无需启动 HTTP 服务。
使用 mock Hono Context 解决 c.req 依赖问题，覆盖 45+ 个平台。
Engine 路径: ~/.openclaw/skills/hot-news/engine/bundle.mjs
"""

import json
import subprocess
import time
from typing import Optional, Dict, List, Any

import os as _os
_SKILL_DIR = _os.path.dirname(_os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# 永久黑名单：上游接口废弃或确认为服务器出口封锁，换任何客户端网络都无效
# ---------------------------------------------------------------------------
PERMANENT_UNAVAILABLE: set = {
    "gameres",       # 上游接口返回空数据，与网络无关
}


def _engine_ok(d: str) -> bool:
    """检查 engine 目录是否完整：bundle.mjs 须存在（新版），或兼容旧版 run_route.mjs + dist/routes/"""
    # 新版：单文件 bundle
    if _os.path.isfile(_os.path.join(d, "bundle.mjs")):
        return True
    # 旧版兼容：run_route.mjs + dist/routes/
    if not _os.path.isfile(_os.path.join(d, "run_route.mjs")):
        return False
    routes_dir = _os.path.join(d, "dist", "routes")
    if not _os.path.isdir(routes_dir):
        return False
    try:
        return len(_os.listdir(routes_dir)) > 0
    except OSError:
        return False


def _bundle_path(d: str) -> str:
    """返回 engine 目录中实际可用的入口脚本路径"""
    bundle = _os.path.join(d, "bundle.mjs")
    if _os.path.isfile(bundle):
        return bundle
    return _os.path.join(d, "run_route.mjs")  # 旧版兼容


def _resolve_engine() -> str:
    """按优先级找可用 engine 目录，找不到时尝试从外部 workspace 修复内置 engine"""
    _internal = _os.path.join(_SKILL_DIR, "engine")
    _external = _os.path.expanduser("~/.openclaw/workspace/daily-hot-api")

    # 1. 内置 engine 完整 → 直接用
    if _engine_ok(_internal):
        return _internal

    # 2. 内置 engine run_route.mjs 存在但 dist/routes 损坏/缺失 → 尝试从外部修复
    if _os.path.isfile(_os.path.join(_internal, "run_route.mjs")) and _engine_ok(_external):
        _ext_dist  = _os.path.join(_external, "dist")
        _int_dist  = _os.path.join(_internal, "dist")
        try:
            import shutil
            if _os.path.islink(_int_dist) or (_os.path.isdir(_int_dist) and not _os.path.isdir(_os.path.join(_int_dist, "routes"))):
                if _os.path.islink(_int_dist):
                    _os.unlink(_int_dist)
                else:
                    shutil.rmtree(_int_dist, ignore_errors=True)
                _os.symlink(_ext_dist, _int_dist)
                print(f"[hot-news] 已将内置 engine/dist 指向外部: {_ext_dist}")
        except Exception as _e:
            print(f"[hot-news] 修复软链接失败: {_e}")
        if _engine_ok(_internal):
            return _internal

    # 3. 外部 workspace 完整 → 降级使用
    if _engine_ok(_external):
        return _external

    # 4. 都不行，返回内置路径（fetch 时会失败并报错）
    return _internal


DAILY_HOT_API_DIR = _resolve_engine()
RUN_ROUTE_PATH = _bundle_path(DAILY_HOT_API_DIR)

# 内存缓存 {source_id: (data, timestamp)}
_cache: Dict[str, tuple] = {}
CACHE_TTL = 3600  # 秒

# 全部 56 个热榜源
SOURCES: Dict[str, Dict] = {
    # 视频/直播
    "bilibili":      {"name": "哔哩哔哩",     "category": "video"},
    "acfun":         {"name": "AcFun",        "category": "video"},
    "douyin":        {"name": "抖音",          "category": "video"},
    "kuaishou":      {"name": "快手",          "category": "video"},
    "coolapk":       {"name": "酷安",          "category": "video"},
    # 社交媒体
    "weibo":         {"name": "微博",          "category": "social"},
    "zhihu":         {"name": "知乎",          "category": "social"},
    "zhihu-daily":   {"name": "知乎日报",      "category": "social"},
    "tieba":         {"name": "百度贴吧",      "category": "social"},
    "douban-group":  {"name": "豆瓣讨论",      "category": "social"},
    "v2ex":          {"name": "V2EX",          "category": "social"},
    "ngabbs":        {"name": "NGA",           "category": "social"},
    "hupu":          {"name": "虎扑",          "category": "social"},
    "newsmth":       {"name": "水木社区",      "category": "social"},
    "linuxdo":       {"name": "Linux.do",      "category": "social"},
    # 新闻资讯
    "baidu":         {"name": "百度热搜",      "category": "news"},
    "thepaper":      {"name": "澎湃新闻",      "category": "news"},
    "toutiao":       {"name": "今日头条",      "category": "news"},
    "36kr":          {"name": "36氪",          "category": "news"},
    "qq-news":       {"name": "腾讯新闻",      "category": "news"},
    "sina":          {"name": "新浪网",        "category": "news"},
    "sina-news":     {"name": "新浪新闻",      "category": "news"},
    "netease-news":  {"name": "网易新闻",      "category": "news"},
    "huxiu":         {"name": "虎嗅",          "category": "news"},
    "ifanr":         {"name": "爱范儿",        "category": "news"},
    "nytimes":       {"name": "纽约时报",      "category": "news"},
    # 科技/技术
    "ithome":        {"name": "IT之家",        "category": "tech"},
    "ithome-xijiayi":{"name": "IT之家喜加一",  "category": "tech"},
    "sspai":         {"name": "少数派",        "category": "tech"},
    "csdn":          {"name": "CSDN",          "category": "tech"},
    "juejin":        {"name": "稀土掘金",      "category": "tech"},
    "51cto":         {"name": "51CTO",         "category": "tech"},
    "nodeseek":      {"name": "NodeSeek",      "category": "tech"},
    "hellogithub":   {"name": "HelloGitHub",   "category": "tech"},
    "geekpark":      {"name": "极客公园",      "category": "tech"},
    "dgtle":         {"name": "数字尾巴",      "category": "tech"},
    "smzdm":         {"name": "什么值得买",    "category": "tech"},
    "github":        {"name": "GitHub",        "category": "tech"},
    "hackernews":    {"name": "Hacker News",   "category": "tech"},
    "producthunt":   {"name": "Product Hunt",  "category": "tech"},
    # 游戏/ACG
    "genshin":       {"name": "原神",          "category": "game"},
    "miyoushe":      {"name": "米游社",        "category": "game"},
    "honkai":        {"name": "崩坏3",         "category": "game"},
    "starrail":      {"name": "星穹铁道",      "category": "game"},
    "lol":           {"name": "英雄联盟",      "category": "game"},
    "yystv":         {"name": "游研社",        "category": "game"},
    "gameres":       {"name": "GameRes",       "category": "game"},
    # 阅读/文化
    "jianshu":       {"name": "简书",          "category": "reading"},
    "guokr":         {"name": "果壳",          "category": "reading"},
    "weread":        {"name": "微信读书",      "category": "reading"},
    "douban-movie":  {"name": "豆瓣电影",      "category": "reading"},
    # 工具/其他
    "52pojie":       {"name": "吾爱破解",      "category": "tool"},
    "hostloc":       {"name": "全球主机交流",  "category": "tool"},
    "weatheralarm":  {"name": "中央气象台",    "category": "tool"},
    "earthquake":    {"name": "中国地震台",    "category": "tool"},
    "history":       {"name": "历史上的今天",  "category": "tool"},
}

CATEGORY_NAMES = {
    "video":   "🎬 视频/直播",
    "social":  "💬 社交媒体",
    "news":    "📰 新闻资讯",
    "tech":    "💻 科技/技术",
    "game":    "🎮 游戏/ACG",
    "reading": "📚 阅读/文化",
    "tool":    "🔧 工具/其他",
}


def _make_error(error_type: str, message: str) -> Dict[str, Any]:
    """构造统一结构的错误返回对象"""
    return {
        "error": True,
        "error_type": error_type,
        "message": message,
    }


def _try_recover_truncated_json(truncated_str: str) -> Optional[Dict[str, Any]]:
    """尝试从截断的 JSON 字符串中恢复尽可能多的数据"""
    if not truncated_str or not truncated_str.startswith("{"):
        return None
    
    # 情况 1：字符串被截断，缺少闭合的 } 和可能的后缀
    # 尝试找到最后一个完整对象的边界
    stack = 0
    last_valid_pos = -1
    
    for i, ch in enumerate(truncated_str):
        if ch == '{':
            stack += 1
        elif ch == '}':
            stack -= 1
            if stack == 0:
                last_valid_pos = i
    
    # 如果找到了完整的对象，截取并解析
    if last_valid_pos >= 0:
        try:
            complete_part = truncated_str[:last_valid_pos + 1]
            return json.loads(complete_part)
        except json.JSONDecodeError:
            pass  # 继续尝试其他方法
    
    # 情况 2：尝试修复常见的截断模式
    # 1. 缺少闭合的 }]
    if truncated_str.endswith(']'):
        # 可能缺少闭合的 }，尝试添加
        try:
            return json.loads(truncated_str + '}')
        except json.JSONDecodeError:
            pass
    
    # 2. 在字符串中间截断，尝试添加闭合
    if truncated_str.count('{') > truncated_str.count('}'):
        # 缺少闭合的 }
        try:
            closed = truncated_str + '}' * (truncated_str.count('{') - truncated_str.count('}'))
            return json.loads(closed)
        except json.JSONDecodeError:
            pass
    
    # 3. 尝试解析 "data" 数组部分（如果能看到数组开始）
    data_start = truncated_str.find('"data":')
    if data_start > 0:
        # 找到数组开始位置
        array_start = truncated_str.find('[', data_start)
        if array_start > 0:
            # 手动构建一个最小可解析的 JSON
            # 假设截断在数组内部
            # 尝试找到最近的完整数组项
            items = []
            pos = array_start + 1
            while pos < len(truncated_str):
                # 寻找下一个对象开始
                obj_start = truncated_str.find('{', pos)
                if obj_start < 0:
                    break
                # 寻找对象结束
                obj_end = truncated_str.find('}', obj_start + 1)
                if obj_end < 0:
                    break
                try:
                    item_str = truncated_str[obj_start:obj_end + 1]
                    item = json.loads(item_str)
                    items.append(item)
                    pos = obj_end + 1
                except json.JSONDecodeError:
                    pos = obj_end + 1
            
            if items:
                # 返回部分数据
                return {
                    "data": items,
                    "total": len(items),
                    "partial": True
                }
    
    return None


def fetch(source_id: str, no_cache: bool = False) -> Optional[Dict[str, Any]]:
    """
    获取指定平台热榜数据。

    返回值：
      - 成功：包含 platform/category/data 等字段的 dict
      - 失败：包含 error=True / error_type / message 的 dict
      - 未知平台：None
    """
    global DAILY_HOT_API_DIR, RUN_ROUTE_PATH

    if source_id not in SOURCES:
        return None

    # 永久黑名单：接口废弃，无需尝试
    if source_id in PERMANENT_UNAVAILABLE:
        return _make_error("permanent_unavailable",
                           f"{SOURCES[source_id]['name']} 接口已废弃或无法访问")



    # engine 完整性检查
    if not _engine_ok(DAILY_HOT_API_DIR):
        print(f"[hot-news] engine 不完整: {DAILY_HOT_API_DIR}，尝试重新解析")
        DAILY_HOT_API_DIR = _resolve_engine()
        RUN_ROUTE_PATH = _bundle_path(DAILY_HOT_API_DIR)
        if not _engine_ok(DAILY_HOT_API_DIR):
            return _make_error("engine_missing", "engine 不可用，请检查 bundle.mjs 是否存在")

    # 缓存命中
    if not no_cache and source_id in _cache:
        data, ts = _cache[source_id]
        if time.time() - ts < CACHE_TTL:
            return data

    try:
        # 修复 ifanr 截断：使用 Popen + communicate()，不受 pipe buffer 限制
        proc = subprocess.Popen(
            ["node", RUN_ROUTE_PATH, source_id],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=DAILY_HOT_API_DIR,
        )
        try:
            stdout_bytes, stderr_bytes = proc.communicate(timeout=20)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=2)
            return _make_error("timeout", f"{SOURCES[source_id]['name']} 请求超时（>20s）")

        # 解码
        stdout = stdout_bytes.decode("utf-8", errors="replace").strip()
        stderr = stderr_bytes.decode("utf-8", errors="replace").strip()

        # Node 进程非零退出 → 网络错误或平台不支持
        if proc.returncode != 0:
            return _make_error("network_unreachable",
                               f"{SOURCES[source_id]['name']} 请求失败（exit={proc.returncode}），可能网络不可达")

        # 从最后一行 JSON 开始往前找有效数据行
        raw = None
        parse_err_msg = None
        truncated_data = None
        
        for line in reversed(stdout.splitlines()):
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                raw = json.loads(line)
                break
            except json.JSONDecodeError as e:
                parse_err_msg = str(e)
                # 尝试修复截断的 JSON
                truncated_data = _try_recover_truncated_json(line)
                if truncated_data:
                    raw = truncated_data
                    break
                # 继续往前找，可能上一行是完整的

        if raw is None:
            if parse_err_msg:
                # JSON 截断（如 ifanr）：尝试返回部分数据
                if truncated_data:
                    # 有部分恢复的数据
                    pass  # raw 已设置为 truncated_data，继续处理
                else:
                    return _make_error("json_decode",
                                       f"{SOURCES[source_id]['name']} 接口响应过大导致解析失败，请稍后重试")
            else:
                return _make_error("empty_response",
                                   f"{SOURCES[source_id]['name']} 接口返回空数据")
        
        # 标记为部分数据（如果是从截断恢复的）
        is_partial = truncated_data is not None

        if "error" in raw:
            return _make_error("node_crash", f"Node 端报错: {raw['error']}")

        if not raw.get("data"):
            # 上游返回空数据
            return _make_error("empty_response",
                               f"{SOURCES[source_id]['name']} 接口返回空列表")


        result = {
            "platform": SOURCES[source_id]["name"],
            "category": SOURCES[source_id]["category"],
            "source_id": source_id,
            "total": raw.get("total", 0),
            "update_time": raw.get("updateTime", ""),
            "from_cache": raw.get("fromCache", False),
            "partial": is_partial or raw.get("partial", False),
            "data": [
                {
                    "rank": i + 1,
                    "title": item.get("title", ""),
                    "desc": item.get("desc", ""),
                    "hot": item.get("hot", ""),
                    "url": item.get("url", ""),
                }
                for i, item in enumerate(raw.get("data", []))
            ],
        }
        _cache[source_id] = (result, time.time())
        return result

    except subprocess.TimeoutExpired:
        return _make_error("timeout", f"{SOURCES[source_id]['name']} 请求超时（>20s）")
    except FileNotFoundError:
        return _make_error("node_missing", "未找到 node 可执行文件，请确认已安装 Node.js 16+")
    except Exception as e:
        return _make_error("unknown", str(e))


def fetch_multi(source_ids: List[str], limit: int = 10) -> List[Dict[str, Any]]:
    """批量获取多个平台热榜，自动过滤失败结果"""
    results = []
    for sid in source_ids:
        r = fetch(sid)
        if r and not r.get("error"):
            r = dict(r)
            r["data"] = r["data"][:limit]
            results.append(r)
    return results


def fetch_by_category(category: str, limit: int = 10) -> List[Dict[str, Any]]:
    """按分类获取该类别所有平台热榜"""
    source_ids = [sid for sid, info in SOURCES.items() if info["category"] == category]
    return fetch_multi(source_ids, limit)


def format_result(data: Dict[str, Any], limit: int = 10) -> str:
    """格式化单个平台热榜为 Markdown"""
    if data.get("error"):
        return f"⚠️ {data.get('message', '获取失败')}"
    lines = [f"### 🔥 {data['platform']}"]
    if data.get("update_time"):
        lines.append(f"更新时间: {data['update_time'][:19].replace('T', ' ')}")
    lines.append("")
    for item in data["data"][:limit]:
        hot = f"  `{item['hot']}`" if item.get("hot") else ""
        lines.append(f"{item['rank']:2d}. {item['title']}{hot}")
    return "\n".join(lines)


def is_available() -> bool:
    """检查 engine 是否完整"""
    return _engine_ok(DAILY_HOT_API_DIR)


def list_sources_by_category() -> str:
    """列出所有支持平台，按分类分组"""
    by_cat: Dict[str, List] = {}
    for sid, info in SOURCES.items():
        by_cat.setdefault(info["category"], []).append((sid, info["name"]))

    lines = ["📊 **支持的热榜源（共 56 个）**\n"]
    for cat_key, cat_name in CATEGORY_NAMES.items():
        if cat_key not in by_cat:
            continue
        lines.append(f"**{cat_name}**")
        for sid, name in by_cat[cat_key]:
            # 显示状态
            if sid in PERMANENT_UNAVAILABLE:
                status = " 🚫 接口废弃"
            else:
                status = ""
            lines.append(f"  • {name} (`{sid}`){status}")
        lines.append("")
    return "\n".join(lines)
