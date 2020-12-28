# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPbapply(RPackage):
    """A lightweight package that adds progress bar to vectorized R
    apply functions."""

    homepage = "https://cloud.r-project.org/package=pbapply"
    url      = "https://cloud.r-project.org/src/contrib/pbapply_1.3-3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/pbapply"

    version('1.4-1', sha256='b3633349181db944e1dfc4422b4728a6562e454117a232cbb51633906cd27cad')
    version('1.3-4', sha256='cdfdaf9b8aecbe48daac858aecaf65a766b74a363d1eb7cd6ebf27c0549f6552')
    version('1.3-3', sha256='7379b21d1176db5769f5cac858dd12c975736e80a600870180cec9625cf51047')
    version('1.3-2', sha256='196367da93fcd31431d8e78c177d4afccf9c634513edf24a7229adce2d95b5e9')
    version('1.3-1', sha256='fc4f1ea9d3290bab20a0ec74a3195c8887592b022ab6abb8d7754006a4487114')
    version('1.3-0', sha256='a6d4bf88ade12a3b25662e271329fe54d170596335cba2a2dd210bbb7e8a5936')
    version('1.2-2', sha256='81e5a8a5e0c7ce24b25679d0f69e8773908c9ce569f1e5984e52d4cef33ac34e')

    depends_on('r@3.2.0:', type=('build', 'run'))
