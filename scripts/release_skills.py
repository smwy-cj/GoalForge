"""Build, verify and install an exact three-skill release without overwriting edits."""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

SKILLS = ('goal-extraction', 'goal-model-building', 'model-review')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encode(data):
    return (json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf-8')


def require(condition, message):
    if not condition: raise ValueError(message)


def skill_files(root):
    files={}
    for name in SKILLS:
        require((root/name/'SKILL.md').is_file(),'Missing skill: '+name)
        for path in sorted((root/name).rglob('*')):
            if path.is_file() and '__pycache__' not in path.parts and path.suffix!='.pyc':
                require(not path.is_symlink() and (root/name).resolve() in path.resolve().parents,'Unsafe skill file')
                files[path.relative_to(root).as_posix()]=path.read_bytes()
    return files


def build(source, output, version):
    source,output=Path(source).resolve(),Path(output).resolve()
    require(not output.exists(),'Use a new release directory')
    require(isinstance(version,str) and version.strip(),'Release version required')
    files=skill_files(source)
    manifest=dict(schema_version='goalforge-skills-release-1',version=version,skills=list(SKILLS),
                  files=[dict(path='skills/'+name,sha256=sha(raw)) for name,raw in files.items()])
    output.mkdir(parents=True)
    for name,raw in files.items():
        target=output/'skills'/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
    manifest_raw=encode(manifest);(output/'manifest.json').write_bytes(manifest_raw)
    with zipfile.ZipFile(output/'goalforge-skills.zip','x',compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr('manifest.json',manifest_raw)
        for name,raw in files.items():archive.writestr('skills/'+name,raw)
    require(files==skill_files(source),'Source skills changed during release build; freeze and rebuild')
    return verify(output)


def verify(release):
    release=Path(release).resolve()
    manifest_raw=(release/'manifest.json').read_bytes();manifest=json.loads(manifest_raw)
    require(manifest.get('schema_version')=='goalforge-skills-release-1' and manifest.get('skills')==list(SKILLS),'Invalid release schema/skills')
    declared={}
    for item in manifest['files']:
        name=item['path'];parts=PurePosixPath(name).parts
        require(not PurePosixPath(name).is_absolute() and len(parts)>=3 and parts[0]=='skills' and parts[1] in SKILLS
                and '\\' not in name and ':' not in name and '..' not in parts and name not in declared,'Unsafe or duplicate release path')
        path=release/name
        require(release in path.resolve().parents and not path.is_symlink(),'Release path escapes package')
        raw=path.read_bytes();require(sha(raw)==item['sha256'],'Release hash mismatch: '+name);declared[name]=raw
    actual={'skills/'+name:raw for name,raw in skill_files(release/'skills').items()}
    require(actual==declared,'Missing or extra skill files')
    require(not (release/'skills/goal-tracing').exists(),'Legacy tracing must not enter release')
    with zipfile.ZipFile(release/'goalforge-skills.zip') as archive:
        require(len(archive.namelist())==len(set(archive.namelist())) and set(archive.namelist())==set(declared)|{'manifest.json'},'Archive members differ')
        require(archive.read('manifest.json')==manifest_raw,'Archive manifest mismatch')
        require(all(archive.read(name)==raw for name,raw in declared.items()),'Archive bytes differ')
    return dict(status='passed',version=manifest['version'],files=len(declared),
                manifest_sha256=sha(manifest_raw),archive_sha256=sha((release/'goalforge-skills.zip').read_bytes()))


def verify_installed(release, destination):
    result=verify(release);release,destination=Path(release).resolve(),Path(destination).resolve()
    require(skill_files(release/'skills')==skill_files(destination),'Installed bytes differ from frozen release')
    with tempfile.TemporaryDirectory(prefix='goalforge-import-check-') as tmp:
        code='import json,sys;sys.path.insert(0,sys.argv[1]);import kaos_model,trace_candidates,simple_candidates;print(json.dumps(dict(kaos_model=kaos_model.__file__,trace_candidates=trace_candidates.__file__,simple_candidates=simple_candidates.__file__,schema=kaos_model.SCHEMA2)))'
        process=subprocess.run([sys.executable,'-X','utf8','-c',code,str(destination/'goal-model-building/scripts')],
                               cwd=tmp,capture_output=True,text=True,encoding='utf-8',timeout=30)
        require(process.returncode==0,'Installed import failed: '+process.stderr)
        loaded=json.loads(process.stdout)
        for name in ('kaos_model','trace_candidates','simple_candidates'):
            require(destination in Path(loaded[name]).resolve().parents,'Loaded code outside installation')
    result.update(destination=str(destination),loaded=loaded,application_discovery='not_asserted')
    return result


def install(release, destination):
    verify(release);release,destination=Path(release).resolve(),Path(destination).resolve()
    require(not any((destination/name).exists() for name in SKILLS),'Existing skill directories are preserved; choose a fresh location or explicitly archive them first')
    require(not destination.exists() or destination.is_dir(),'Installation destination is not a directory')
    destination.mkdir(parents=True,exist_ok=True)
    for name in SKILLS:
        shutil.copytree(release/'skills'/name,destination/name,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    return verify_installed(release,destination)


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('build');p.add_argument('source',type=Path);p.add_argument('output',type=Path);p.add_argument('--version',required=True)
    p=sub.add_parser('verify');p.add_argument('release',type=Path)
    for name in ('install','verify-installed'):
        p=sub.add_parser(name);p.add_argument('release',type=Path);p.add_argument('destination',type=Path)
    args=parser.parse_args()
    try:
        result=(build(args.source,args.output,args.version) if args.command=='build' else verify(args.release) if args.command=='verify'
                else install(args.release,args.destination) if args.command=='install' else verify_installed(args.release,args.destination))
        print(json.dumps(result,ensure_ascii=False,indent=2))
    except (ValueError,OSError,KeyError,zipfile.BadZipFile) as exc:parser.exit(2,str(exc)+'\n')


if __name__=='__main__':main()
