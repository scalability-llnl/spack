# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *
from spack.util.environment import EnvironmentModifications


class Octa(AutotoolsPackage):
    """OCTA is an integrated simulation system for soft materials."""

    homepage = "https://octa.jp"
    url = (
        "http://49.212.191.63/phpBB/download/file.php?id=3454&sid=3dfae182c664d1f5960d9ca63c40798a"
    )

    version(
        "8.4",
        sha256="b76d25f333fef76601bfe8262e9a748154280d5408ea823fa6530a6f3f86b51b",
        extension="tar.gz",
    )

    variant("withgui", default=True, description="Enables the GUI for GOURMET.")
    variant(
        "engine",
        default="cognac, pasta, sushi, muffin",
        values=("cognac", "pasta", "sushi", "muffin"),
        multi=True,
        description="Simulation programs",
    )

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("mpi")

    with when("+withgui"):
        depends_on("libjpeg", type="link")
        depends_on("libpng", type="link")
        depends_on("zlib", type="link")
        depends_on("jogl")
        depends_on("python")
        depends_on("gnuplot", type="run")
        depends_on("py-numpy")
        depends_on("py-scipy")
        depends_on("py-numba")

    # These patches modify the Makefile to enable building with the Fujitsu compiler on AArch64.
    patch("fj_cognac.patch", when="%fj")
    patch("fj_pasta.patch", when="%fj")

    # This patch modifies the Makefile to enable building with the Fujitsu compiler on AArch64
    # and fixes a missing return statement in the C++ code.
    patch("fj_sushi.patch", when="%fj")

    # This patch modifies the Makefile to enable building with the Fujitsu compiler on AArch64
    # and resolves a reference error with friend functions in the Fujitsu compiler.
    patch("fj_muffin.patch", when="%fj")

    # These patches modify the Makefile to enable building with the GNU compiler on AArch64.
    patch("aarch64gcc_sushi.patch", when="target=aarch64: %gcc")
    patch("aarch64gcc_pasta.patch", when="target=aarch64: %gcc")

    # For jogl 2.3.2 or later
    patch("jogl.patch")
    # patch for non-constant-expression cannot be narrowed error.
    patch("narrowed-initialize.patch")

    configure_directory = join_path("GOURMET", "src")

    def patch(self):
        with working_dir(self.configure_directory):
            copy("jogltest.java_v232", "jogltest.java")

    def setup_build_environment(self, env):
        # download and expand archive previously to load env file
        self.stage.create()
        self.stage.fetch()
        self.stage.expand_archive()

        # add aarch64 support
        if self.spec.target.family == "aarch64":
            filter_file(
                r"(ia64\) S='linux_ia64' ;;)",
                "ia64) S='linux_ia64' ;;\n             aarch64) S='linux_aarch64' ;;",
                join_path(self.stage.source_path, "GOURMET", "src", "pfgetsystem"),
            )
        copy(
            join_path(self.stage.source_path, "GOURMET", "src", "pfgetsystem"),
            join_path(self.stage.source_path, "GOURMET", "bin", "pfgetsystem"),
        )

        octasetup = join_path(self.stage.source_path, "GOURMET", "gourmetterm")
        os.environ["OCTA84_HOME"] = self.stage.source_path
        if os.path.isfile(octasetup):
            env.extend(EnvironmentModifications.from_sourcing_file(octasetup, "-"))

    def setup_run_environment(self, env):
        for dirpath, dirnames, filenames in os.walk(self.prefix.bin):
            env.prepend_path("PATH", dirpath)
        for dirpath, dirnames, filenames in os.walk(self.prefix.lib):
            env.prepend_path("LD_LIBRARY_PATH", dirpath)

    def configure_args(self):
        spec = self.spec
        args = []
        if "+withgui" in spec:
            args = [
                "--with-python={0}".format(spec["python"].command),
                "--with-java-home={0}".format(spec["java"].prefix),
                "--with-jogl-jar={0}".format(spec["jogl"].prefix.lib),
                "--with-jogl-lib={0}".format(spec["jogl"].prefix.lib),
            ]
        return args

    def build(self, spec, prefix):
        pass

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir(self.configure_directory):
            make()
            make("install", parallel=False)

        # Fix install directory
        if spec.variants["engine"]:
            os.environ["PF_FILES"] = prefix
            os.environ["PF_ENGINE"] = prefix

        if spec.satisfies("engine=cognac"):
            build_dir = join_path("ENGINES", "COGNAC1012", "src")
            with working_dir(build_dir):
                make()
                make("install", parallel=False)

        if spec.satisfies("engine=sushi"):
            build_directory = join_path("ENGINES", "SUSHI11.0", "Susi", "src")
            mkdirp(join_path(prefix, "udf"))
            with working_dir(build_directory):
                make(
                    "all",
                    "MPI=ON",
                    "CXX={0}".format(spec["mpi"].mpicxx),
                    "MACHINE={0}".format(spec.target.family),
                )
                make("install", parallel=False)

        if spec.satisfies("engine=pasta"):
            build_directory = join_path("ENGINES", "PASTA", "PASTA", "src")
            with working_dir(build_directory):
                make()
                make("install", parallel=False)

        if spec.satisfies("engine=muffin"):
            build_directory = join_path("ENGINES", "MUFFIN5", "src", "muffin5")
            with working_dir(build_directory):
                make()
                make("install", parallel=False)
