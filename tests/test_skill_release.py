"""Exact installation, no legacy dependency, package integrity and no overwrite."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('release_skills',ROOT/'scripts/release_skills.py')
r=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(r)


class ReleaseTests(unittest.TestCase):
    def test_release_installs_exact_three_skills_and_imports_from_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            base=Path(tmp);release=base/'release';destination=base/'isolated/skills'
            result=r.build(ROOT/'skills',release,'test-kaos2')
            self.assertEqual(result['status'],'passed')
            receipt=r.install(release,destination)
            self.assertEqual(receipt['loaded']['schema'],'goalforge-kaos-2')
            self.assertFalse((destination/'goal-tracing').exists())
            source=(destination/'goal-extraction/SKILL.md').read_bytes()
            with self.assertRaises(ValueError):r.install(release,destination)
            self.assertEqual((destination/'goal-extraction/SKILL.md').read_bytes(),source)
            with self.assertRaises(ValueError):r.build(ROOT/'skills',release,'test-kaos2')

    def test_tamper_and_escaping_manifest_are_rejected_before_install(self):
        for variant in ('tamper','escape','extra'):
            with self.subTest(variant=variant),tempfile.TemporaryDirectory() as tmp:
                base=Path(tmp);release=base/'release';r.build(ROOT/'skills',release,'test')
                if variant=='tamper':(release/'skills/goal-extraction/SKILL.md').write_bytes(b'changed')
                elif variant=='extra':(release/'skills/goal-extraction/extra.txt').write_bytes(b'extra')
                else:
                    m=json.loads((release/'manifest.json').read_bytes());m['files'][0]['path']='skills/goal-extraction/../../../outside'
                    (release/'manifest.json').write_bytes(r.encode(m))
                with self.assertRaises(ValueError):r.install(release,base/'install')
                self.assertFalse((base/'install').exists())


if __name__=='__main__':unittest.main()
