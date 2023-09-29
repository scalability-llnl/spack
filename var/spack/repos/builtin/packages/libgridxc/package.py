# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Libgridxc(CMakePackage, MakefilePackage):
    """A library to compute the exchange and correlation energy and potential
    in spherical (i.e. an atom) or periodic systems.
    """

    homepage = "https://gitlab.com/siesta-project/libraries/libgridxc"
    git = "https://gitlab.com/siesta-project/libraries/libgridxc.git"
    url = "https://gitlab.com/siesta-project/libraries/libgridxc/-/archive/1.1.0/libgridxc-1.1.0.tar.gz"

    version("1.1.0", sha256="e7883e57a4db2438ee59437740291c06e0cfe1c8ae1901e4001f32312307e46a")
    version("0.10.1", sha256="c6b74457e516cba32c334ae4d7b027b18022d16733e05da7570a1ba7f4e4ada2")
    version("0.9.6", sha256="3b89ccc02d65729ea2d7cb291ae1d9b53acd65c1fd144e8846362cffb71b114a")
    version("0.9.5", sha256="98aa34dbaffe360ff332606eebb7c842994244a3114015d89c5a3850298c40aa")
    version("0.9.1", sha256="346735e30dd3a4099532a985b7a491f6d2b882954a527bdac655d87232be5341")
    version("0.8.5", sha256="af293be83d85908231aba9074f2b51545457bc7fce87fab9f72010a10f0028a6")
    version("0.8.4", sha256="b4f2f4af1f0c98b9e82505b99924da16e8c7719dd3e3e95f1d16e504b43944ce")
    version("0.8.3", sha256="01643c2e009474d4eb1f945f7e506f465bf0378d19e56028bc4a9af56ab0b1f3")
    version("0.8.0", sha256="ff89b3302f850d1d9f651951e4ade20dfa4c71c809a2d86382c6797392064c9c")
    version("0.7.6", sha256="058b80f40c85997eea0eae3f15b7cc8105f817e59564106308b22f57a03b216b")

    # Version dependens file system
    build_system(
        conditional("cmake", when="@1.1.0:"),
        conditional("makefile", when="@:0.10.1"),
        default="cmake",
    )

    with when("build_system=makefile"):
        build_directory = "build"
        depends_on("autoconf@2.69:", type="build")
        depends_on("automake@1.14:", type="build")
        depends_on("libtool@2.4.2:", type="build")
        depends_on("m4", type="build")

    with when("build_system=cmake"):
        depends_on("cmake", type="build")
        depends_on("mpi", type="build")

    depends_on("libxc@:4.3.4", when="@0.8.0:")

    parallel = False

    #
    # ------- CMake Install Procedure ------
    #

    def cmake_args(self):
        args = ["-DWITH_MPI=ON", "-DWITH_LIBXC=ON"]
        return args

    @when("build_system=cmake")
    def build_targets(self):
        # Since we override build_targets for the legacy build
        # we have to also define it for the new build path
        return []

    @when("build_system=cmake")
    def install(self, spec, prefix):
        # Since we override install for the legacy build
        # we have to wrap the original CMakePackage.install here
        super(CMakePackage, self).install(spec, prefix)

    #
    # ------- Legacy Install Procedure ------
    #

    @when("build_system=makefile")
    def edit(self, spec, prefix):
        sh = which("sh")
        with working_dir("build", create=True):
            sh("../src/config.sh")
            copy("../extra/fortran.mk", "fortran.mk")

    @property
    @when("build_system=makefile")
    def build_targets(self):
        # Legacy build options
        args = ["PREFIX={0}".format(self.prefix)]
        if self.spec.satisfies("@0.8.0:"):
            args += ["WITH_LIBXC=1", "LIBXC_ROOT={0}".format(self.spec["libxc"].prefix)]
        return args

    @when("build_system=makefile")
    def install(self, spec, prefix):
        # Legacy install options
        mkdirp(join_path(self.prefix, "share", "org.siesta-project"))
        install(
            join_path(self.prefix, "gridxc.mk"),
            join_path(self.prefix, "share", "org.siesta-project", "gridxc.mk"),
        )
        os.remove(join_path(self.prefix, "gridxc.mk"))
        install(
            join_path(self.prefix, "libxc.mk"),
            join_path(self.prefix, "share", "org.siesta-project", "libxc.mk"),
        )
        os.remove(join_path(self.prefix, "libxc.mk"))

