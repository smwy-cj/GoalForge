"""Prepare native text or a GoalForge source JSON without loading reference labels."""

import argparse
import hashlib
import json
from pathlib import Path


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def prepare(path, document_id=None, canonical_path=None):
    path = Path(path)
    raw = path.read_bytes()
    suffix = path.suffix.lower()
    issues = []
    if suffix == ".json":
        record = json.loads(raw.decode("utf-8-sig"))
        document_id = record["document_id"]
        turns = record["turns"]
        if not turns:
            raise ValueError("Source has no turns")
        canonical = "".join(
            f"[{t['source_id'].split(':', 1)[1]}] {t['speaker']}: {t['text']}\n" for t in turns
        )
        if canonical_path is not None:
            canonical = Path(canonical_path).read_bytes().decode("utf-8")
        if digest(canonical.encode("utf-8")) != record["document_hash"]:
            raise ValueError("Canonical text hash differs from source record")
        segments = []
        for t in turns:
            if not t["source_id"].startswith(document_id + ":"):
                raise ValueError("Cross-document source_id")
            if canonical[t["start_char"]:t["end_char"]] != t["text"]:
                raise ValueError("Source offset mismatch")
            segments.append(dict(source_id=t["source_id"], material_id="M001", text=t["text"],
                                 speaker=t["speaker"], recognition_status="native_text",
                                 original_locator=dict(turn=t["turn"], start_char=t["start_char"], end_char=t["end_char"])))
        method = "保留现有标准原文、轮次与偏移；JSON 仅投影源文字段"
        id_origin = "provided"
    elif suffix in {".md", ".txt"}:
        decoded = raw.decode("utf-8-sig")
        canonical = decoded.replace("\r\n", "\n").replace("\r", "\n")
        id_origin = "provided" if document_id is not None else "generated"
        document_id = document_id or "DOC-" + digest(raw)[:12]
        if raw.startswith(b"\xef\xbb\xbf") or canonical != decoded:
            issues.append("仅移除 UTF-8 BOM 并统一换行为 LF；原件未修改。")
        segments = []
        offset = 0
        for line_number, line in enumerate(canonical.splitlines(keepends=True), 1):
            text = line.rstrip("\n")
            if text.strip():
                sid = f"{document_id}:S{len(segments) + 1:03}"
                segments.append(dict(source_id=sid, material_id="M001", text=text, speaker=None,
                                     recognition_status="native_text", original_locator=dict(
                                         line_start=line_number, line_end=line_number,
                                         start_char=offset, end_char=offset + len(text))))
            offset += len(line)
        method = "UTF-8 原生文本忠实读取，保留行顺序；不做语义摘要"
    else:
        raise ValueError("此工具仅处理 UTF-8 MD/TXT 和源文 JSON；其他格式请使用对应读取或转写工具。")
    if not segments:
        raise ValueError("No readable source text")
    if len({s["source_id"] for s in segments}) != len(segments):
        raise ValueError("Duplicate source_id")
    data = dict(document_id=document_id, document_hash=digest(canonical.encode("utf-8")),
                materials=[dict(material_id="M001", file_name=path.name,
                                media_type={".json": "application/json", ".md": "text/markdown", ".txt": "text/plain"}[suffix],
                                original_hash=digest(raw), id_origin=id_origin, processing_status="processed")],
                conversion=dict(canonical_text_path="source.txt", method=method, issues=issues),
                segments=segments, coverage=dict(scope="provided_material", source_ids=[s["source_id"] for s in segments], omissions=[]))
    return canonical, data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--document-id")
    parser.add_argument("--canonical-text", type=Path)
    args = parser.parse_args()
    canonical, data = prepare(args.input, args.document_id, args.canonical_text)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    outputs = [args.output_dir / "source.txt", args.output_dir / "source-input.json"]
    if any(p.exists() for p in outputs) or args.input.resolve() in {p.resolve() for p in outputs}:
        parser.error("Use a fresh output directory; existing source artifacts will not be overwritten")
    outputs[0].write_bytes(canonical.encode("utf-8"))
    outputs[1].write_bytes((json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


if __name__ == "__main__":
    main()
