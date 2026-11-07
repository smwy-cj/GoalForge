"""Prepare native text or a GoalForge source JSON without loading reference labels."""

import argparse
import hashlib
import json
from pathlib import Path


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def encode(data):
    return (json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def validate_segments(data, canonical):
    """Check the shared canonical coordinate system before cutting any windows."""
    if digest(canonical.encode("utf-8")) != data["document_hash"]:
        raise ValueError("Canonical text hash differs from source record")
    segments = data["segments"]
    if not segments or len({s["source_id"] for s in segments}) != len(segments):
        raise ValueError("Empty source or duplicate source_id")
    previous_end = 0
    for segment in segments:
        loc = segment["original_locator"]
        start, end = loc.get("start_char"), loc.get("end_char")
        if (type(start) is not int or type(end) is not int
                or not 0 <= previous_end <= start <= end <= len(canonical)
                or canonical[start:end] != segment["text"]):
            raise ValueError("Invalid, overlapping or out-of-order source offsets")
        if not segment["source_id"].startswith(data["document_id"] + ":"):
            raise ValueError("Cross-document source_id")
        previous_end = end
    return segments


def build_windows(data, canonical, size=4, stride=2, source_input_sha256=None):
    """Overlapping source units; never summarize or forward annotation fields."""
    if type(size) is not int or type(stride) is not int or not 1 <= stride <= size:
        raise ValueError("Window size/stride must be positive integers with stride <= size")
    segments = validate_segments(data, canonical)
    windows = []
    for offset in range(0, len(segments), stride):
        chunk = segments[offset:offset + size]
        start = chunk[0]["original_locator"]["start_char"]
        end = chunk[-1]["original_locator"]["end_char"]
        windows.append(dict(
            window_id=f"{data['document_id']}:W{len(windows) + 1:04}",
            source_ids=[s["source_id"] for s in chunk], start_char=start, end_char=end,
            text=canonical[start:end], segments=[dict(
                source_id=s["source_id"], speaker=s.get("speaker"), text=s["text"],
                start_char=s["original_locator"]["start_char"],
                end_char=s["original_locator"]["end_char"],
                window_start_char=s["original_locator"]["start_char"] - start,
                window_end_char=s["original_locator"]["end_char"] - start,
            ) for s in chunk]))
        # The last window reaches the end; do not emit a redundant tail window.
        if offset + size >= len(segments):
            break
    return dict(schema_version="goalforge-source-windows-1", document_id=data["document_id"],
                input_binding=dict(document_hash=data["document_hash"],
                                   source_input_sha256=source_input_sha256),
                parameters=dict(size=size, stride=stride, unit=("turn" if all(
                    "turn" in s["original_locator"] for s in segments) else "segment")),
                windows=windows)


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
    validate_segments(data, canonical)
    return canonical, data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--document-id")
    parser.add_argument("--canonical-text", type=Path)
    parser.add_argument("--window-size", type=int, help="Also write source-windows.json; e.g. 4 turns/segments")
    parser.add_argument("--window-stride", type=int, help="Defaults to min(2, size); must not exceed size")
    args = parser.parse_args()
    if args.window_stride is not None and args.window_size is None:
        parser.error("--window-stride requires --window-size")
    canonical, data = prepare(args.input, args.document_id, args.canonical_text)
    outputs = [args.output_dir / "source.txt", args.output_dir / "source-input.json"]
    payloads = [canonical.encode("utf-8"), encode(data)]
    if args.window_size is not None:
        stride = args.window_stride if args.window_stride is not None else min(2, args.window_size)
        try:
            windows = build_windows(data, canonical, args.window_size, stride, digest(payloads[1]))
        except ValueError as exc:
            parser.error(str(exc))
        outputs.append(args.output_dir / "source-windows.json")
        payloads.append(encode(windows))
    if any(p.exists() for p in outputs) or args.input.resolve() in {p.resolve() for p in outputs}:
        parser.error("Use a fresh output directory; existing source artifacts will not be overwritten")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for path, raw in zip(outputs, payloads):
        with path.open("xb") as handle:
            handle.write(raw)


if __name__ == "__main__":
    main()
