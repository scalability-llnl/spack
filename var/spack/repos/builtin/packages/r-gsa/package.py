# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGsa(RPackage):
    """Gene Set Analysis."""

    cran = "GSA"

    version("1.03.3", sha256="5459786190f40339addc45e7bb58c6a983548aa8feac7277ea7ec0662c5a282c")
    version("1.03.2", sha256="177d6059fc645d3d8883806d2dea1c5dfc68efdada9aadde8a96b6d57acf35b8")
    version("1.03.1", sha256="e192d4383f53680dbd556223ea5f8cad6bae62a80a337ba5fd8d05a8aee6a917")
