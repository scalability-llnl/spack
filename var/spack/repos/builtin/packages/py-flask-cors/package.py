# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyFlaskCors(PythonPackage):
    """A Flask extension for handling Cross Origin Resource Sharing (CORS),
    making cross-origin AJAX possible.
    """

    homepage = "https://flask-cors.corydolphin.com/en/latest/index.html"
    pypi = "Flask-Cors/Flask-Cors-3.0.10.tar.gz"

    version('3.0.10', sha256='b60839393f3b84a0f3746f6cdca56c1ad7426aa738b70d6c61375857823181de')

    depends_on('py-setuptools', type='build')
    depends_on('py-flask@0.9:', type=('build', 'run'))
    depends_on('py-six',        type=('build', 'run'))
