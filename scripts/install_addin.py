#!/usr/bin/env python3
"""Install Brepwright into Autodesk Fusion's user add-ins folder."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ADDIN_SOURCE = REPO_ROOT / "addin" / "Brepwright"


def default_addins_dir() -> Path:
    home = Path.home()
    if (home / "Library").exists():
        return (
            home
            / "Library"
            / "Application Support"
            / "Autodesk"
            / "Autodesk Fusion 360"
            / "API"
            / "AddIns"
        )
    return home / "AppData" / "Roaming" / "Autodesk" / "Autodesk Fusion 360" / "API" / "AddIns"


def copy_addin(target_dir: Path, dry_run: bool) -> None:
    if not ADDIN_SOURCE.exists():
        raise SystemExit(f"Add-in source not found: {ADDIN_SOURCE}")

    target = target_dir / "Brepwright"
    print(f"Source: {ADDIN_SOURCE}")
    print(f"Target: {target}")

    if dry_run:
        print("Dry run: no files copied.")
        return

    target_dir.mkdir(parents=True, exist_ok=True)
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(ADDIN_SOURCE, target)
    print("Installed Brepwright add-in.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, default=default_addins_dir(), help="Fusion AddIns directory")
    parser.add_argument("--dry-run", action="store_true", help="Print paths without copying files")
    args = parser.parse_args()

    copy_addin(args.target.expanduser(), args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
