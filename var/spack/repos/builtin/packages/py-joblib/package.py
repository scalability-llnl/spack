# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJoblib(PythonPackage):
    """Python function as pipeline jobs"""

    homepage = "http://packages.python.org/joblib/"
    url      = "https://pypi.io/packages/source/j/joblib/joblib-0.13.2.tar.gz"

    import_modules = [
        'joblib', 'joblib.externals', 'joblib.externals.cloudpickle',
        'joblib.externals.loky', 'joblib.externals.loky.backend'
    ]

    version('0.13.2', sha256='315d6b19643ec4afd4c41c671f9f2d65ea9d787da093487a81ead7b0bac94524')
    version('0.10.3', sha256='29b2965a9efbc90a5fe66a389ae35ac5b5b0c1feabfc7cab7fd5d19f429a071d')
    version('0.10.2', sha256='3123553bdad83b143428033537c9e1939caf4a4d8813dade6a2246948c94494b')
    version('0.10.0', sha256='49b3a0ba956eaa2f077e1ebd230b3c8d7b98afc67520207ada20a4d8b8efd071')
