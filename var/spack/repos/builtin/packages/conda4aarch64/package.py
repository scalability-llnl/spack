# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.util.environment import EnvironmentModifications


class Conda4aarch64(Package):
    """Conda for aarch64"""

    homepage = "https://anaconda.org/c4aarch64/"
    url = "https://github.com/jjhelmus/conda4aarch64/releases/download/1.0.0/c4aarch64_installer-1.0.0-Linux-aarch64.sh"

    conflicts("arch=x86_64:")
    conflicts("arch=ppc64:")
    conflicts("arch=ppc64le:")

    version(
        "1.0.0",
        sha256="165565dc7e7cc74c9ef8fd75d309fb7b81a6d1bc5e2eab48aafa7b836a7427af",
        expand=False,
    )

    def install(self, spec, prefix):
        conda_script = self.stage.archive_file
        bash = which("bash")
        bash(conda_script, "-b", "-f", "-p", self.prefix)

    def setup_run_environment(self, env):
        filename = self.prefix.etc.join("profile.d").join("conda.sh")
        env.extend(EnvironmentModifications.from_sourcing_file(filename))
