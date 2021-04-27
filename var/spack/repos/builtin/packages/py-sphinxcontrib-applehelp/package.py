# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PySphinxcontribApplehelp(PythonPackage):
    """sphinxcontrib-applehelp is a sphinx extension which outputs Apple
    help books."""

    homepage = "http://sphinx-doc.org/"
    pypi = "sphinxcontrib-applehelp/sphinxcontrib-applehelp-1.0.1.tar.gz"

    # Sphinx requires sphinxcontrib-applehelp at build-time, but
    # sphinxcontrib-applehelp requires sphinx at run-time
    import_modules = []

    version('1.0.1', sha256='edaa0ab2b2bc74403149cb0209d6775c96de797dfd5b5e2a71981309efab3897')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
