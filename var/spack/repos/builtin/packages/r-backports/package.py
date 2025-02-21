# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBackports(RPackage):
    """Reimplementations of Functions Introduced Since R-3.0.0.

    Functions introduced or changed since R v3.0.0 are re-implemented in this
    package. The backports are conditionally exported in order to let R resolve
    the function name to either the implemented backport, or the respective
    base version, if available. Package developers can make use of new
    functions or arguments by selectively importing specific backports to
    support older installations."""

    cran = "backports"

    license("GPL-2.0-only OR GPL-3.0-only")

    version("1.5.0", sha256="0d3ed9db8f1505e88967f48d669b2a257e0c6b7e6320ea64b946c1bd40897ca2")
    version("1.4.1", sha256="845c3c59fbb05e5a892c4231b955a0afdd331d82b7cc815bcff0672023242474")
    version("1.4.0", sha256="e7611565d24a852ad8b08579a7c67ad9121c1bda148bade98c7bec686e8dabbf")
    version("1.2.1", sha256="a2834bbd57e305e5d8010322f1906ea1789b3b5ba5eca77c5ff4248aceb7c2d5")
    version("1.1.4", sha256="ee4b5efef22fa7ef27d7983ffcd31db52f81e1fbb7189c6e89ee09b69349ff03")
    version("1.1.3", sha256="e41bd146824ec921994f1b176d0e4cca0b36dd3db32ca7a954d872a5ba214cc1")
    version("1.1.1", sha256="494e81a4829339c8f1cc3e015daa807e9138b8e21b929965fc7c00b1abbe8897")
    version("1.1.0", sha256="c5536966ed6ca93f20c9a21d4f569cc1c6865d3352445ea66448f82590349fcd")

    depends_on("r@3.0.0:", type=("build", "run"))
