# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ants(CMakePackage):
    """ANTs extracts information from complex datasets that include imaging.
    Paired with ANTsR (answer), ANTs is useful for managing, interpreting
    and visualizing multidimensional data. ANTs is popularly considered a
    state-of-the-art medical image registration and segmentation toolkit.
    ANTs depends on the Insight ToolKit (ITK), a widely used medical image
    processing library to which ANTs developers contribute.
    """

    homepage = "https://stnava.github.io/ANTs/"
    git = "https://github.com/ANTsX/ANTs.git"
    url = "https://github.com/ANTsX/ANTs/archive/v2.2.0.tar.gz"

    version("2.5.1", sha256="8e3a7c0d3dab05883cba466aff262d78d832f679491318b94ce49b606565cebe")
    version("2.4.3", sha256="13ba78917aca0b20e69f4c43da607f8fe8c810edba23b6f5fd64fbd81b70a79a")
    version("2.4.0", sha256="a8ff78f4d2b16e495f340c9b0647f56c92cc4fc40b6ae04a60b941e5e239f9be")
    version("20220205", commit="6f07ac55569d0d085d2adf7888d1c7a2bd563bfe", deprecated=True)
    version("2.3.5", sha256="2fddfd5f274a47f1c383e734a7e763b627c4a8383d2d3b9971561f335016bb0a")
    version("2.2.0", sha256="62f8f9ae141cb45025f4bb59277c053acf658d4a3ba868c9e0f609af72e66b4a")

    depends_on("cxx", type="build")  # generated

    depends_on("zlib-api", type="link")

    variant("minc", default=True, description="Build ITK with MINC support")

    def cmake_args(self):
        return [
            "-DBUILD_TESTING=OFF",  # needed for <= 2.3.5 due to ANTs/#1236
            self.define_from_variant("ITK_BUILD_MINC_SUPPORT", "minc"),
        ]

    def install(self, spec, prefix):
        with working_dir(join_path(self.build_directory, "ANTS-build"), create=False):
            make("install")
        install_tree("Scripts", prefix.bin)

    def setup_run_environment(self, env):
        env.set("ANTSPATH", self.prefix.bin)
