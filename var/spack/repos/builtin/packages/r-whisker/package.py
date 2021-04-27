# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RWhisker(RPackage):
    """{{mustache}} for R, Logicless Templating

    Implements 'Mustache' logicless templating."""

    homepage = "http://github.com/edwindj/whisker"
    url      = "https://cloud.r-project.org/src/contrib/whisker_0.3-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/whisker"

    version('0.4', sha256='7a86595be4f1029ec5d7152472d11b16175737e2777134e296ae97341bf8fba8')
    version('0.3-2', sha256='484836510fcf123a66ddd13cdc8f32eb98e814cad82ed30c0294f55742b08c7c')
