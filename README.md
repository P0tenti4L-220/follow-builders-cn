# Follow Builders 中文阅读库

从自己关注的中文 AI 与开发作者中，读公开内容，做简短摘要，保留原文入口和可以继续思考的问题。

当前收录 **11 位作者、11 条阅读记录**。最近读取：**2026-10-30**（Asia/Shanghai）。

[阅读最近一期](digests/2026-10-30.md) · [查看 Skill](.agents/skills/follow-builders-cn/SKILL.md) · [整理规则](docs/approach.md)

## 作者目录

| 作者 | 关注主题 | 已整理 |
| --- | --- | ---: |
| [码良](builders/cxjwin/README.md) | 工程实践 / Agent 面试 / iOS | 1 |
| [LinearUncle](builders/LinearUncle/README.md) | AI 编程 / 工程实践 | 1 |
| [小墨同学](builders/xiaomovps/README.md) | Agent / Harness / 硬件 | 1 |
| [张立行](builders/bylixing/README.md) | Agent / Context / 产品实践 | 1 |
| [Ethan 恩宇](builders/UPing123zzz/README.md) | AI 落地 / FDE / 软件交付 | 1 |
| [victor-wu.eth](builders/victor_wu/README.md) | AI 编程 / 产品实践 | 1 |
| [Yifan Xu](builders/yifanxu_ephai/README.md) | Agent / Sandbox / 基础设施 | 1 |
| [数字生命卡兹克](builders/Khazix0918/README.md) | AI 产品 / 应用体验 | 1 |
| [纳米AI](builders/antiAIvo/README.md) | LLM / Agent / 推理 / 训练 | 1 |
| [KonghaYao - 江夏尧](builders/konghayao/README.md) | Agent / AI 编程 / 开源 | 1 |
| [Jerry Fang](builders/Jerry_fsy/README.md) | Agent / RAG / Context / 基础设施 | 1 |

## 阅读归档

- [2026-10-30 阅读摘要](digests/2026-10-30.md)（11 条）

## 如何更新

在 Codex 中打开本仓库，让它使用 `follow-builders-cn` skill，例如：

> 使用 follow-builders-cn，读取这些作者近期的公开内容，生成中文摘要，并同步到本仓库。

流程：读取 `config/sources.json` → 通过已登录浏览器或已授权接口阅读 X → 将摘要和证据范围追加到 `data/curated-posts.json` → 运行构建检查 → 按本轮请求同步 GitHub。

```sh
python3 scripts/build.py
python3 scripts/build.py --check
```

构建脚本只用 Python 标准库，负责校验记录、按作者归档和生成目录；联网阅读和摘要由运行 skill 的 agent 完成。校验通过不代表事实已经独立核验。

## 当前能力

首版支持浏览器辅助的按需整理与 GitHub 同步。尚未配置定时任务、X API 或后台抓取，也不承诺覆盖每一篇新帖。登录失效或内容无法读取时，应报告缺口。

灵感来自 [zarazhangrui/follow-builders](https://github.com/zarazhangrui/follow-builders)。其默认 skill 使用作者维护的集中 feed；这个版本改为可维护的中文作者列表，并将输出放到 GitHub。这里没有复用对方的后台 feed 或假定它能采集任意账号。

本仓库仅发布自行整理的摘要与链接。原帖、图片及外链文章的权利归原作者；仓库中的原创工具代码和整理文字使用 [MIT License](LICENSE)。
