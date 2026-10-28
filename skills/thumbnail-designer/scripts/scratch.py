#!/usr/bin/env python3
"""Where working files go.

Proof sheets, overlays, contact sheets and frame dumps are evidence for the person
doing the work. They are not deliverables, and writing them next to the finished
artwork is how a delivery folder ends up with four previews for every real file.

So every script that produces proof output routes it here by default: a per-project
folder under the system temp directory. The script still prints the full path, so
the images can be opened and looked at - which is the whole point of them - but the
output directory the user sees stays clean.

    from scratch import proof_path
    p = proof_path(src, "_safezone.png", here=args.here)

`--here` on any of those scripts puts the file back beside the source, for when
someone genuinely wants the proofs kept.
"""
import os
import tempfile
from pathlib import Path

ROOT_NAME = "designer-proofs"


def proof_dir(src=None):
    """A stable working directory, namespaced by the source file's own folder."""
    root = Path(tempfile.gettempdir()) / ROOT_NAME
    if src:
        tag = Path(src).resolve().parent.name or "work"
        root = root / tag
    root.mkdir(parents=True, exist_ok=True)
    return root


def proof_path(src, suffix, here=False):
    """Full path for a proof artefact derived from `src`.

    suffix may start with '_' (appended to the stem) or '.' (replaces the extension).
    """
    src = Path(src)
    name = src.stem + suffix if suffix.startswith("_") else src.stem + suffix
    if here:
        return str(src.parent / name)
    return str(proof_dir(src) / name)


def clean(src=None):
    """Remove this project's proof folder. Never touches anything outside temp."""
    import shutil
    d = proof_dir(src)
    if Path(tempfile.gettempdir()) in d.parents:
        shutil.rmtree(d, ignore_errors=True)
        return str(d)
    return None


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--clean":
        print("removed", clean(sys.argv[2] if len(sys.argv) > 2 else None))
    else:
        print(proof_dir())
