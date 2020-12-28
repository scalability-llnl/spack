# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGlue(RPackage):
    """An implementation of interpreted string literals, inspired by Python's
       Literal String Interpolation <https://www.python.org/dev/peps/pep-0498/>
       and Docstrings <https://www.python.org/dev/peps/pep-0257/> and Julia's
       Triple-Quoted String Literals <https://docs.julialang.org/en/stable/
       manual/strings/#triple-quoted-string-literals>."""

    homepage = "https://github.com/tidyverse/glue"
    url      = "https://cloud.r-project.org/src/contrib/glue_1.2.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/glue"

    version('1.4.1', sha256='f8b687d35cacb5ee7fcada6e9c26ea20c04d0bdc9d37e919a03abd1137513bc8')
    version('1.4.0', sha256='ea6c409f7141754baa090deba96cff270a11b185452cf9e6fb69cb148a9069c1')
    version('1.3.1', sha256='4fc1f2899d71a634e1f0adb7942772feb5ac73223891abe30ea9bd91d3633ea8')
    version('1.3.0', sha256='789e5a44c3635c3d3db26666e635e88adcf61cd02b75465125d95d7a12291cee')
    version('1.2.0', sha256='19275b34ee6a1bcad05360b7eb996cebaa1402f189a5dfb084e695d423f2296e')

    depends_on('r@3.1:', type=('build', 'run'))
