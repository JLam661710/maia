# 环境配置指南 (Environment Setup Guide)

欢迎进入 **Triple-Agent System** 的开发准备阶段。请按照以下步骤配置你的本地开发环境。

---

## 1. 检查 Python 环境

我们检测到你的系统已安装 Python 3.9.6，这符合最低要求 (Python 3.8+)。
为了避免污染系统环境，强烈建议创建一个**虚拟环境 (Virtual Environment)**。

### 步骤 A: 创建虚拟环境
在 Trae 的终端 (Terminal) 中运行以下命令：

```bash
# 1. 创建名为 venv 的虚拟环境
python3 -m venv venv

# 2. 激活虚拟环境 (macOS/Linux)
source venv/bin/activate
```

*激活成功后，你的终端提示符前面会出现 `(venv)` 字样。*

---

## 2. 安装项目依赖

激活虚拟环境后，运行以下命令安装所需的 Python 库：

```bash
pip install -r requirements.txt
```

*包含的核心库：*
*   `streamlit`: 用于快速构建 Web 界面。
*   `openai`: 用于调用 LLM API。
*   `python-dotenv`: 用于安全地读取 .env 文件中的密钥。
*   `pydantic`: 用于数据验证和 JSON Schema 定义。

---

## 3. 配置 API Key

为了让 Agent "活" 过来，我们需要给它提供大脑 (LLM API)。

### 步骤 A: 准备 Key
你需要拥有以下至少一种 API Key：
*   **OpenAI** (支持 GPT-4o, o1/o3-mini)
*   **DeepSeek** (支持 V3, R1) -> *推荐！性价比极高*
*   **Anthropic** (支持 Claude 3.5 Sonnet)

### 步骤 B: 创建配置文件
1.  在项目根目录下，复制一份配置模板：
    ```bash
    cp .env.example .env
    ```
2.  打开新生成的 `.env` 文件。
3.  将你的 API Key 填入对应的位置 (例如 `DEEPSEEK_API_KEY=sk-xxxx`)。
4.  保存文件。

**注意：** `.env` 文件包含敏感信息，**绝对不要**提交到 GitHub 等公共代码仓库。

---

## 4. 验证环境

一切准备就绪后，你可以运行以下简单的 Python 代码来测试 Key 是否有效：

```bash
# 创建一个测试脚本
touch test_api.py
```

在 `test_api.py` 中写入：
```python
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# 以 DeepSeek 为例 (如果你用 OpenAI，去掉 base_url 即可)
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"), 
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "Hello, are you ready?"}]
)

print(response.choices[0].message.content)
```

然后运行 `python test_api.py`，如果看到回复，说明环境配置成功！

---

## 5. 准备就绪？

当你完成了以上步骤（特别是填好了 `.env`），请告诉我。我们将开始编写核心的 **Triple-Agent** 代码！
