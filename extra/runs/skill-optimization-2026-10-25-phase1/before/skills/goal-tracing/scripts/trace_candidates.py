"""Compatibility entrypoint; maintained implementation lives in goal-extraction."""
import importlib.util
from pathlib import Path

_target = Path(__file__).resolve().parents[2] / 'goal-extraction/scripts/trace_candidates.py'
if not _target.is_file() or _target.resolve() == Path(__file__).resolve():
    raise RuntimeError('GoalForge compatibility target unavailable: ' + str(_target))
_spec = importlib.util.spec_from_file_location('_goalforge_extraction_trace', _target)
_implementation = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_implementation)
globals().update({name: value for name, value in vars(_implementation).items() if not name.startswith('_')})

if __name__ == '__main__':
    _implementation.main()
