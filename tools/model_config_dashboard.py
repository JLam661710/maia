import streamlit as st
import os

# Page Config
st.set_page_config(
    page_title="Model Config Dashboard",
    page_icon="⚙️",
    layout="wide"
)

ENV_FILE = ".env"
ENV_EXAMPLE_FILE = ".env.example"

def load_env_file(filepath):
    """Read env file and return a dict of key-values and the raw lines."""
    config = {}
    lines = []
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line and not line.startswith("#"):
                    parts = line.split("=", 1)
                    if len(parts) == 2:
                        config[parts[0].strip()] = parts[1].strip()
    return config, lines

def save_env_file(filepath, updates, original_lines):
    """
    Save updates to env file.
    Preserves comments and structure by modifying original lines if key exists,
    or appending if it's new.
    """
    new_lines = []
    updated_keys = set()
    
    # Process existing lines
    for line in original_lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            parts = stripped.split("=", 1)
            if len(parts) == 2:
                key = parts[0].strip()
                if key in updates:
                    new_lines.append(f"{key}={updates[key]}\n")
                    updated_keys.add(key)
                    continue
        new_lines.append(line)
    
    # Append new keys
    for key, value in updates.items():
        if key not in updated_keys:
            # Add a newline before appending new keys if the file doesn't end with one
            if new_lines and not new_lines[-1].endswith("\n"):
                new_lines.append("\n")
            new_lines.append(f"{key}={value}\n")
            updated_keys.add(key)

    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

