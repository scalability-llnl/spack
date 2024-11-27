# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Revbayes(CMakePackage):
    """Bayesian phylogenetic inference using probabilistic graphical models
    and an interpreted language."""

    homepage = "https://revbayes.github.io"
    url = "https://github.com/revbayes/revbayes/archive/1.1.0.tar.gz"
    git = "https://github.com/revbayes/revbayes.git"

    license("GPL-3.0-only")

    version("develop", branch="development")
    version(
        "1.2.2",
        sha256="339f89169cc9320212c3c64d0557b66f416ec9ae25d45e21a4e9a1cafef6e423",
        url="https://github.com/revbayes/revbayes/archive/refs/tags/v1.2.2.tar.gz",
    )
    version("1.1.1", sha256="d61293fceac817d8203ed1e828661d76c73fa16bf04458a50a37057e99fd40c0")
    version("1.1.0", sha256="a9f35178d8289d0dd32c9d936f6384f260e8e81e7b80a5155169064a24666012")
    version("1.0.13", sha256="e85e2e1fe182fe9f504900150d936a06d252a362c591b9d3d8272dd085aa85d9")
    version("1.0.12", sha256="80c926bb6b37288d02e36e07b44e4663841cd1fe541e2cc0b0e44c89ca929759")
    version("1.0.11", sha256="03052194baa220dde7e622a739f09f34393f67ea00a0b163b409d313d7fc7c02")
    version("1.0.10", sha256="6a3cf303e7224b0b32637bd8e2c3c2cf2621f5dbe599cd74ce4b0c215d0fcd2d")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("mpi", default=True, description="Enable MPI parallel support")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on("mpi", when="+mpi")

    conflicts("%gcc@7.1.0:", when="@:1.0.12")

    def url_for_version(self, version):
        if version > Version("1.0.13"):
            return "https://github.com/revbayes/revbayes/archive/{0}.tar.gz".format(version)
        else:
            return "https://github.com/revbayes/revbayes.archive/archive/v{0}.tar.gz".format(
                version
            )

    @property
    def root_cmakelists_dir(self):
        if self.spec.version > Version("1.0.13"):
            return "src"
        else:
            return "projects/cmake/build"

    @when("@1.1.0:")
    def cmake_args(self):
        args = []
        if "+mpi" in self.spec:
            args.extend([self.define("MPI", "ON"), self.define("RB_EXEC_NAME", "rb-mpi")])
        return args

    @run_before("cmake")
    def regenerate(self):
        with working_dir(join_path("projects", "cmake")):
            mkdirp("build")
            if self.spec.version > Version("1.0.13"):
                generate_version = Executable("./generate_version_number.sh")
                generate_version()
                dest = join_path("..", "..", "src", "revlanguage", "utils")
                install("GitVersion.cpp", dest)
            else:
                edit = FileFilter("regenerate.sh")
                edit.filter('boost="true"', 'boost="false"')
                if "+mpi" in self.spec:
                    edit.filter('mpi="false"', 'mpi="true"')
            regenerate = Executable("./regenerate.sh")
            regenerate()

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        if "+mpi" in spec:
            install_path = join_path(self.build_directory, "..", "rb-mpi")
            install(install_path, prefix.bin)
        else:
            install_path = join_path(self.build_directory, "..", "rb")
            install(install_path, prefix.bin)

    @when("@1.0.12:1.0.13")
    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install_path = join_path(self.build_directory, "..", "rb")
        install(install_path, prefix.bin)
