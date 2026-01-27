import re
from typing import List, Dict


_FILE_HEADER_RE = re.compile(r"^\s*===\s*FILE:\s*(?P<name>[^=]+?)\s*===\s*$", re.MULTILINE)


def split_deliverables(raw_text: str) -> List[Dict[str, str]]:
    text = (raw_text or "").strip()
    if not text:
        return []

    matches = list(_FILE_HEADER_RE.finditer(text))
    if not matches:
        return [{"file_name": "Maia_Deliverables.md", "content": text}]

    docs: List[Dict[str, str]] = []
    for i, m in enumerate(matches):
        file_name = (m.group("name") or "").strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = text[start:end].strip()
        if not file_name:
            continue
        if not content:
            continue
        docs.append({"file_name": file_name, "content": content})

    return docs

