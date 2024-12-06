# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.package import *


class Codecov(Package):
    """Codecov uploads coverage reports to Codecov for processing."""

    homepage = "https://codecov.io"

    _versions = {
        "0.4.1": {
            "linux": {
                "x86_64": "32cb14b5f3aaacd67f4c1ff55d82f037d3cd10c8e7b69c051f27391d2e66e15c"
            },
            "darwin": {
                "x86_64": "4ab0f06f06e9c4d25464f155b0aff36bfc1e8dbcdb19bfffd586beed1269f3af"
            },
            "windows": {
                "x86_64": "e0cda212aeaebe695509ce8fa2d608760ff70bc932003f544f1ad368ac5450a8"
            },
        }
    }

    system = platform.system().lower()
    machine = platform.machine().lower()

    for ver in _versions:
        if system in _versions[ver] and machine in _versions[ver][system]:
            version(ver, sha256=_versions[ver][system][machine], expand=False)

    def url_for_version(self, version):
        _url_base = f"https://github.com/codecov/uploader/releases/download/v{version}/codecov"
        return _url_base + ".exe" if self.system == "windows" else _url_base + f"-{self.system}"

    def install(self, spec, prefix):
        codecov = self.stage.archive_file
        chmod = which("chmod")
        chmod("+x", codecov)
        mkdirp(prefix.bin)
        install(codecov, prefix.bin.codecov)
