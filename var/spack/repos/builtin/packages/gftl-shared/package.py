# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GftlShared(CMakePackage):
    """
    Provides common gFTL containers of Fortran intrinsic types that
    are encountered frequently.
    """

    homepage = "https://github.com/Goddard-Fortran-Ecosystem/gFTL-shared"
    url = (
        "https://github.com/Goddard-Fortran-Ecosystem/gFTL-shared/archive/refs/tags/v1.5.0.tar.gz"
    )
    list_url = "https://github.com/Goddard-Fortran-Ecosystem/gFTL-shared/tags"
    git = "https://github.com/Goddard-Fortran-Ecosystem/gFTL-shared.git"

    maintainers("mathomp4", "tclune")

    license("Apache-2.0")

    version("main", branch="main")

    version("1.9.0", sha256="a3291ce61b512fe88628cc074b02363c2ba3081e7b453371089121988482dd6f")
    version("1.8.0", sha256="3450161508c573ea053b2a23cdbf2a1d6fd6fdb78c162d31fc0019da0f8dd03c")
    version("1.7.0", sha256="8ba567133fcee6b93bc71f61b3bb2053b4b07c6d78f6ad98a04dfc40aa478de7")
    version("1.6.1", sha256="0e3e1e0c7e0c3f1576e296b3b199dcae4bbaad055fc8fe929c34e52d4b07b02c")
    version("1.6.0", sha256="90245b83aea9854bc5b9fbd553a68cf73ab12f6ed5a14753a9c84092047e8cb0")
    version("1.5.1", sha256="353d07cc22678d1a79b19dbf53d8ba54b889e424a15e315cc4f035b72eedb83a")
    version("1.5.0", sha256="c19b8197cc6956d4a51a16f98b38b63c7bc9f784f1fd38f8e3949be3ea792356")
    version("1.4.1", sha256="bb403f72e80aaac49ed5107f7c755ce5273c2e650bd5438a746228798eeced6c")
    version("1.4.0", sha256="83a2474ae943d81d797460b18106874de14c39093efd4e35abb3f1b6ec835171")
    version("1.3.6", sha256="d8cd1fc7b8c9a42fc44c8986f6b89e06589bef9b6718699e564dd506e101cf1f")
    version("1.3.5", sha256="5cb421cf79a0505d21da6c25961dc7f9f108a4ff68a2ee8b5db39b2926a1133f")
    version("1.3.4", sha256="02570edb08af379aa59d3a15296c0231701e114de273ce08804c718681555854")
    version("1.3.3", sha256="40822130fc4eec9d34ba71cc0ee0a00fb7410e5ce4d2841cb405f192fb12ab3b")
    version("1.3.2", sha256="142e94420986fa1bb3797bd4a0e61ca07cdd4d379465734bd25ec92032d769f0")
    version("1.3.1", sha256="a71e164108847f32f37da505f604fc2a50f392a4fcdf9a7cfe8eaf775bed64d4")
    version("1.3.0", sha256="979b00c4d531e701bf4346f662e3e4cc865124a97ca958637a53201d66d4ee43")

    depends_on("fortran", type="build")

    depends_on("m4", type=("build", "run"))
    depends_on("cmake@3.12:", type="build")
    depends_on("gftl")

    # gftl-shared only works with the Fujitsu compiler from 1.8.0 onwards
    conflicts(
        "%fj",
        when="@:1.7.0",
        msg="gftl-shared only works with the Fujitsu compiler from 1.8.0 onwards",
    )

    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release"),
    )
