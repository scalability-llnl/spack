# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDryscrape(PythonPackage):
    """a lightweight Javascript-aware, headless web scraping library
       for Python"""

    homepage = "https://github.com/niklasb/dryscrape"
    url      = "https://pypi.io/packages/source/d/dryscrape/dryscrape-1.0.tar.gz"
    git      = "https://github.com/niklasb/dryscrape.git"

    version('develop', branch='master')
    version('1.0', sha256='a99858786434947266cb81d5634cb1722de48aaf6b9cdffda15b7cd4a8e07340')

    depends_on('py-lxml', type=('build', 'run'))
    depends_on('py-webkit-server@1.0:', type=('build', 'run'))
    depends_on('py-xvfbwrapper', type=('build', 'run'))
