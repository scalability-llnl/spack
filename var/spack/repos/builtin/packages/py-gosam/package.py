# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGosam(Package):
    """The package GoSam allows for the automated calculation of
    one-loop amplitudes for multi-particle processes in renormalizable
    quantum field theories."""

    homepage = "https://github.com/gudrunhe/gosam"
    git = "https://github.com/gudrunhe/gosam.git"

    tags = ["hep"]

    extends("python")

    license("GPL-3.0-only")

    version(
        "2.1.1",
        url="https://github.com/gudrunhe/gosam/releases/download/2.1.1/gosam-2.1.1-4b98559.tar.gz",
        sha256="4a2b9160d51e3532025b9579a4d17d0e0f8a755b8481aeb8271c1f58eb97ab01",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("form", type="run")
    depends_on("qgraf", type="run")
    depends_on("gosam-contrib", type="link")
    depends_on("python@3:", type=("build", "run"))

    def setup_run_environment(self, env):
        gosam_contrib_lib_dir = self.spec["gosam-contrib"].prefix.lib
        env.prepend_path("LD_LIBRARY_PATH", gosam_contrib_lib_dir)

    def install(self, spec, prefix):
        python("-s", "setup.py", "--no-user-cfg", "build")
        python("-s", "setup.py", "--no-user-cfg", "install", "--prefix=" + prefix)
