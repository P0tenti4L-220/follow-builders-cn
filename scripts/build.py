#!/usr/bin/env python3
"""Validate curated observations and render Markdown; no network or model calls."""

import argparse
import datetime as dt
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDLE = re.compile(r"[A-Za-z0-9_]{1,15}\Z")
SCOPES = {
    "visible_text": "主页可见正文；未展开外链、图片或引用全文",
    "expanded_visible_text": "已展开可见正文；未核验图片、视频及引用全文",
}


def cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def load_data():
    config = json.loads((ROOT / "config/sources.json").read_text())
    sources = config["sources"]
    by_handle = {}
    for source in sources:
        handle = source["handle"]
        if not HANDLE.fullmatch(handle) or handle.lower() in by_handle:
            raise ValueError(f"Invalid or duplicate source handle: {handle}")
        for key in ("name", "focus", "topics"):
            if not source.get(key):
                raise ValueError(f"Missing source {key}: {handle}")
        by_handle[handle.lower()] = source
    posts = json.loads((ROOT / "data/curated-posts.json").read_text())
    seen = set()
    for post in posts:
        source = by_handle[post["handle"].lower()]
        if post["handle"] != source["handle"]:
            raise ValueError("Use canonical source handle casing")
        match = re.fullmatch(r"https://x\.com/([A-Za-z0-9_]+)/status/([0-9]+)", post["url"])
        if not match or match[1].lower() != post["handle"].lower():
            raise ValueError(f"URL does not match source: {post['url']}")
        if match[2] in seen:
            raise ValueError(f"Duplicate post ID: {match[2]}")
        seen.add(match[2])
        collected = dt.date.fromisoformat(post["collected_on"])
        if collected.isoformat() != post["collected_on"]:
            raise ValueError("Use YYYY-MM-DD dates")
        if post["evidence_scope"] not in SCOPES:
            raise ValueError("Unknown evidence scope")
        for key in ("title", "summary", "learning_prompt", "published_label", "entry_type"):
            if not isinstance(post.get(key), str) or not post[key].strip():
                raise ValueError(f"Missing post {key}")
    return config, sources, by_handle, posts


def note(post, source, level=2):
    return (
        f"{'#' * level} {post['title']}\n\n"
        f"作者：[{source['name']}](https://x.com/{source['handle']}) · 类型：{post['entry_type']}\n\n"
        f"{post['summary']}\n\n"
        f"学习问题（本仓库整理）：{post['learning_prompt']}\n\n"
        f"[查看原文]({post['url']}) · X 显示发布时间：{post['published_label']}\n\n"
        f"读取于 {post['collected_on']}（Asia/Shanghai）；{SCOPES[post['evidence_scope']]}。\n"
    )


