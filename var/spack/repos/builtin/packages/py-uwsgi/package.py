# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyUwsgi(PythonPackage):
    """Web Application framework for low overhead web services"""

    homepage = "https://github.com/unbit/uwsgi/"
    pypi = "uwsgi/uwsgi-2.0.18.tar.gz"

    version('2.0.18', sha256='4972ac538800fb2d421027f49b4a1869b66048839507ccf0aa2fda792d99f583')

    depends_on('py-setuptools', type='build')
