# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import inspect
import os

import llnl.util.tty as tty

import spack.pkg.builtin.openfoam as openfoam
from spack.package import *
from spack.version import Version


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
    assets = [join_path("applications", "Allwmake"), "Allwmake"]

    build_script = "./spack-derived-Allwmake"

    phases = ["configure", "build", "install"]

    def add_extra_files(self, common, local_prefix, local):
        """Copy additional common and local files into the stage.source_path
        from the openfoam/common and the package/assets directories,
        respectively. Modified from `spack.pkg.builtin.openfoam.add_extra_files()`.
        """
        outdir = self.stage.source_path
        indir = join_path(os.path.dirname(inspect.getfile(openfoam)), "common")
        for f in common:
            tty.info("Added file {0}".format(f))
            openfoam.install(join_path(indir, f), join_path(outdir, f))

        indir = join_path(self.package_dir, "assets", local_prefix)
        for f in local:
            tty.info("Added file {0}".format(f))
            openfoam.install(join_path(indir, f), join_path(outdir, f))

    def patch(self):
        spec = self.spec
        asset_dir = ""
        if Version("main") in spec.versions:
            asset_dir = "assets_main"
        elif Version("1.0.0") in spec.versions:
            asset_dir = "assets_1.0.0"
        self.add_extra_files(self.common, asset_dir, self.assets)

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
