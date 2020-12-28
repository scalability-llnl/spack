# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWeblogo(PythonPackage):
    """WebLogo is a web based application designed to make the generation of
    sequence logos as easy and painless as possible."""

    homepage = "http://weblogo.threeplusone.com"
    url      = "https://pypi.io/packages/source/w/weblogo/weblogo-3.6.0.tar.gz"

    version('3.6.0', sha256='af5a9f065581f18d71bd7c22b160c1e443932f22cab992d439d3dc8757c80a85')

    depends_on('py-setuptools', type='build')
    depends_on('ghostscript', type=('build', 'run'))
    depends_on('pdf2svg', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
