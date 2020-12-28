# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RWhisker(RPackage):
    """logicless templating, reuse templates in many programming languages
    including R"""

    homepage = "http://github.com/edwindj/whisker"
    url      = "https://cloud.r-project.org/src/contrib/whisker_0.3-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/whisker"

    version('0.3-2', sha256='484836510fcf123a66ddd13cdc8f32eb98e814cad82ed30c0294f55742b08c7c')
