# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGoftest(RPackage):
    """Cramer-Von Mises and Anderson-Darling tests of goodness-of-fit for
       continuous univariate distributions, using efficient algorithms.
    """

    homepage = "https://cloud.r-project.org/package=goftest"
    url      = "https://cloud.r-project.org/src/contrib/goftest_1.2-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/goftest"

    version('1.2-2', sha256='e497992666b002b6c6bed73bf05047ad7aa69eb58898da0ad8f1f5b2219e7647')

    depends_on('r@3.3:', type=('build', 'run'))
