# Cloudflare / 线上部署指南

本指南旨在帮助您将 Maia 项目部署到线上环境（如 Streamlit Community Cloud, Cloudflare, Railway 等）。

## 1. 环境变量配置 (Environment Variables)

无论您选择哪个平台进行部署，都必须在平台的“Settings”或“Environment Variables”部分添加以下键值对。**请勿将这些值直接提交到 GitHub 代码仓库中！**

| 变量名 (Key) | 描述 (Description) | 示例值 (Example Value) |
| :--- | :--- | :--- |
| `OPENAI_API_KEY` | 火山引擎或兼容 OpenAI 格式的 API Key | `a10addaa-4bf9-xxxx` |
| `OPENAI_BASE_URL` | API 基础地址 | `https://ark.cn-beijing.volces.com/api/v3` |
| `SUPABASE_URL` | Supabase 项目 URL | `https://xxxx.supabase.co` |
| `SUPABASE_KEY` | Supabase Key | `<<your_supabase_key>>` |
| `INVITE_CODE` | 注册邀请码 (用于限制用户注册) | `MAIA2025` |
| `MODEL_INTERVIEWER` | 访谈者模型名称 | `doubao-seed-1-8-251228` |
| `MODEL_ANALYST` | 分析师模型名称 | `doubao-seed-1-8-251228` |
| `MODEL_ARCHITECT` | 架构师模型名称 | `doubao-seed-1-8-251228` |
| `MODEL_SUMMARY` | 总结专员模型名称 | `doubao-seed-1-8-251228` |
| `MODEL_JUDGE` | 评估者模型名称 | `doubao-seed-1-8-251228` |
| `REASONING_EFFORT_INTERVIEWER` | 访谈者推理强度 | `minimal` |
| `REASONING_EFFORT_ANALYST` | 分析师推理强度 | `medium` |
| `REASONING_EFFORT_ARCHITECT` | 架构师推理强度 | `high` |
| `REASONING_EFFORT_SUMMARY` | 总结专员推理强度 | `minimal` |
| `REASONING_EFFORT_JUDGE` | 评估者推理强度 | `medium` |
| `TEMPERATURE_INTERVIEWER` | 访谈者采样温度（可选） | `0.7` |
| `TEMPERATURE_ANALYST` | 分析师采样温度（可选） | `0.2` |
| `TEMPERATURE_ARCHITECT` | 架构师采样温度（可选） | `0.7` |
| `TEMPERATURE_SUMMARY` | 总结专员采样温度（可选） | `0.3` |
| `TEMPERATURE_JUDGE` | 评估者采样温度（可选） | `0.2` |
| `TOP_P_INTERVIEWER` | 访谈者 top_p（可选） | `1.0` |
| `TOP_P_ANALYST` | 分析师 top_p（可选） | `1.0` |
| `TOP_P_ARCHITECT` | 架构师 top_p（可选） | `1.0` |
| `TOP_P_SUMMARY` | 总结专员 top_p（可选） | `1.0` |
| `TOP_P_JUDGE` | 评估者 top_p（可选） | `1.0` |
| `MAX_TOKENS_INTERVIEWER` | 访谈者最大输出 token（可选） | `1024` |
| `MAX_TOKENS_ANALYST` | 分析师最大输出 token（可选） | `4096` |
| `MAX_TOKENS_ARCHITECT` | 架构师最大输出 token（可选） | `8192` |
| `MAX_TOKENS_SUMMARY` | 总结专员最大输出 token（可选） | `1024` |
| `MAX_TOKENS_JUDGE` | 评估者最大输出 token（可选） | `2048` |
| `RESPONSE_FORMAT_ANALYST` | 分析师输出格式（可选） | `{\"type\":\"json_object\"}` |
| `RESPONSE_FORMAT_JUDGE` | 评估者输出格式（可选） | `{\"type\":\"json_object\"}` |

## 2. Zeabur 部署要点（Docker / Port）

