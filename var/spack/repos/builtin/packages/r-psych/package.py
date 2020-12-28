# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPsych(RPackage):
    """A general purpose toolbox for personality, psychometric theory and
       experimental psychology. Functions are primarily for multivariate
       analysis and scale construction using factor analysis, principal
       component analysis, cluster analysis and reliability analysis, although
       others provide basic descriptive statistics. Item Response Theory is
       done using factor analysis of tetrachoric and polychoric correlations.
       Functions for analyzing data at multiple levels include within and
       between group statistics, including correlations and factor analysis.
       Functions for simulating and testing particular item and test structures
       are included. Several functions serve as a useful front end for
       structural equation modeling. Graphical displays of path diagrams,
       factor analysis and structural equation models are created using basic
       graphics. Some of the functions are written to support a book on
       psychometric theory as well as publications in personality research.
       For more information, see the <http://personality-project.org/r> web
       page."""

    homepage = "http://personality-project.org/r/psych"
    url      = "https://cloud.r-project.org/src/contrib/psych_1.7.8.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/psych"

    version('1.8.12', sha256='6e175e049bc1ee5b79a9e51ccafb22b962b4e6c839ce5c9cfa1ad83967037743')
    version('1.8.10', sha256='e8901ddab14729bfccbd82a8824fbb6523c10c2cd8fb7199b1ca56a7ffcb6e58')
    version('1.7.8', sha256='f328ea602e22b0e7e5f310a8d19f305d8e0a3a86040cdfb64863b68b56d55135')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-mnormt', type=('build', 'run'))
    depends_on('r-foreign', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-nlme', type=('build', 'run'))
