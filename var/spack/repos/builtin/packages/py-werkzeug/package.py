# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWerkzeug(PythonPackage):
    """The Swiss Army knife of Python web development"""

    homepage = "http://werkzeug.pocoo.org"
    url      = "https://pypi.io/packages/source/W/Werkzeug/Werkzeug-0.16.0.tar.gz"

    version('0.16.0',  sha256='7280924747b5733b246fe23972186c6b348f9ae29724135a6dfc1e53cea433e7')
    version('0.15.4',  sha256='a0b915f0815982fb2a09161cb8f31708052d0951c3ba433ccc5e1aa276507ca6')
    version('0.11.15', sha256='455d7798ac263266dbd38d4841f7534dd35ca9c3da4a8df303f8488f38f3bcc0')
    version('0.11.11', sha256='e72c46bc14405cba7a26bd2ce28df734471bc9016bc8b4cb69466c2c14c2f7e5')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
