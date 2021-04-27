# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PySphinxRtdTheme(PythonPackage):
    """ReadTheDocs.org theme for Sphinx."""

    homepage = "https://github.com/readthedocs/sphinx_rtd_theme"
    pypi = "sphinx-rtd-theme/sphinx_rtd_theme-0.5.1.tar.gz"

    version('0.5.1', sha256='eda689eda0c7301a80cf122dad28b1861e5605cbf455558f3775e1e8200e83a5')
    version('0.5.0', sha256='22c795ba2832a169ca301cd0a083f7a434e09c538c70beb42782c073651b707d')
    version('0.4.3', sha256='728607e34d60456d736cc7991fd236afb828b21b82f956c5ea75f94c8414040a')

    depends_on('py-setuptools', type='build')
    depends_on('py-sphinx', when='@0.4.1:', type=('build', 'run'))

    def setup_build_environment(self, env):
        # Hack to prevent usage of npm in 0.5+
        # https://github.com/readthedocs/sphinx_rtd_theme/issues/1014
        env.set('CI', True)
