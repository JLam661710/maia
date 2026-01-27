import json
import os
from typing import Any, Dict, Optional, Tuple, List


DEFAULT_TOOL_CATALOG_PATH = os.path.join("config", "tool_catalog.json")


def load_tool_catalog_from_file(file_path: str = DEFAULT_TOOL_CATALOG_PATH) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data, None
        return None, "tool_catalog must be a JSON object"
    except FileNotFoundError:
        return None, f"tool_catalog file not found: {file_path}"
    except json.JSONDecodeError as e:
        return None, f"tool_catalog JSON parse error: {e}"
    except Exception as e:
        return None, f"tool_catalog load error: {e}"


def validate_tool_catalog(catalog: Dict[str, Any]) -> Optional[str]:
    if not isinstance(catalog, dict):
        return "tool_catalog must be a dict"
    if not isinstance(catalog.get("categories"), list):
        return "tool_catalog.categories must be a list"
    for c in catalog["categories"]:
        if not isinstance(c, dict):
            return "each category must be a dict"
        if not c.get("id") or not c.get("name"):
            return "each category must include id and name"
        items = c.get("items")
        if items is None:
            continue
        if not isinstance(items, list):
            return f"category {c.get('id')} items must be a list"
        for it in items:
            if not isinstance(it, dict):
                return f"category {c.get('id')} item must be a dict"
            if not it.get("id") or not it.get("name"):
                return f"category {c.get('id')} item must include id and name"
    return None


def build_catalog_injection(catalog: Dict[str, Any], max_chars: int = 2200) -> str:
    policies = catalog.get("policies") if isinstance(catalog.get("policies"), dict) else {}
    prefer_recommended = bool(policies.get("prefer_recommended", True))
    forbid_deprecated = bool(policies.get("forbid_deprecated", True))
    allow_unknown = bool(policies.get("allow_unknown_with_admin_flag", True))

    lines: List[str] = []
    lines.append("[HUMAN_TOOL_CATALOG]")
    lines.append("以下清单由管理员维护，优先以此为准。不要凭空推荐清单外工具。")
    rules = []
    if prefer_recommended:
        rules.append("优先推荐 status=recommended 的选项")
    if forbid_deprecated:
        rules.append("不要推荐 status=deprecated 的选项")
    if allow_unknown:
        rules.append("清单外建议必须标记“需要管理员确认”，不要当作既定事实")
    if rules:
        lines.append("规则：" + "；".join(rules))

    categories = catalog.get("categories", [])
    for c in categories:
        if not isinstance(c, dict):
            continue
        name = c.get("name")
        items = c.get("items", [])
        if not name or not isinstance(items, list) or not items:
            continue
        parts: List[str] = []
        for it in items:
            if not isinstance(it, dict):
                continue
            item_name = it.get("name")
            status = it.get("status")
            if not item_name:
                continue
            tag = f"({status})" if status else ""
            parts.append(f"{item_name}{tag}")
        if parts:
            lines.append(f"- {name}: " + "、".join(parts))

    text = "\n".join(lines).strip()
    if len(text) <= max_chars:
        return text

    truncated: List[str] = []
    size = 0
    for line in lines:
        if size + len(line) + 1 > max_chars:
            break
        truncated.append(line)
        size += len(line) + 1
    if truncated and truncated[-1] != "...":
        truncated.append("...")
    return "\n".join(truncated).strip()


def load_tool_catalog(db_client, config_key: str = "tool_catalog") -> Tuple[Optional[Dict[str, Any]], Optional[str], Optional[Dict[str, Any]]]:
    record = None
    if db_client is not None:
        try:
            getter = getattr(db_client, "get_admin_config_latest", None)
            if callable(getter):
                record = getter(config_key)
        except Exception:
            record = None

    if record and isinstance(record.get("content_json"), dict):
        catalog = record.get("content_json")
        err = validate_tool_catalog(catalog)
        if err is None:
            return catalog, None, record
        return None, err, record

    catalog, err = load_tool_catalog_from_file(DEFAULT_TOOL_CATALOG_PATH)
    if catalog is None:
        return None, err, record
    v_err = validate_tool_catalog(catalog)
    if v_err is not None:
        return None, v_err, record
    return catalog, None, record

