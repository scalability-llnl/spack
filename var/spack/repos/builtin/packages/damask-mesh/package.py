# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class DamaskMesh(CMakePackage):
    """Mesh solver for DAMASK"""

    homepage = "https://damask-multiphysics.org"
    url = "https://damask-multiphysics.org/download/damask-3.0.0.tar.xz"

    maintainers("MarDiehl")

    license("AGPL-3.0-or-later")

    version("3.0.1", sha256="3db1231f6763356e71b3bb91f66f1abb4fdae2721ce85754fc468446f3d74882")
    version("3.0.0", sha256="aaebc65b3b10e6c313132ee97cfed427c115079b7e438cc0727c5207e159019f")
    version(
        "3.0.0-beta2", sha256="513567b4643f39e27ae32b9f75463fc6f388c1548d42f0393cc87ba02d075f6a"
    )
    version(
        "3.0.0-beta", sha256="1e25e409ac559fc437d1887c6ca930677a732db89a3a32499d545dd75e93925c"
    )
    version(
        "3.0.0-alpha8", sha256="f62c38123213d1c1fe2eb8910b0ffbdc1cac56273c2520f3b64a553363190b9d"
    )
    version(
        "3.0.0-alpha7", sha256="442b06b824441293e72ff91b211a555c5d497aedf62be1c4332c426558b848a4"
    )
    version(
        "3.0.0-alpha6", sha256="de6748c285558dec8f730c4301bfa56b4078c130ff80e3095faf76202f8d2109"
    )
    version(
        "3.0.0-alpha5", sha256="2d2b10901959c26a5bb5c52327cdafc7943bc1b36b77b515b0371221703249ae"
    )
    version(
        "3.0.0-alpha4", sha256="0bb8bde43b27d852b1fb6e359a7157354544557ad83d87987b03f5d629ce5493"
    )

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("petsc@3.21:3.22", when="@3.0.1:")
    depends_on("petsc@3.21", when="@3.0.0-beta2:")
    depends_on("petsc@3.20.3:3.20", when="@3.0.0-beta")
    depends_on("petsc@3.20.2:3.20", when="@3.0.0-alpha8")
    depends_on("petsc@3.17.1:3.18", when="@3.0.0-alpha7")
    depends_on("petsc@3.16.5:3.16", when="@3.0.0-alpha6")
    depends_on("petsc@3.14.0:3.14,3.15.1:3.16", when="@3.0.0-alpha5")
    depends_on("petsc@3.14.0:3.14,3.15.1:3.15", when="@3.0.0-alpha4")
    depends_on("pkgconfig", type="build")
    depends_on("cmake@3.10:", type="build")
    depends_on("petsc+mpi+hdf5")
    depends_on("hdf5@1.12:+mpi+fortran", when="@3.0.0-alpha7:")
    depends_on("hdf5@1.10:+mpi+fortran")
    depends_on("libfyaml", when="@3.0.0-alpha7:")

    # relax Fortran source limit to 132 char to enable PETSc macro expansion. created by @MarDiehl
    patch("long-lines.patch", when="@3.0.0-alpha7")
    patch("CMakeDebugRelease.patch", when="@3.0.0-alpha4")

    variant(
        "build_type",
        default="DebugRelease",
        description="The build type to build",
        values=("Debug", "Release", "DebugRelease"),
    )

    def cmake_args(self):
        return [self.define("DAMASK_SOLVER", "mesh")]

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def execute(self):
        with working_dir(self.build_directory):
            damask_mesh = Executable("src/DAMASK_mesh")
            damask_mesh("--help")
