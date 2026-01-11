# Cloudflare / 线上部署指南

本指南旨在帮助您将 Maia 项目部署到线上环境（如 Streamlit Community Cloud, Cloudflare, Railway 等）。

## 1. 环境变量配置 (Environment Variables)

无论您选择哪个平台进行部署，都必须在平台的“Settings”或“Environment Variables”部分添加以下键值对。**请勿将这些值直接提交到 GitHub 代码仓库中！**

| 变量名 (Key) | 描述 (Description) | 示例值 (Example Value) |
| :--- | :--- | :--- |
| `OPENAI_API_KEY` | 火山引擎或兼容 OpenAI 格式的 API Key | `a10addaa-4bf9-xxxx` |
| `OPENAI_BASE_URL` | API 基础地址 | `https://ark.cn-beijing.volces.com/api/v3` |
| `SUPABASE_URL` | Supabase 项目 URL | `https://xxxx.supabase.co` |
| `SUPABASE_KEY` | Supabase Anon Key (公开密钥) | `eyJhbGciOiJIUzI1NiIs...` |
| `INVITE_CODE` | 注册邀请码 (用于限制用户注册) | `MAIA2025` |
| `MODEL_INTERVIEWER` | 访谈者模型名称 | `doubao-seed-1-8-251228` |
| `MODEL_ANALYST` | 分析师模型名称 | `doubao-seed-1-8-251228` |
| `MODEL_ARCHITECT` | 架构师模型名称 | `doubao-seed-1-8-251228` |
| `MODEL_SUMMARY` | 总结专员模型名称 | `doubao-seed-1-8-251228` |
| `REASONING_EFFORT_INTERVIEWER` | 访谈者推理强度 | `minimal` |
| `REASONING_EFFORT_ANALYST` | 分析师推理强度 | `medium` |
| `REASONING_EFFORT_ARCHITECT` | 架构师推理强度 | `high` |
| `REASONING_EFFORT_SUMMARY` | 总结专员推理强度 | `minimal` |

## 2. 部署前检查清单 (Pre-deployment Checklist)

- [x] **敏感信息隐藏**: `.env` 文件已被 `.gitignore` 忽略，不会上传到 GitHub。
- [x] **依赖完整性**: `requirements.txt` 已包含 `tenacity` 等所有必要库。
- [x] **权限控制**: 游客模式已关闭，注册需校验邀请码。
- [x] **管理员视图**: 仅特定邮箱可见 Token 消耗和 JSON 状态。

## 3. GitHub 上传与更新

在本地终端执行以下命令将代码推送到 GitHub：

```bash
# 关联远程仓库 (请替换为您的实际仓库地址)
git remote add origin git@github.com:JLam661710/maia.git

# 推送代码到主分支
git push -u origin main
```

## 4. Cloudflare Zero Trust / Access (可选)

如果您计划使用 Cloudflare Tunnel 将本地服务暴露到公网，或使用 Cloudflare Access 进行额外的身份验证，请确保：
1. 在 Cloudflare Dashboard 中配置 Tunnel。
2. 将 Tunnel 运行在部署服务的机器上。
3. 在 Cloudflare Access 中配置允许访问的邮箱规则（但这可能与 Maia 自带的邀请码机制功能重叠）。

**推荐**: 直接使用支持 Streamlit 的托管平台（如 Streamlit Community Cloud），然后在该平台上填入上述环境变量即可一键上线。
