# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MparkVariant(CMakePackage):
    """C++17 `std::variant` for C++11/14/17"""

    homepage = "https://github.com/mpark/variant"
    url = "https://github.com/mpark/variant/archive/v1.4.0.tar.gz"
    git = "https://github.com/mpark/variant.git"
    maintainers("ax3l")

    tags = ["e4s"]

    license("BSL-1.0")

    version("1.4.0", sha256="8f6b28ab3640b5d76d5b6664dda7257a4405ce59179220431b8fd196c79b2ecb")
    version("1.3.0", sha256="d0f7e41f818fcc839797a8017e76b8b66b323651c304cff641a83a56ae9943c6")

    depends_on("cxx", type="build")  # generated

    # Ref.: https://github.com/mpark/variant/pull/73
    patch("nvcc.patch", when="@:1.4.0")
    # Ref.: https://github.com/mpark/variant/issues/60
    patch("version.patch", when="@1.4.0")
    # Ref.: https://github.com/mpark/variant/pull/78
    patch("icpc.patch", when="@:1.4.0")

    cxx11_msg = (
        "MPark.Variant needs a C++11-capable compiler. "
        "See https://github.com/mpark/variant#requirements"
    )
    conflicts("%gcc@:4.7", msg=cxx11_msg)
    conflicts("%clang@:3.5", msg=cxx11_msg)

    conflicts(
        "%gcc@7.3.1",
        msg="GCC 7.3.1 has a bug that prevents using MPark.Variant. "
        "See https://github.com/mpark/variant/issues/43 and "
        "https://gcc.gnu.org/bugzilla/show_bug.cgi?id=84785 "
        "Please use a different compiler version or another "
        "compiler.",
    )
