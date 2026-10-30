# 整理方法与边界

参考项目：[zarazhangrui/follow-builders](https://github.com/zarazhangrui/follow-builders)。2026-10-30 查看其 README、SKILL.md、feed 生成脚本和 GitHub Actions 配置。

借鉴的是“关注实际构建者、按来源组织、摘要附原文链接、技能流程与脚本分工”的思路。本仓库的脚本和说明为独立编写。

原项目的消费端读取作者集中生成的 feed，默认 skill 不允许用户直接修改集中来源；其生成脚本调用 X API，工作流通过 secret 提供 `X_BEARER_TOKEN`。因此，原项目的“使用者无需 key”不能直接推导为任意自选作者都可无配置地后台采集。

这里改用 `config/sources.json` 维护选定的中文作者，并使用已授权浏览器按需阅读。首期作者从实际关注页选择，关注方向根据公开简介概括；没有将简介中的履历、产品能力或效果作为独立核验事实。未收录完整关注名单，也不发布用户登录信息。

`data/curated-posts.json` 是整理后的记录源。每条记录保留作者、X status URL、页面时间标签、读取日和读取范围。作者目录、按日阅读摘要和首页由 `scripts/build.py` 生成。只存摘要与链接，不搬运原帖全文、配图或视频。

“学习问题”由整理者提出，目的是帮助阅读者继续思考，不表示原作者已经回答或本仓库已经完成实验。引用帖中的第三方说法需要明确归属，产品效果需要单独验证。

目前是浏览器辅助的按需工作流。仓库没有定时任务、X API 密钥、后台抓取服务或外部 LLM 调用。未来若需要无人值守更新，应先选择可持续访问的内容接口，再配置调度，并真实跑通一次后记录结果。

Skill 的形式参考 [OpenAI 官方技能说明](https://developers.openai.com/plugins/concepts/skills)：用 `SKILL.md` 记录重复工作流，需要时附带脚本与参考资料。此处的 skill 位于 `.agents/skills/follow-builders-cn/`。