def main():
    st.title("⚙️ 模型配置管理面板 (Internal Tool)")
    st.markdown("此工具用于调整 Agent 的模型配置，仅供内部使用。修改将保存到 `.env` 文件。")

    # Load Config
    if os.path.exists(ENV_FILE):
        current_config, raw_lines = load_env_file(ENV_FILE)
        st.success(f"已加载配置文件: `{ENV_FILE}`")
    elif os.path.exists(ENV_EXAMPLE_FILE):
        current_config, raw_lines = load_env_file(ENV_EXAMPLE_FILE)
        st.warning(f"未找到 `{ENV_FILE}`，已加载 `{ENV_EXAMPLE_FILE}` 作为模板。保存后将创建 `{ENV_FILE}`。")
    else:
        st.error("未找到配置文件！")
        return

    # Quick Presets
    st.subheader("⚡ 快速预设 (Quick Presets)")
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        if st.button("🚀 加载 Doubao 预设 (Default)", use_container_width=True):
            updates = {
                "OPENAI_BASE_URL": "https://ark.cn-beijing.volces.com/api/v3",
                "OPENAI_API_KEY": "",
                "MODEL_INTERVIEWER": "doubao-seed-1-8-251228",
                "MODEL_ANALYST": "doubao-seed-1-8-251228",
                "MODEL_ARCHITECT": "doubao-seed-1-8-251228",
                "MODEL_SUMMARY": "doubao-seed-1-8-251228",
                "MODEL_JUDGE": "doubao-seed-1-8-251228",
                "REASONING_EFFORT_INTERVIEWER": "minimal",
                "REASONING_EFFORT_ANALYST": "medium",
                "REASONING_EFFORT_ARCHITECT": "high",
                "REASONING_EFFORT_SUMMARY": "minimal",
                "REASONING_EFFORT_JUDGE": "medium",
                "TEMPERATURE_INTERVIEWER": "0.7",
                "TEMPERATURE_ANALYST": "0.2",
                "TEMPERATURE_ARCHITECT": "0.5",
                "TEMPERATURE_SUMMARY": "0.3",
                "TEMPERATURE_JUDGE": "0.2",
                "MAX_TOKENS_ARCHITECT": "12000",
                "RESPONSE_FORMAT_ANALYST": "json_object",
                "RESPONSE_FORMAT_JUDGE": "json_object",
            }
            save_env_file(ENV_FILE, updates, raw_lines)
            st.success("已加载 Doubao 预设！")
            st.rerun()

    with col_p2:
        if st.button("🌐 加载 APIYi 预设 (Legacy)", use_container_width=True):
            updates = {
                "OPENAI_BASE_URL": "https://api.apiyi.com/v1",
                "OPENAI_API_KEY": "",
                "MODEL_INTERVIEWER": "claude-3-7-sonnet-20250219",
                "MODEL_ANALYST": "gemini-3-pro-preview-thinking",
                "MODEL_ARCHITECT": "gemini-3-pro-preview",
                "MODEL_SUMMARY": "gemini-2.5-flash",
                "MODEL_JUDGE": "gemini-3-pro-preview-thinking",
                "REASONING_EFFORT_INTERVIEWER": "None",
                "REASONING_EFFORT_ANALYST": "None",
                "REASONING_EFFORT_ARCHITECT": "None",
                "REASONING_EFFORT_SUMMARY": "None",
                "REASONING_EFFORT_JUDGE": "None",
            }
            save_env_file(ENV_FILE, updates, raw_lines)
            st.success("已加载 APIYi 预设！")
            st.rerun()

    # Form
    with st.form("config_form"):
        st.subheader("1. API 连接配置")
        col1, col2 = st.columns(2)
        
        with col1:
            openai_base_url = st.text_input(
                "API Base URL", 
                value=current_config.get("OPENAI_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3"),
                help="例如: https://ark.cn-beijing.volces.com/api/v3"
            )
        
        with col2:
            openai_api_key = st.text_input(
                "API Key", 
                value=current_config.get("OPENAI_API_KEY", ""),
                type="password",
                help="输入火山引擎或 APIYi 的 API Key"
            )

        st.subheader("2. Agent 模型选择")
        st.caption("输入模型 ID (例如: doubao-seed-1-8-251228)")
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            model_interviewer = st.text_input("Interviewer Model", value=current_config.get("MODEL_INTERVIEWER", "doubao-seed-1-8-251228"))
            model_analyst = st.text_input("Analyst Model", value=current_config.get("MODEL_ANALYST", "doubao-seed-1-8-251228"))
        
        with col_m2:
            model_architect = st.text_input("Architect Model", value=current_config.get("MODEL_ARCHITECT", "doubao-seed-1-8-251228"))
            model_summary = st.text_input("Summary Model", value=current_config.get("MODEL_SUMMARY", "doubao-seed-1-8-251228"))

        with col_m3:
            model_judge = st.text_input("Judge Model", value=current_config.get("MODEL_JUDGE", "doubao-seed-1-8-251228"))

        st.subheader("3. 推理强度配置 (Reasoning Effort)")
        st.caption("仅部分模型支持 (如 o1, o3, doubao-seed)")
        
        reasoning_options = ["None", "minimal", "low", "medium", "high"]
        
        col_r1, col_r2, col_r3 = st.columns(3)
        
        def get_index(key, options):
            val = current_config.get(key, "None")
            if val in options:
                return options.index(val)
            return 0

        with col_r1:
            re_interviewer = st.selectbox(
                "Interviewer Reasoning Effort", 
                options=reasoning_options,
                index=get_index("REASONING_EFFORT_INTERVIEWER", reasoning_options)
            )
            re_analyst = st.selectbox(
                "Analyst Reasoning Effort", 
                options=reasoning_options,
                index=get_index("REASONING_EFFORT_ANALYST", reasoning_options)
            )
            
        with col_r2:
            re_summary = st.selectbox(
                "Summary Reasoning Effort", 
                options=reasoning_options,
                index=get_index("REASONING_EFFORT_SUMMARY", reasoning_options)
            )
            re_architect = st.selectbox(
                "Architect Reasoning Effort", 
                options=reasoning_options,
                index=get_index("REASONING_EFFORT_ARCHITECT", reasoning_options)
            )

        with col_r3:
            re_judge = st.selectbox(
                "Judge Reasoning Effort",
                options=reasoning_options,
                index=get_index("REASONING_EFFORT_JUDGE", reasoning_options)
            )

        st.subheader("4. 采样与输出参数 (可选)")
        col_p_a, col_p_b, col_p_c = st.columns(3)
        with col_p_a:
            temperature_interviewer = st.text_input("TEMPERATURE_INTERVIEWER", value=current_config.get("TEMPERATURE_INTERVIEWER", ""))
            max_tokens_interviewer = st.text_input("MAX_TOKENS_INTERVIEWER", value=current_config.get("MAX_TOKENS_INTERVIEWER", ""))
            top_p_interviewer = st.text_input("TOP_P_INTERVIEWER", value=current_config.get("TOP_P_INTERVIEWER", ""))

        with col_p_b:
            temperature_analyst = st.text_input("TEMPERATURE_ANALYST", value=current_config.get("TEMPERATURE_ANALYST", ""))
            max_tokens_analyst = st.text_input("MAX_TOKENS_ANALYST", value=current_config.get("MAX_TOKENS_ANALYST", ""))
            top_p_analyst = st.text_input("TOP_P_ANALYST", value=current_config.get("TOP_P_ANALYST", ""))

        with col_p_c:
            temperature_architect = st.text_input("TEMPERATURE_ARCHITECT", value=current_config.get("TEMPERATURE_ARCHITECT", ""))
            max_tokens_architect = st.text_input("MAX_TOKENS_ARCHITECT", value=current_config.get("MAX_TOKENS_ARCHITECT", ""))
            top_p_architect = st.text_input("TOP_P_ARCHITECT", value=current_config.get("TOP_P_ARCHITECT", ""))

        col_p_d, col_p_e, col_p_f = st.columns(3)
        with col_p_d:
            temperature_summary = st.text_input("TEMPERATURE_SUMMARY", value=current_config.get("TEMPERATURE_SUMMARY", ""))
            max_tokens_summary = st.text_input("MAX_TOKENS_SUMMARY", value=current_config.get("MAX_TOKENS_SUMMARY", ""))
            top_p_summary = st.text_input("TOP_P_SUMMARY", value=current_config.get("TOP_P_SUMMARY", ""))

        with col_p_e:
            temperature_judge = st.text_input("TEMPERATURE_JUDGE", value=current_config.get("TEMPERATURE_JUDGE", ""))
            max_tokens_judge = st.text_input("MAX_TOKENS_JUDGE", value=current_config.get("MAX_TOKENS_JUDGE", ""))
            top_p_judge = st.text_input("TOP_P_JUDGE", value=current_config.get("TOP_P_JUDGE", ""))

        with col_p_f:
            response_format_analyst = st.text_input("RESPONSE_FORMAT_ANALYST", value=current_config.get("RESPONSE_FORMAT_ANALYST", ""))
            response_format_judge = st.text_input("RESPONSE_FORMAT_JUDGE", value=current_config.get("RESPONSE_FORMAT_JUDGE", ""))

        st.markdown("---")
        submitted = st.form_submit_button("💾 保存配置", use_container_width=True)

        if submitted:
            updates = {
                "OPENAI_BASE_URL": openai_base_url,
                "OPENAI_API_KEY": openai_api_key,
                "MODEL_INTERVIEWER": model_interviewer,
                "MODEL_ANALYST": model_analyst,
                "MODEL_ARCHITECT": model_architect,
                "MODEL_SUMMARY": model_summary,
                "MODEL_JUDGE": model_judge,
                "REASONING_EFFORT_INTERVIEWER": re_interviewer,
                "REASONING_EFFORT_ANALYST": re_analyst,
                "REASONING_EFFORT_ARCHITECT": re_architect,
                "REASONING_EFFORT_SUMMARY": re_summary,
                "REASONING_EFFORT_JUDGE": re_judge,
                "TEMPERATURE_INTERVIEWER": temperature_interviewer,
                "TEMPERATURE_ANALYST": temperature_analyst,
                "TEMPERATURE_ARCHITECT": temperature_architect,
                "TEMPERATURE_SUMMARY": temperature_summary,
                "TEMPERATURE_JUDGE": temperature_judge,
                "TOP_P_INTERVIEWER": top_p_interviewer,
                "TOP_P_ANALYST": top_p_analyst,
                "TOP_P_ARCHITECT": top_p_architect,
                "TOP_P_SUMMARY": top_p_summary,
                "TOP_P_JUDGE": top_p_judge,
                "MAX_TOKENS_INTERVIEWER": max_tokens_interviewer,
                "MAX_TOKENS_ANALYST": max_tokens_analyst,
                "MAX_TOKENS_ARCHITECT": max_tokens_architect,
                "MAX_TOKENS_SUMMARY": max_tokens_summary,
                "MAX_TOKENS_JUDGE": max_tokens_judge,
                "RESPONSE_FORMAT_ANALYST": response_format_analyst,
                "RESPONSE_FORMAT_JUDGE": response_format_judge,
            }
            
            # Filter out "None" values if needed, or save them as empty string/None
            # For this impl, we save "None" as string if selected, or we can choose to not save it.
            # Let's save what the user sees. But if it is "None", maybe we should remove the key or set to empty?
            # Agent logic handles: if self.reasoning_effort and self.reasoning_effort.lower() != "none":
            # So saving "None" string is fine.

            save_env_file(ENV_FILE, updates, raw_lines)
            st.success(f"配置已保存至 `{ENV_FILE}`！请重启主应用以生效。")
            st.toast("配置已保存")
            
            # Reload to show updates
            st.rerun()

if __name__ == "__main__":
    main()
