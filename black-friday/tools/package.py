"""Create a deployable static package; omit preview tooling, tests and snapshots."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

root = Path(__file__).resolve().parents[1]
out = root / 'release/nmc-black-friday.zip'
out.parent.mkdir(exist_ok=True)
files = [root / name for name in ('index.html', 'polish.css', 'campaign.js', 'overlay-bridge.js', 'homepage-overlay.js')]
files += sorted((root / 'assets').glob('*.jpg'))
with ZipFile(out, 'w', ZIP_DEFLATED) as archive:
    for path in files:
        archive.write(path, 'black-friday/' + str(path.relative_to(root)))
print(out)
