# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Gxsview(QMakePackage):
    """Gxsview is a stand-alone multi-platform integrated tool to visualize input
    data of Monte Carlo radiation transport calculation code, MCNP5, and PHITS3.

    It consists of 3D, 2D, cross-section, and input file viewers.
    Also, this software is capable of exporting in 2D(png, jpg, and xpm)
    or 3D(stl, vtk, vtp and ply) formats."""

    homepage = "https://www.nmri.go.jp/study/research_organization/risk/gxsview/en/index.html"
    url = "https://www.nmri.go.jp/study/research_organization/risk/gxsview/download/gxsview-2021.07.01-src.zip"

    # Support email for questions ohnishi@m.mpat.go.jp
    maintainers("cessenat")

    license("LGPL-3.0-only")

    version(
        "2023.05.29", sha256="1e768fd7afd22198b7f73adeb42f4ccf7e0ff68996a3843b1ea138225c4c1da3"
    )
    version(
        "2022.11.04", sha256="28c299e4f87836b93e4a42934777364a166e35d305050ee5623a1b7cbc0ab561"
    )
    version(
        "2022.05.09", sha256="c052797aee1fa9588574b28e6cf24d8ca9135c9a20cd86d134a58a7bbcbde67b"
    )
    version(
        "2021.07.01", sha256="000f9b4721d4ee03b02730dbbfe83947f96a60a183342b127f0b6b63b03e8f9a"
    )

    depends_on("fontconfig")
    depends_on("qt@5.14.0:+opengl+gui")
    depends_on("vtk@8.0:+qt+opengl2")  # +mpi+python are optional
    conflicts("%gcc@:7.2.0", msg="Requires C++17 compiler support")  # need C++17 standard

    patch("vtk9.patch", when="^vtk@9:")
    # gcc11 compilation rule for std::numeric_limits,
    # avoid "numeric_limits" is not a member of "std"
    patch("gcc11.patch", when="@2021.07.01 %gcc@11:")

    build_directory = "gui"

    def qmake_args(self):
        vtk_suffix = self.spec["vtk"].version.up_to(2)
        vtk_lib_dir = self.spec["vtk"].prefix.lib
        vtk_include_dir = join_path(self.spec["vtk"].prefix.include, "vtk-{0}".format(vtk_suffix))
        args = []
        if not os.path.exists(vtk_include_dir):
            vtk_include_dir = join_path(self.spec["vtk"].prefix.include, "vtk")
            args.append("VTK_NO_VER_SUFFIX=ON")
        args.extend(
            [
                "VTK_LIB_DIR={0}".format(vtk_lib_dir),
                "VTK_INC_DIR={0}".format(vtk_include_dir),
                "VTK_MAJOR_VER={0}".format(str(vtk_suffix)),
            ]
        )
        # Below to avoid undefined reference to `std::filesystem::__cxx11::path::_M_split_cmpts()'
        if self.spec.satisfies("%gcc@8.0:8.9") or self.spec.satisfies("%fj"):
            if self.spec.satisfies("^vtk@9:"):
                fic = "vtk9.pri"
            else:
                fic = "vtk8.pri"
            with open(fic, "a") as fh:
                fh.write("-lstdc++fs\n")
        return args

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install(join_path(self.build_directory, "gxsview"), prefix.bin)
