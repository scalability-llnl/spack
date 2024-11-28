# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Entt(CMakePackage):
    """EnTT is a header-only, tiny and easy to use library for game
    programming and much more written in modern C++, mainly known for its
    innovative entity-component-system (ECS) model.
    """

    homepage = "https://entt.docsforge.com"
    url = "https://github.com/skypjack/entt/archive/v3.5.2.tar.gz"

    license("MIT")

    version("3.13.2", sha256="cb556aa543d01177b62de41321759e02d96078948dda72705b3d7fe68af88489")
    version("3.13.1", sha256="a4f290b601a70333126abd2cec7b0c232c74a4f85dcf1e04d969e8122dae8652")
    version("3.11.1", sha256="0ac010f232d3089200c5e545bcbd6480cf68b705de6930d8ff7cdb0a29f5b47b")
    version("3.5.2", sha256="f9271293c44518386c402c9a2188627819748f66302df48af4f6d08e30661036")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.7.0:", type="build")
    depends_on("doxygen@1.8.0:", type="build")

    # TODO: This list is not comprehensive, we might want to extend it later
    compiler_warning = "EnTT requires a compiler with support for C++17"
    conflicts("%apple-clang@:10.1", msg=compiler_warning)
    conflicts("%clang@:6", msg=compiler_warning)
    conflicts("%gcc@:7.1", msg=compiler_warning)

    def cmake_args(self):
        return [self.define("BUILD_DOCS", "ON")]
