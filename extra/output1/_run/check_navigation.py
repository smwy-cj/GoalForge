"""Verify local navigation targets without claiming visual or interaction QA."""
import json
import re
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

OUT = Path(__file__).resolve().parents[1]


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag in ('a', 'link', 'script', 'img'):
            for key, value in attrs:
                if key in ('href', 'src') and value:
                    self.links.append(value)


def main():
    index = json.loads((OUT / '_run/delivery-index.json').read_text(encoding='utf-8'))
    paths = {OUT / p for p in ['README.md', 'index.html', '处理总结.md', 'review/expanded-review.md',
             'review/pilot-comparison.md', 'review/pilot-gate.md', 'review/pilot-v2-followup.md',
             'review/expanded-batch1/report.md', 'review/expanded-batch1/followup.md',
             'review/expanded-batch2/report.md', 'review/expanded-batch2/followup-by-batch3.md',
             'review/expanded-batch3/report.md']}
    for record in index['documents']:
        paths.update(OUT / record[k] for k in ('html', 'markdown'))
    followup=OUT/'review/remaining-20261025'
    if (followup/'summary.json').exists():
        paths.update(followup/p for p in ['README.md','复核总结.md','统一问题清单.md',
                     'batch1/report.md','batch2/report.md','batch3/report.md'])
    checked, errors, ignored = [], [], []
    for path in sorted(paths):
        if not path.exists():
            errors.append(dict(file=path.relative_to(OUT).as_posix(), error='missing document'))
            continue
        text = path.read_text(encoding='utf-8-sig')
        if path.suffix == '.html':
            parser = Links()
            parser.feed(text)
            links = parser.links
        else:
            links = re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)', text)
        for link in links:
            link = link.strip().strip('<>')
            if link.startswith('#'):
                continue
            split = urlsplit(link)
            if split.scheme and split.scheme.lower() not in ('file',):
                ignored.append(link)
                continue
            target = unquote(split.path)
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            item = dict(file=path.relative_to(OUT).as_posix(), target=link, exists=resolved.exists())
            checked.append(item)
            if not item['exists']:
                errors.append(item)
    result = dict(checked_at_utc=datetime.now(timezone.utc).isoformat(),
                  status='passed' if not errors else 'failed', documents=len(paths),
                  local_targets_checked=len(checked), errors=errors,
                  ignored_external_or_data_links=len(ignored),
                  scope='Local file existence only; anchors, browser layout and interactions not tested')
    (OUT / '_run/navigation-verification.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
