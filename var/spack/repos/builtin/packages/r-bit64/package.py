# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBit64(RPackage):
    """A S3 Class for Vectors of 64bit Integers.

    Package 'bit64' provides serializable S3 atomic 64bit (signed) integers.
    These are useful for handling database keys and exact counting in +-2^63.
    WARNING: do not use them as replacement for 32bit integers, integer64 are
    not supported for subscripting by R-core and they have different semantics
    when combined with double, e.g.  integer64 + double => integer64. Class
    integer64 can be used in vectors, matrices, arrays and data.frames. Methods
    are available for coercion from and to logicals, integers, doubles,
    characters and factors as well as many elementwise and summary functions.
    Many fast algorithmic operations such as 'match' and 'order' support inter-
    active data exploration and manipulation and optionally leverage
    caching."""

    cran = "bit64"

    license("GPL-2.0-only OR GPL-3.0-only")

    version("4.0.5", sha256="25df6826ea5e93241c4874cad4fa8dadc87a40f4ff74c9107aa12a9e033e1578")
    version("0.9-7", sha256="7b9aaa7f971198728c3629f9ba1a1b24d53db5c7e459498b0fdf86bbd3dff61f")

    depends_on("c", type="build")  # generated

    depends_on("r@3.0.1:", type=("build", "run"))
    depends_on("r-bit@1.1-12:", type=("build", "run"))
    depends_on("r-bit@4.0.0:", type=("build", "run"), when="@4.0.5:")
