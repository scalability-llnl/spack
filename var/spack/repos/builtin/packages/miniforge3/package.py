# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform
from os.path import split

from spack.package import *
from spack.util.environment import EnvironmentModifications

_versions = {
    "24.3.0-0": {
        "Linux-x86_64": ("23367676b610de826f50f7ddc91139a816d4b59bd4c69cc9b6082d9b2e7fe8a3",)
    },
    "24.1.2-0": {
        "Linux-x86_64": ("dbadb808edf4da00af35d888d3eeebbfdce71972b60bf4b16dbacaee2ab57f28",)
    },
    "4.8.3-4": {
        "Linux-x86_64": ("24951262a126582f5f2e1cf82c9cd0fa20e936ef3309fdb8397175f29e647646",),
        "Linux-aarch64": ("52a8dde14ecfb633800a2de26543a78315058e30f5883701da1ad2f2d5ba9ed8",),
    },
    "4.8.3-2": {
        "Linux-x86_64": ("c8e5b894fe91ce0f86e61065d2247346af107f8d53de0ad89ec848701c4ec1f9",),
        "Linux-aarch64": ("bfefc0ede6354568978b4198607edd7f17c2f50ca4c6a47e9f22f8c257c8230a",),
        "MacOSX-x86_64": ("25ca082ab00a776db356f9bbc660edf6d24659e2aec1cbec5fd4ce992d4d193d"),
    },
}


class Miniforge3(Package):
    """Miniforge3 is a minimal installer for conda and mamba specific to conda-forge."""

    homepage = "https://github.com/conda-forge/miniforge"

    maintainers("ChristopherChristofi")

    license("BSD-3-Clause")

    for ver, packages in _versions.items():
        key = f"{platform.system()}-{platform.machine()}"
        pkg = packages.get(key)
        if pkg:
            version(ver, sha256=pkg[0], expand=False)

    variant("mamba", default=True, description="Enable mamba support.")

    conflicts("+mamba", when="@:22.3.1-0")

    def url_for_version(self, version):
        script = f"Miniforge3-{version}-{platform.system()}-{platform.machine()}.sh"
        return f"https://github.com/conda-forge/miniforge/releases/download/{version}/{script}"

    def install(self, spec, prefix):
        dir, script = split(self.stage.archive_file)
        bash = which("bash")
        bash(script, "-b", "-f", "-p", self.prefix)

    @run_after("install")
    def patch_sbang(self):
        # Conda replaces the full path to the Python executable with `/usr/bin/env python`
        # if the full path exceeds 127 characters. This does however break `conda deactivate`
        # because the wrong Python interpreter is used after activating an environment.
        # The 127 character limit is not relevant in Spack as Spack will automatically
        # use the `sbang` script to deal with the overly long sbang line.
        filter_file(
            r"#!/usr/bin/env python", rf"#!{self.prefix.bin.python}", self.prefix.bin.conda
        )
        if "+mamba" in self.spec:
            filter_file(
                r"#!/usr/bin/env python", rf"#!{self.prefix.bin.python}", self.prefix.bin.mamba
            )

    def setup_run_environment(self, env):
        filename = self.prefix.etc.join("profile.d").join("conda.sh")
        env.extend(EnvironmentModifications.from_sourcing_file(filename))

        if "+mamba" in self.spec:
            filename = self.prefix.etc.join("profile.d").join("mamba.sh")
            env.extend(EnvironmentModifications.from_sourcing_file(filename))
