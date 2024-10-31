# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import llnl.util.tty as tty

from spack.package import *
from spack.pkg.builtin.openfoam import add_extra_files


class OfPrecice(Package):
    """preCICE adapter for OpenFOAM"""

    homepage = "https://precice.org/"
    git = "https://github.com/precice/openfoam-adapter.git"
    url = "https://github.com/precice/openfoam-adapter/archive/v1.2.3.tar.gz"
    maintainers("MakisH", "kjrstory")

    license("GPL-3.0-only")

    version("develop", branch="develop")
    version("master", branch="master")
    version("1.2.3", sha256="e5fbbc633a573cd1a952a98f7f05078a384078a8ea9cd166825148538a23683e")
    version("1.2.2", sha256="9d2d8d372b39c4e672e6311e92545d335c52c8eb3cefea34a794572523583aa5")
    version("1.2.1", sha256="12772ddea1eb0155ebf6d0a2ea4cd9700dbe63a0df016771b39591ae12efad11")
    version("1.2.0", sha256="4e7676cffe12380cda7af32e84a7727dc4c9133815d3b0e1c22150a2e7b34ce0")
    version("1.1.0", sha256="c35340b50d1b01978635130da94a876e1fa846c80b62e45204aa727db2ef4983")
    version("1.0.0", sha256="b70e5bdce47328f789f76dc6187604f8568b4a996158b5a6f6c11f111ff10308")

    depends_on("cxx", type="build")  # generated

    depends_on("openfoam+source")
    depends_on("precice")
    depends_on("yaml-cpp")
    depends_on("pkgconfig", type="build")

    # General patches
    common = ["change-userdir.sh", "spack-derived-Allwmake"]
    assets = []  # type: List[str]

    build_script = "./spack-derived-Allwmake"
    build_userdir = "spack-userdir"  # Build user APPBIN, LIBBIN into here

    phases = ["configure", "build", "install"]

    #
    # - End of definitions / setup -
    #

    def patch(self):
        """Copy additional files or other patching."""
        add_extra_files(self, self.common, self.assets)
        # Emit openfoam version immediately, if we resolved the wrong version
        # it takes a very long time to rebuild!
        tty.info(
            "Build for "
            + self.spec["openfoam"].format("{name}{@version}{%compiler}{compiler_flags}{variants}")
        )

    def configure(self, spec, prefix):
        """Generate spack-config.sh file."""
        # Local tweaks
        # This is ugly, but otherwise it only looks for src/precice,
        # not the installed include files
        config = join_path(self.stage.source_path, "spack-config.sh")
        with open(config, "w") as out:
            out.write(
                """# Local tweaks for building
CPLUS_INCLUDE_PATH="{precice_dir}/include/precice${{CPLUS_INCLUDE_PATH:+:}}$CPLUS_INCLUDE_PATH"
export CPLUS_INCLUDE_PATH
# Local build (for user appbin, libbin)
. ./change-userdir.sh $PWD/{user_dir}
#
""".format(
                    precice_dir=spec["precice"].prefix, user_dir=self.build_userdir
                )
            )

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

        # Place directly under 'lib' (no bin)
        install_tree(join_path(self.build_userdir, "lib"), join_path(self.prefix, "lib"))

    def setup_run_environment(self, env):
        env.prepend_path("LD_LIBRARY_PATH", join_path(self.prefix, "lib"))
