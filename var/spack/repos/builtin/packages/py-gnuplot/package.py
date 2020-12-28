# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGnuplot(PythonPackage):
    """Gnuplot.py is a Python package that allows you to create graphs from
       within Python using the gnuplot plotting program."""
    homepage = "http://gnuplot-py.sourceforge.net/"
    url      = "http://downloads.sourceforge.net/project/gnuplot-py/Gnuplot-py/1.8/gnuplot-py-1.8.tar.gz"

    version('1.8', sha256='ab339be7847d30a8acfd616f27b5021bfde0999b7bf2d68400fbe62c53106e21')

    depends_on('py-numpy', type=('build', 'run'))
