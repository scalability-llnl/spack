# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *
from spack.pkg.builtin.apple_gl import AppleGlBase


class AppleGlu(AppleGlBase):
    """Shim package for Apple implementation of OpenGL Utility Libray (GLU)"""

    version("1.3.0")

    provides("glu@1.3")

    requires(
        "%apple-clang platform=darwin",
        msg="Apple-GLU is only available on Darwin, when using Apple Clang",
    )
