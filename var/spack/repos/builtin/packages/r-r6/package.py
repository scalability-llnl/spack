# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RR6(RPackage):
    """Encapsulated Classes with Reference Semantics.

    The R6 package allows the creation of classes with reference semantics,
    similar to R's built-in reference classes. Compared to reference classes,
    R6 classes are simpler and lighter-weight, and they are not built on S4
    classes so they do not require the methods package. These classes allow
    public and private members, and they support inheritance, even when the
    classes are defined in different packages."""

    cran = "R6"

    version("2.5.1", sha256="8d92bd29c2ed7bf15f2778618ffe4a95556193d21d8431a7f75e7e5fc102bf48")
    version("2.5.0", sha256="aec1af9626ec532cb883b544bf9eff4cb2d89c343c7ce0fa31761ec5a7882e02")
    version("2.4.0", sha256="70be110174fbf5f5304049b186a6f9c05b77bfaec6d8caf980fcef5da6e0abce")
    version("2.2.2", sha256="087756f471884c3b3ead80215a7cc5636a78b8a956e91675acfe2896426eae8f")
    version("2.2.0", sha256="7d7bddc4303fafa99954182ccad938166d681499d4e9ae7001d21b0fd60d25c7")
    version("2.1.2", sha256="1bfbb14d9da85b5f8eb865aa6355b2c71c9f86b71f616bfe5a28939b62484d79")

    depends_on("r@3.0:", type=("build", "run"))
