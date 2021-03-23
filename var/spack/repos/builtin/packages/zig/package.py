# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
class Zig(CMakePackage):
    """A general-purpose programming language and toolchain for maintaining
    robust, optimal, and reusable software.
    """

    homepage = "https://ziglang.org/"
    git = "https://github.com/ziglang/zig.git"

    version('0.7.1', tag='0.7.1')

    variant(
        'build_type', values=('Release', 'RelWithDebInfo', 'MinSizeRel'),
        default='Release', description='CMake build type'
    )

    depends_on('llvm@11.0.0: +all_targets')

    provides('ziglang')
