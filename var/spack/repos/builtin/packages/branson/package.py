# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Branson(CMakePackage):
    """Branson's purpose is to study different algorithms for parallel Monte
    Carlo transport. Currently it contains particle passing and mesh passing
    methods for domain decomposition."""

    homepage = "https://github.com/lanl/branson"
    url = "https://github.com/lanl/branson/archive/0.82.tar.gz"
    git = "https://github.com/lanl/branson.git"

    tags = ["proxy-app"]

    license("MIT")

    version("develop", branch="develop")

    version("1.01", sha256="90208eaec4f6d64a4fd81cd838e30b5e7207246cb7f407e482965f23bbcee848")
    version(
        "0.82",
        sha256="7d83d41d0c7ab9c1c906a902165af31182da4604dd0b69aec28d709fe4d7a6ec",
        preferred=True,
    )
    version("0.81", sha256="493f720904791f06b49ff48c17a681532c6a4d9fa59636522cf3f9700e77efe4")
    version("0.8", sha256="85ffee110f89be00c37798700508b66b0d15de1d98c54328b6d02a9eb2cf1cb8")

    depends_on("cxx", type="build")  # generated

    depends_on("mpi@2:")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, when="@:0.81")
    depends_on("metis")
    depends_on("parmetis", when="@:0.81")

    root_cmakelists_dir = "src"

    def cmake_args(self):
        spec = self.spec
        args = []
        args.append(f"-DCMAKE_C_COMPILER={spec['mpi'].mpicc}")
        args.append(f"-DCMAKE_CXX_COMPILER={spec['mpi'].mpicxx}")
        args.append(f"-DCMAKE_Fortran_COMPILER={spec['mpi'].mpifc}")
        return args

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdir(prefix.doc)
        install(join_path(self.build_directory, "BRANSON"), prefix.bin)
        install("LICENSE.md", prefix.doc)
        install("README.md", prefix.doc)
