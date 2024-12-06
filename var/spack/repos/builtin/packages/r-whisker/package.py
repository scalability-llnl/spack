# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RWhisker(RPackage):
    """{{mustache}} for R, Logicless Templating.

    Implements 'Mustache' logicless templating."""

    cran = "whisker"

    license("GPL-3.0-only")

    version("0.4.1", sha256="bf5151494508032f68ac41e211bda80da9087c65c7068ffdd12f16669bf1f2bc")
    version("0.4", sha256="7a86595be4f1029ec5d7152472d11b16175737e2777134e296ae97341bf8fba8")
    version("0.3-2", sha256="484836510fcf123a66ddd13cdc8f32eb98e814cad82ed30c0294f55742b08c7c")
