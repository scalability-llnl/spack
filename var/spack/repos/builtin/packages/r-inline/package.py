# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RInline(RPackage):
    """Functions to Inline C, C++, Fortran Function Calls from R.

    Functionality to dynamically define R functions and S4 methods with inlined
    C, C++ or Fortran code supporting .C and .Call calling conventions."""

    cran = "inline"

    license("LGPL-2.0-or-later")

    version("0.3.19", sha256="0ee9309bb7dab0b97761ddd18381aa12bd7d54678ccd7bec00784e831f4c99d5")
    version("0.3.17", sha256="792857b2ebd408d6523424d2f6bb7297e241d4b28ab32372f6a9240c8cd554f3")
    version("0.3.15", sha256="ff043fe13c1991a3b285bed256ff4a9c0ba10bee764225a34b285875b7d69c68")
    version("0.3.14", sha256="fd34d6bf965148d26d983a022a0ff7bc1a5831f6ca066deee3f6139894dfc931")

    depends_on("r@2.4.0:", when="@0.3.16:", type=("build", "run"))
