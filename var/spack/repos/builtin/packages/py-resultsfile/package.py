# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyResultsfile(PythonPackage):
    """Python module to read output files of quantum chemistry programs"""

    homepage = "https://gitlab.com/scemama/resultsFile"
    url      = "https://gitlab.com/scemama/resultsFile/-/archive/v1.0/resultsFile-v1.0.tar.gz"
    git      = "https://gitlab.com/scemama/resultsFile.git"

    maintainers = ['scemama']

    version('2.0', sha256='2a34208254e4bea155695690437f6a59bf5f7b0ddb421d6c1a2d377510f018f7')
    version('1.0', sha256='e029054b2727131da9684fa2ec9fb8b6a3225dc7f648216a9390267b2d5d60c3')

    depends_on('python@2.7:2.8.999', type=('build', 'run'), when='@1.0:1.999')
    depends_on('python@3:', type=('build', 'run'), when='@2.0:')
