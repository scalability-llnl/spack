# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlask(PythonPackage):
    """A simple framework for building complex web applications."""

    homepage = "https://palletsprojects.com/p/flask/"
    url      = "https://pypi.io/packages/source/F/Flask/Flask-1.1.1.tar.gz"

    version('1.1.2',  sha256='4efa1ae2d7c9865af48986de8aeb8504bf32c7f3d6fdc9353d34b21f4b127060')
    version('1.1.1',  sha256='13f9f196f330c7c2c5d7a5cf91af894110ca0215ac051b5844701f2bfd934d52')
    version('0.12.4', sha256='2ea22336f6d388b4b242bc3abf8a01244a8aa3e236e7407469ef78c16ba355dd')
    version('0.12.2', sha256='49f44461237b69ecd901cc7ce66feea0319b9158743dd27a2899962ab214dac1')
    version('0.12.1', sha256='9dce4b6bfbb5b062181d3f7da8f727ff70c1156cbb4024351eafd426deb5fb88')
    version('0.11.1', sha256='b4713f2bfb9ebc2966b8a49903ae0d3984781d5c878591cf2f7b484d28756b0e')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))
    depends_on('py-setuptools',         type=('build', 'run'))
    depends_on('py-werkzeug@0.15:',     type=('build', 'run'))
    depends_on('py-jinja2@2.10.1:',     type=('build', 'run'))
    depends_on('py-itsdangerous@0.24:', type=('build', 'run'))
    depends_on('py-click@5.1:',         type=('build', 'run'))
