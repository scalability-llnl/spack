# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Eigen(CMakePackage):
    """Eigen is a C++ template library for linear algebra matrices,
    vectors, numerical solvers, and related algorithms.
    """

    homepage = "https://eigen.tuxfamily.org/"
    url = "https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.gz"
    maintainers("HaoZeke")

    license("MPL-2.0")

    version("3.4.0", sha256="8586084f71f9bde545ee7fa6d00288b264a2b7ac3607b974e54d13e7162c1c72")
    version("3.3.9", sha256="7985975b787340124786f092b3a07d594b2e9cd53bbfe5f3d9b1daee7d55f56f")
    version("3.3.8", sha256="146a480b8ed1fb6ac7cd33fec9eb5e8f8f62c3683b3f850094d9d5c35a92419a")
    version("3.3.7", sha256="d56fbad95abf993f8af608484729e3d87ef611dd85b3380a8bad1d5cbc373a57")
    version("3.3.6", sha256="e7cd8c94d6516d1ada9893ccc7c9a400fcee99927c902f15adba940787104dba")
    version("3.3.5", sha256="383407ab3d0c268074e97a2cbba84ac197fd24532f014aa2adc522355c1aa2d0")
    version("3.3.4", sha256="c5ca6e3442fb48ae75159ca7568854d9ba737bc351460f27ee91b6f3f9fd1f3d")
    version("3.3.3", sha256="fd72694390bd8e81586205717d2cf823e718f584b779a155db747d1e68481a2e")
    version("3.3.2", sha256="8d7611247fba1236da4dee7a64607017b6fb9ca5e3f0dc44d480e5d33d5663a5")
    version("3.3.1", sha256="50dd21a8997fce0857b27a126811ae8ee7619984ab5425ecf33510cec649e642")
    version("3.3.0", sha256="de82e01f97e1a95f121bd3ace87aa1237818353c14e38f630a65f5ba2c92f0e1")
    version("3.2.10", sha256="0920cb60ec38de5fb509650014eff7cc6d26a097c7b38c7db4b1aa5df5c85042")
    version("3.2.9", sha256="f683b20259ad72c3d384c00278166dd2a42d99b78dcd589ed4a6ca74bbb4ca07")
    version("3.2.8", sha256="64c54781cfe9eefef2792003ab04b271d4b2ec32eda6e9cdf120d7aad4ebb282")
    version("3.2.7", sha256="0ea9df884873275bf39c2965d486fa2d112f3a64b97b60b45b8bc4bb034a36c1")
    version("3.2.6", sha256="e097b8dcc5ad30d40af4ad72d7052e3f78639469baf83cffaadc045459cda21f")
    version("3.2.5", sha256="8068bd528a2ff3885eb55225c27237cf5cda834355599f05c2c85345db8338b4")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # there is a bug that provokes bad parsing of nvhpc version
    patch(
        "https://gitlab.com/libeigen/eigen/-/commit/001a57519a7aa909d3bf0cd8c6ec8a9cd19d9c70.diff",
        when="@3.2.6:3.3.9",
        sha256="55daee880b7669807efc0dcbeda2ae3b659e6dd4df3932f3573c8778bf5f8a42",
    )

    # there is a bug in 3.3.8 that provokes a compile error in dependent packages, see https://gitlab.com/libeigen/eigen/-/issues/2011
    patch(
        "https://gitlab.com/libeigen/eigen/-/commit/ef3cc72cb65e2d500459c178c63e349bacfa834f.diff",
        when="@3.3.8",
        sha256="b8877a84c4338f08ab8a6bb8b274c768e93d36ac05b733b078745198919a74bf",
    )

    # there is a bug in 3.3.4 that provokes a compile error with the xl compiler
    # See https://gitlab.com/libeigen/eigen/-/issues/1555
    patch("xlc-compilation-3.3.4.patch", when="@3.3.4%xl_r")

    # From http://eigen.tuxfamily.org/index.php?title=Main_Page#Requirements
    # "Eigen doesn't have any dependencies other than the C++ standard
    # library."
    variant(
        "build_type",
        default="RelWithDebInfo",
        description="The build type to build",
        values=("Debug", "Release", "RelWithDebInfo"),
    )

    # TODO: latex and doxygen needed to produce docs with make doc
    # TODO: Other dependencies might be needed to test this package

    def setup_run_environment(self, env):
        env.prepend_path("CPATH", self.prefix.include.eigen3)

    def cmake_args(self):
        args = []
        if self.spec.satisfies("@:3.4"):
            # CMake fails without this flag
            # https://gitlab.com/libeigen/eigen/-/issues/1656
            args += [self.define("BUILD_TESTING", "ON")]
        return args

    @property
    def headers(self):
        headers = find_all_headers(self.prefix.include)
        headers.directories = [self.prefix.include.eigen3]
        return headers
