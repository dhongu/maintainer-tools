"""Set the images key in addons manifests."""
import os
import re

import click

from .manifest import get_manifest_path, parse_manifest


IMAGES_KEY_RE = re.compile(r"""(["']images["']\s*:\s*][["'])([^"']*)(["'])""")


@click.command()
@click.argument("path")
@click.option("--addons-dir", default=".")
def main(path, addons_dir):
    for addon_dir in os.listdir(addons_dir):
        manifest_path = get_manifest_path(os.path.join(addons_dir, addon_dir))
        if not manifest_path:
            continue
        try:
            with open(manifest_path) as manifest_file:
                manifest = parse_manifest(manifest_file.read())
        except Exception:
            raise click.ClickException(
                "Error parsing manifest {}.".format(manifest_path)
            )
        if "images" not in manifest:
            raise click.ClickException(
                "images key not found in manifest in {}.".format(addon_dir)
            )
        with open(manifest_path) as manifest_file:
            manifest_str = manifest_file.read()
        new_manifest_str, n = IMAGES_KEY_RE.subn(
            r"\g<1>" + path + r"\g<3>", manifest_str
        )
        if n == 0:
            raise click.ClickException(
                "no images key match in manifest in {}.".format(addon_dir)
            )
        if n > 1:
            raise click.ClickException(
                "more than one images key match in manifest in {}.".format(addon_dir)
            )
        if new_manifest_str != manifest_str:
            with open(manifest_path, "w") as manifest_file:
                manifest_file.write(new_manifest_str)
