# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyTexttable(PythonPackage):
    """Python module for creating simple ASCII tables."""

    homepage = "https://github.com/foutaise/texttable/"
    pypi = "texttable/texttable-1.6.1.tar.gz"

    version('1.6.1', sha256='2b60a5304ccfbeac80ffae7350d7c2f5d7a24e9aab5036d0f82489746419d9b2')

    depends_on('py-setuptools', type='build')
