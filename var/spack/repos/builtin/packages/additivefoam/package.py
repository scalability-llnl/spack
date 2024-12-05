# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *
from spack.pkg.builtin.openfoam import add_extra_files


class Additivefoam(Package):
    """AdditiveFOAM is a heat and mass transfer software for Additive Manufacturing (AM)"""

    homepage = "https://github.com/ORNL/AdditiveFOAM"
    git = "https://github.com/ORNL/AdditiveFOAM.git"
    url = "https://github.com/ORNL/AdditiveFOAM/archive/1.0.0.tar.gz"

    maintainers("streeve", "colemanjs", "gknapp1")

    tags = ["ecp"]

    license("GPL-3.0-only")

    version("main", branch="main")
    version("1.0.0", sha256="abbdf1b0230cd2f26f526be76e973f508978611f404fe8ec4ecdd7d5df88724c")

    depends_on("cxx", type="build")  # generated

    depends_on("openfoam-org@10")

    common = ["spack-derived-Allwmake"]
    assets = ["applications/Allwmake", "Allwmake"]

    build_script = "./spack-derived-Allwmake"

    phases = ["configure", "build", "install"]

    def patch(self):
        add_extra_files(self, self.common, self.assets)

    def configure(self, spec, prefix):
        pass

    def build(self, spec, prefix):
        """Build with Allwmake script, wrapped to source environment first."""
        args = []
        if self.parallel:  # Parallel build? - pass via environment
            os.environ["WM_NCOMPPROCS"] = str(make_jobs)
        builder = Executable(self.build_script)
        builder(*args)

    def install(self, spec, prefix):
        """Install under the prefix directory"""

        for f in ["README.md", "LICENSE"]:
            if os.path.isfile(f):
                install(f, join_path(self.prefix, f))

        dirs = ["tutorials", "applications"]
        for d in dirs:
            if os.path.isdir(d):
                install_tree(d, join_path(self.prefix, d), symlinks=True)
