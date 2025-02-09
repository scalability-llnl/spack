# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import json
import os.path as osp

from spack.error import UnsupportedPlatformError
from spack.package import *


class Anaconda3(Package):
    """Anaconda is a free and open-source distribution of the Python and R
    programming languages for scientific computing, that aims to simplify
    package management and deployment. Package versions are managed by
    the package management system conda.
    """

    homepage = "https://www.anaconda.com"
    url = "https://repo.anaconda.com/archive"

    maintainers("ajkotobi", "kftsehk")

    # * To maintainers:
    # To add a new version of Anaconda3
    #   1. Copy https://repo.anaconda.com/archive to anaconda-archive.dat
    #   2. Run `python3 anaconda-archive.py anaconda-archive.dat > versions.json`
    #   3. Paste the checksum for versions.json below

    VERSION_FILE = osp.join(osp.dirname(__file__), "versions.json")
    with open(VERSION_FILE, encoding="utf-8") as f:
        ANACONDA3_VERSIONS = json.load(f)

    for _tmp_platform, _tmp_targets in ANACONDA3_VERSIONS.items():
        for _tmp_target, _tmp_versions in _tmp_targets.items():
            for _tmp_idx, (_tmp_version, _tmp_attrs) in enumerate(_tmp_versions.items()):
                # * Hack: Workaround for platform-specific installer
                # Checksum for source-code is the checksum for `VERSION_FILE`
                # containing checksums for all installer variants
                # from https://repo.anaconda.com/archive
                version(
                    _tmp_version,
                    preferred=_tmp_idx == 0,
                    # deprecate version older than ~3-4 years
                    deprecated=int(_tmp_version.split(".")[0]) < 2021,
                    extension="json",
                    expand=False,
                    url="file://{0}".format(VERSION_FILE),
                    checksum="95c2a6cbc0ffba9823be9674f96e5e775f057f0e39d5637a8e0227524f43f0d7",
                )
                # * Hack: Workaround for platform-specific installer
                # Create a resource for each platform-specific installer
                # from the checksumed `VERSION_FILE` file
                # Resource is matched for
                # - version
                # - platform
                # - target (range match for x86_64 family/microarchs)
                resource(
                    name="anaconda3-{0}-{1}-{2}".format(_tmp_version, _tmp_platform, _tmp_target),
                    when="@{0} platform={1} target={2}".format(
                        _tmp_version,
                        _tmp_platform,
                        # all x86_64 family/microarchs are coerced to x86_64
                        "{0}:".format(_tmp_target) if _tmp_target == "x86_64" else _tmp_target,
                    ),
                    url="https://repo.anaconda.com/archive/{0}".format(
                        _tmp_attrs["installer_name"]
                    ),
                    extension="sh",
                    sha256=_tmp_attrs["sha256"],
                    expand=False,
                )

    def install(self, spec, prefix):
        if len(self.stage) != 2:
            raise UnsupportedPlatformError(
                "Anaconda3 resource stage should match exactly 1 installer, "
                "if your arch family is not x86_64, "
                "have a look at the hack used in package.py"
            )
        anaconda_script = self.stage[1].resource.fetcher.archive_file
        bash = which("bash")
        bash(anaconda_script, "-b", "-f", "-p", self.prefix)

    @run_after("install")
    def postinstall(self):
        # Fix conda command interpreter to conda built-in python3
        filter_file(
            '"$CONDA_EXE" $_CE_M $_CE_CONDA "$@"',
            '{0} $CONDA_EXE $_CE_M $_CE_CONDA "$@"'.format(osp.join(self.prefix.bin, "python3")),
            osp.join(self.prefix, "etc", "profile.d", "conda.sh"),
            string=True,
        )

    def setup_run_environment(self, env):
        filename = self.prefix.etc.join("profile.d").join("conda.sh")
        env.extend(EnvironmentModifications.from_sourcing_file(filename))
