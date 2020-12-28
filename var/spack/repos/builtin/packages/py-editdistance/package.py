# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEditdistance(PythonPackage):
    """Fast implementation of the edit distance (Levenshtein distance)."""

    homepage = "https://github.com/aflc/editdistance"
    url      = "https://pypi.io/packages/source/e/editdistance/editdistance-0.4.tar.gz"

    version('0.4', sha256='c765db6f8817d38922e4a50be4b9ab338b2c539377b6fcf0bca11dea72eeb8c1')

    depends_on('py-setuptools', type='build')
