# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyDoxypy(PythonPackage):
    """doxypy is an input filter for Doxygen."""

    pypi = "doxypy/doxypy-0.3.tar.gz"

    version('0.3', sha256='55d621b0edebd9e2a58a266c0a1d086fc9892de8e07e04dfbb93880a7ae91f00')

    depends_on('python@:2.8')
