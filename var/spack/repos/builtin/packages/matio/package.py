# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Matio(AutotoolsPackage):
    """matio is an C library for reading and writing Matlab MAT files"""

    homepage = "https://sourceforge.net/projects/matio/"
    git = "https://github.com/tbeu/matio"
    url = "https://github.com/tbeu/matio/releases/download/v1.5.9/matio-1.5.9.tar.gz"

    license("BSD-2-Clause")

    version("1.5.26", sha256="8b47c29f58e468dba7a5555371c6a72ad4c6aa8b15f459b2b0b65a303c063933")
    version("1.5.17", sha256="5e455527d370ab297c4abe5a2ab4d599c93ac7c1a0c85d841cc5c22f8221c400")
    version("1.5.16", sha256="47ba3d5d269d5709b8d9a7385c88c8b5fb5ff875ef781a1ced4892b5b03c4f44")
    version("1.5.15", sha256="21bf4587bb7f0231dbb4fcc88728468f1764c06211d5a0415cd622036f09b1cf")
    version("1.5.14", sha256="0b3abb98f5cd75627122a72522db4e4280eb580bdbeafe90a8a0d2df22801f6e")
    version("1.5.13", sha256="feadb2f54ba7c9db6deba8c994e401d7a1a8e7afd0fe74487691052b8139e5cb")
    version("1.5.12", sha256="8695e380e465056afa5b5e20128935afe7d50e03830f9f7778a72e1e1894d8a9")
    version("1.5.11", sha256="0ccced0c55c9c2cdc21348b7e16447843402d729ffaadd6135767faad7c9cf0b")
    version("1.5.10", sha256="41209918cebd8cc87a4aa815fed553610911be558f027aee54af8b599c78b501")
    version("1.5.9", sha256="beb7f965831ec5b4ef43f8830ee1ef1c121cd98e11b0f6e1d98713d9f860c05c")
    version("1.5.8", sha256="6e49353d1d9d5127696f2e67b46cf9a1dc639663283c9bc4ce5280489c03e1f0")
    version("1.5.7", sha256="84b9a17ada1ee08374fb47cc2d0e10a95b8f7f603b58576239f90b8c576fad48")
    version("1.5.6", sha256="39a6e6a40d9fd8d707f4494483b8df30ffd617ba0a19c663e3685ad55ff55878")
    version("1.5.5", sha256="72f00cc3cd8f7603c48867887cef886289f1f04a30f1c777aeef0b9ddd7d9c9d")
    version("1.5.4", sha256="90d16dfea9070d241ef5818fee2345aee251a3c55b86b5d0314967e61fcd18ef")
    version("1.5.3", sha256="85ba46e192331473dc4d8a9d266679f8f81e60c06debdc4b6f9d7906bad46257")
    version("1.5.2", sha256="db02d0fb3373c3d766a606309b17e64a5d8da55610e921a9f1a0ec171e911d45")

    depends_on("c", type="build")  # generated

    variant("zlib", default=True, description="support for compressed mat files")
    variant("hdf5", default=True, description="support for version 7.3 mat files via hdf5")
    variant("shared", default=True, description="Enables the build of shared libraries.")

    depends_on("zlib-api", when="+zlib")
    depends_on("hdf5", when="+hdf5")

    def configure_args(self):
        args = []
        if "+zlib" in self.spec:
            args.append("--with-zlib=%s" % self.spec["zlib-api"].prefix)
        if "+hdf5" in self.spec:
            args.append("--with-hdf5=%s" % self.spec["hdf5"].prefix)
        if "+shared" not in self.spec:
            args.append("--disable-shared")
        return args

    def patch(self):
        if self.spec.satisfies("%nvhpc@:20.11"):
            # workaround anonymous version tag linker error for the NVIDIA
            # compilers
            filter_file(
                "${wl}-version-script " "${wl}$output_objdir/$libname.ver",
                "",
                "configure",
                string=True,
            )
