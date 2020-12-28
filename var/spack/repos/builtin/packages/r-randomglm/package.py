# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRandomglm(RPackage):
    """randomGLM: Random General Linear Model Prediction"""

    homepage = "http://www.genetics.ucla.edu/labs/horvath/CoexpressionNetwork/"
    url      = "https://cloud.r-project.org/src/contrib/randomGLM_1.02-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/randomGLM"

    version('1.02-1', sha256='3bf7c1dbdacc68125f8ae3014b9bc546dd3328d04ad015d154781bdf3f1a230c')

    depends_on('r@2.14.0:', type=('build', 'run'))
    depends_on('r-doparallel', type=('build', 'run'))
    depends_on('r-foreach', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