- 本项目包含 [Dockerfile](file:///Users/lishuyi/Downloads/TRAE%20-%20%E6%99%BA%E8%83%BD%E4%BD%93%E5%BC%80%E5%8F%91%E7%BB%BC%E5%90%88/trae%20-%20multiAgentProject_%E5%89%AF%E6%9C%AC/Dockerfile)，默认以 Docker 方式启动 Streamlit。
- 平台侧若注入 `PORT` 环境变量，容器会自动监听 `PORT`（缺省回退 8501）。
- 在 Zeabur 配置环境变量时，务必只在平台侧填写 Key，不要写入仓库文件。

## 2.1 Zeabur 一键粘贴（当前运行配置，安全版）

说明：为了避免密钥泄露，本文档不会写入真实的 `OPENAI_API_KEY / SUPABASE_KEY / POSTHOG_API_KEY / INVITE_CODE`。请从你本地运行机器的 `.env` 中复制对应值，粘贴到 Zeabur。
把下面整段复制到 Zeabur 的 Environment Variables（或逐条添加）：

```env
OPENAI_API_KEY=<<从本地 .env 复制>>
OPENAI_BASE_URL=https://ark.cn-beijing.volces.com/api/v3

SUPABASE_URL=https://omkszgpsxwbeowbcvlhc.supabase.co
SUPABASE_KEY=<<从本地 .env 复制>>
INVITE_CODE=<<从本地 .env 复制>>

POSTHOG_API_KEY=<<从本地 .env 复制（可为空）>>
POSTHOG_HOST=https://us.posthog.com

MODEL_INTERVIEWER=doubao-seed-1-8-251228
MODEL_ANALYST=doubao-seed-1-8-251228
MODEL_ARCHITECT=doubao-seed-1-8-251228
MODEL_SUMMARY=doubao-seed-1-8-251228
MODEL_JUDGE=doubao-seed-1-8-251228

REASONING_EFFORT_INTERVIEWER=minimal
REASONING_EFFORT_ANALYST=medium
REASONING_EFFORT_ARCHITECT=high
REASONING_EFFORT_SUMMARY=minimal
REASONING_EFFORT_JUDGE=medium

TEMPERATURE_INTERVIEWER=0.7
TEMPERATURE_ANALYST=0.2
TEMPERATURE_ARCHITECT=0.7
TEMPERATURE_SUMMARY=0.3
TEMPERATURE_JUDGE=0.2

TOP_P_INTERVIEWER=1.0
TOP_P_ANALYST=1.0
TOP_P_ARCHITECT=1.0
TOP_P_SUMMARY=1.0
TOP_P_JUDGE=1.0

MAX_TOKENS_INTERVIEWER=1024
MAX_TOKENS_ANALYST=4096
MAX_TOKENS_ARCHITECT=8192
MAX_TOKENS_SUMMARY=1024
MAX_TOKENS_JUDGE=2048

RESPONSE_FORMAT_ANALYST={"type":"json_object"}
RESPONSE_FORMAT_JUDGE={"type":"json_object"}
```

## 3. 部署前检查清单 (Pre-deployment Checklist)

- [x] **敏感信息隐藏**: `.env` 文件已被 `.gitignore` 忽略，不会上传到 GitHub。
- [x] **仓库密钥清理**: 仓库内不应出现任何明文 token/key（示例文档与测试脚本也要用占位符/环境变量）。
- [x] **依赖完整性**: `requirements.txt` 已包含 `tenacity` 等所有必要库。
- [x] **权限控制**: 游客模式已关闭，注册需校验邀请码。
- [x] **管理员视图**: 仅特定邮箱可见 Token 消耗和 JSON 状态。

## 4. GitHub 上传与更新

在本地终端执行以下命令将代码推送到 GitHub：

```bash
# 关联远程仓库 (请替换为您的实际仓库地址)
git remote add origin git@github.com:JLam661710/maia.git

# 推送代码到主分支
git push -u origin main
```

## 5. Cloudflare Zero Trust / Access (可选)

如果您计划使用 Cloudflare Tunnel 将本地服务暴露到公网，或使用 Cloudflare Access 进行额外的身份验证，请确保：
1. 在 Cloudflare Dashboard 中配置 Tunnel。
2. 将 Tunnel 运行在部署服务的机器上。
3. 在 Cloudflare Access 中配置允许访问的邮箱规则（但这可能与 Maia 自带的邀请码机制功能重叠）。

**推荐**: 直接使用支持 Streamlit 的托管平台（如 Streamlit Community Cloud），然后在该平台上填入上述环境变量即可一键上线。