def render():
    config, sources, by_handle, posts = load_data()
    files = {}
    days = defaultdict(list)
    authors = defaultdict(list)
    for post in posts:
        days[post["collected_on"]].append(post)
        authors[post["handle"]].append(post)
    latest = max(days) if days else None
    rows = ["| 作者 | 关注主题 | 已整理 |", "| --- | --- | ---: |"]
    for source in sources:
        handle = source["handle"]
        entries = authors[handle]
        rows.append(f"| [{cell(source['name'])}](builders/{handle}/README.md) | {cell(' / '.join(source['topics']))} | {len(entries)} |")
        groups = defaultdict(list)
        for post in entries:
            groups[post["collected_on"]].append(post)
        profile = (
            f"# {source['name']}\n\n"
            f"[X 主页](https://x.com/{handle}) · [返回目录](../../README.md)\n\n"
            f"关注方向：{source['focus']}\n\n"
            f"主题：{' / '.join(source['topics'])}\n\n"
            f"来源：{config['selection_verified_on']} 从当前关注页选取的公开账号。上述方向是整理标签；不构成对作者资质或产品效果的核验。\n\n"
            "## 归档\n\n"
        )
        profile += "\n".join(f"- [{day}：{len(items)} 条](./{day}.md)" for day, items in sorted(groups.items(), reverse=True)) or "本次只建立作者索引，尚未整理帖子。"
        files[f"builders/{handle}/README.md"] = profile + "\n"
        for day, items in groups.items():
            files[f"builders/{handle}/{day}.md"] = (
                f"# {source['name']} · {day} 阅读记录\n\n[作者索引](README.md) · [本期摘要](../../digests/{day}.md)\n\n"
                + "\n".join(note(p, source) for p in items)
            )
    for day, items in days.items():
        files[f"digests/{day}.md"] = (
            f"# 中文 Builders 阅读摘要 · {day}\n\n"
            f"本期 {len(items)} 条，来自 {len({p['handle'] for p in items})} 位作者；日期为读取日，并非所有帖子都发布于当天。\n\n"
            "以下是对公开文字的中文概括。产品能力、效果和数字属于原作者的说法，本仓库未做独立复测。学习问题由本仓库整理。\n\n"
            "[全部作者](../README.md)\n\n"
            + "\n".join(note(p, by_handle[p["handle"].lower()]) for p in items)
        )
    archives = "\n".join(f"- [{day} 阅读摘要](digests/{day}.md)（{len(items)} 条）" for day, items in sorted(days.items(), reverse=True)) or "暂无已整理内容。"
    files["README.md"] = (
        "# Follow Builders 中文阅读库\n\n"
        "从自己关注的中文 AI 与开发作者中，读公开内容，做简短摘要，保留原文入口和可以继续思考的问题。\n\n"
        f"当前收录 **{len(sources)} 位作者、{len(posts)} 条阅读记录**。最近读取：**{latest or '暂无'}**（Asia/Shanghai）。\n\n"
        f"{'[阅读最近一期](digests/' + latest + '.md) · ' if latest else ''}[查看 Skill](.agents/skills/follow-builders-cn/SKILL.md) · [整理规则](docs/approach.md)\n\n"
        "## 作者目录\n\n" + "\n".join(rows) + "\n\n"
        "## 阅读归档\n\n" + archives + "\n\n"
        "## 如何更新\n\n"
        "在 Codex 中打开本仓库，让它使用 `follow-builders-cn` skill，例如：\n\n"
        "> 使用 follow-builders-cn，读取这些作者近期的公开内容，生成中文摘要，并同步到本仓库。\n\n"
        "流程：读取 `config/sources.json` → 通过已登录浏览器或已授权接口阅读 X → 将摘要和证据范围追加到 `data/curated-posts.json` → 运行构建检查 → 按本轮请求同步 GitHub。\n\n"
        "```sh\npython3 scripts/build.py\npython3 scripts/build.py --check\n```\n\n"
        "构建脚本只用 Python 标准库，负责校验记录、按作者归档和生成目录；联网阅读和摘要由运行 skill 的 agent 完成。校验通过不代表事实已经独立核验。\n\n"
        "## 当前能力\n\n"
        "首版支持浏览器辅助的按需整理与 GitHub 同步。尚未配置定时任务、X API 或后台抓取，也不承诺覆盖每一篇新帖。登录失效或内容无法读取时，应报告缺口。\n\n"
        "灵感来自 [zarazhangrui/follow-builders](https://github.com/zarazhangrui/follow-builders)。其默认 skill 使用作者维护的集中 feed；这个版本改为可维护的中文作者列表，并将输出放到 GitHub。这里没有复用对方的后台 feed 或假定它能采集任意账号。\n\n"
        "本仓库仅发布自行整理的摘要与链接。原帖、图片及外链文章的权利归原作者；仓库中的原创工具代码和整理文字使用 [MIT License](LICENSE)。\n"
    )
    return files, len(sources), len(posts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate inputs and detect stale generated Markdown")
    args = parser.parse_args()
    files, sources, posts = render()
    stale = []
    for path, content in files.items():
        target = ROOT / path
        if args.check:
            if not target.exists() or target.read_text() != content:
                stale.append(path)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
    if stale:
        parser.exit(1, "Generated files need rebuilding: " + ", ".join(stale) + "\n")
    print(f"{'Checked' if args.check else 'Built'} {len(files)} Markdown files; {sources} authors, {posts} posts.")


if __name__ == "__main__":
    main()
