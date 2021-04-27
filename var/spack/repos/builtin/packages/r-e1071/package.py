# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RE1071(RPackage):
    """Misc Functions of the Department of Statistics, Probability Theory Group
    (Formerly: E1071), TU Wien

    Functions for latent class analysis, short time Fourier transform, fuzzy
    clustering, support vector machines, shortest path computation, bagged
    clustering, naive Bayes classifier, ..."""

    homepage = "https://cloud.r-project.org/package=e1071"
    url      = "https://cloud.r-project.org/src/contrib/e1071_1.6-7.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/e1071"

    version('1.7-4', sha256='e6ab871b06f500dc65f8f781cc7253f43179698784c06dab040b4aa6592f2309')
    version('1.7-2', sha256='721c299ce83047312acfa3e0c4b3d4c223d84a4c53400c73465cca2c92913752')
    version('1.7-1', sha256='5c5f04a51c1cd2c7dbdf69987adef9bc07116804c63992cd36d804a1daf89dfe')
    version('1.6-7', sha256='7048fbc0ac17d7e3420fe68081d0e0a2176b1154ee3191d53558ea9724c7c980')

    depends_on('r-class', type=('build', 'run'))
