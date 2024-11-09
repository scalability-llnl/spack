# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Muparserx(CMakePackage):
    """A C++ Library for Parsing Expressions with Strings, Complex
    Numbers, Vectors, Matrices and more."""

    homepage = "https://beltoforion.de/en/muparserx/"
    url = "https://github.com/beltoforion/muparserx/archive/refs/tags/v4.0.8.tar.gz"

    license("BSD-2-Clause")

    version("4.0.12", sha256="941c79f9b8b924f2f22406af8587177b4b185da3c968dbe8dc371b9dbe117f6e")
    version("4.0.8", sha256="5913e0a4ca29a097baad1b78a4674963bc7a06e39ff63df3c73fbad6fadb34e1")

    depends_on("cxx", type="build")  # generated
