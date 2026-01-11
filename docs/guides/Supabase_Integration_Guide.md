# 傻瓜式 Supabase 数据库配置与操作指南

## 1. 简介
这份指南是为您量身定制的，旨在帮助您零基础将 **Trae AI** 项目连接到 **Supabase** 云数据库。您不需要懂任何 SQL 代码或数据库原理，只需按照下方的图文步骤点点鼠标即可。

---

## 2. 注册与创建项目 (3分钟)

1.  **打开官网**：访问 [https://supabase.com/](https://supabase.com/)。
2.  **登录/注册**：点击右上角的 `Sign in`，可以直接使用 GitHub 账号登录（如果没有 GitHub，建议注册一个，很方便）。
3.  **新建项目**：
    *   登录后，点击绿色的 `+ New Project` 按钮。
    *   选择一个 `Organization`（如果还没创建，系统会提示你创建一个，随便起个名就行）。
    *   **Name**: 输入项目名称，例如 `maia-db`。
    *   **Database Password**: 点击 `Generate a password` 生成一个强密码，**务必复制并保存好这个密码**（虽然我们在本教程中暂时用不到它，但以防万一）。iCYM0j3AWQfCCJBp
    *   **Region**: 选择离您最近的地区（例如 `Singapore` 或 `Tokyo`，国内访问会快一些）。
    *   点击 `Create new project`。
4.  **等待初始化**：系统大概需要 1-2 分钟来为您准备数据库，屏幕上会显示 "Setting up..."，稍等片刻即可。

---

## 3. 一键配置数据库表 (1分钟)

1.  **打开 SQL 编辑器**：
    *   在 Supabase 左侧侧边栏中，找到图标像“两张纸”一样的按钮（鼠标悬停会显示 `SQL Editor`），点击它。
2.  **新建查询**：
    *   点击页面左上角的 `+ New query`。
3.  **复制粘贴代码**：
    *   **回到 Trae 编辑器**，打开项目根目录下的 `supabase_setup_v2.sql` 文件。
    *   **全选** (`Ctrl+A` 或 `Cmd+A`) 并 **复制** (`Ctrl+C` 或 `Cmd+C`) 里面的所有内容。
    *   **回到 Supabase 网页**，把刚才复制的内容 **粘贴** 到那个大的黑色编辑框里。
4.  **运行代码**：
    *   点击右下角绿色的 `Run` 按钮。
    *   如果您看到 `Success` 的提示，说明所有数据库表都已经自动创建好了！

---

## 4. 关键配置：关闭邮箱验证 (必做！)

为了实现“傻瓜式”注册（不需要发邮件点链接），您必须在后台关闭邮箱验证功能：

1.  在 Supabase 左侧菜单点击 `Authentication` (图标像一个指纹)。
2.  在二级菜单点击 `Providers`。
3.  点击 `Email` 展开设置。
4.  **关闭** `Confirm email` (Confirm email addresses) 开关。
5.  点击 `Save` 保存。

---

## 5. 填入 Trae 项目 (1分钟)

1.  **回到 Trae 编辑器**。
2.  打开项目根目录下的 `.env` 文件。
3.  找到最后两行：
    ```env
    # Supabase Configuration
    SUPABASE_URL=your_supabase_project_url
    SUPABASE_KEY=your_supabase_anon_key
    ```
4.  **替换内容**：
    *   把 `your_supabase_project_url` 替换为您刚才复制的 `Project URL`。
    *   把 `your_supabase_anon_key` 替换为您刚才复制的 `anon key`。
5.  **保存文件** (`Ctrl+S` 或 `Cmd+S`)。

---

## 6. 完成！验证成果

恭喜您！所有配置都已完成。

1.  **自动验证（推荐）**：
    *   我们在项目中为您准备了一个自动化验证脚本。在终端运行：
        ```bash
        python verify_supabase_connection.py
        ```
    *   如果看到绿色的 `SUCCESS`，说明一切正常！

2.  **启动项目**：
    *   在终端中运行：
        ```bash
        streamlit run main.py
        ```

---

## 7. 如何查看数据库中的内容？

您有三种方式可以查看保存的数据：

### 方法一：使用 Supabase 网页（最直观，上帝视角）
1.  回到 [Supabase 官网](https://supabase.com/dashboard/projects)。
2.  进入您的项目。
3.  点击左侧侧边栏的 **Table Editor** 图标（像一个表格）。
4.  您会看到以下几张表：
    *   `sessions`: 存储所有的对话会话（包括游客和注册用户）。
    *   `messages`: 存储每一条具体的聊天记录。
    *   `users`: (系统表) 存储注册用户的账号信息。

### 方法二：使用项目自带的“管理员查看器”（最快捷，不用打开网页）
我们在项目中为您内置了一个简单的查看脚本。
1.  在 Trae 的终端中运行：
    ```bash
    python view_all_data.py
    ```
2.  它会直接在终端里列出最新的 5 条会话和消息，方便您快速确认数据是否写入成功。

### 方法三：在 App 内部查看（用户视角）
1.  启动应用 (`streamlit run main.py`)。
2.  登录您的账号。
3.  在 **Dashboard** (仪表盘) 页面，您可以看到属于您自己的历史会话记录。

---

## 常见问题 (FAQ)

*   **Q: 我的数据安全吗？**
    *   A: 本方案使用了 Supabase 的标准安全机制。我们在配置中开启了 Row Level Security (RLS) 并允许了公开读写以便于您快速上手演示。如果您要将项目发布给其他人使用，请联系 AI 助手为您升级更严格的安全策略。
*   **Q: 数据库连不上怎么办？**
    *   A: 检查 `.env` 文件里的 URL 和 KEY 是否有多余的空格，或者是否复制错了。确保您的网络能正常访问国外网站。
