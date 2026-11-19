from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
out = Path('/output')
out.mkdir(parents=True, exist_ok=True)
shutil.copyfile(ROOT / 'entry.png', out / 'entry.png')
