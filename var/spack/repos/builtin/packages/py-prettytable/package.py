# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPrettytable(PythonPackage):
    """PrettyTable is a simple Python library designed to make
    it quick and easy to represent tabular data in visually
    appealing ASCII tables.
    """

    homepage = "https://code.google.com/archive/p/prettytable/"
    url      = "https://pypi.io/packages/source/p/prettytable/prettytable-0.7.2.tar.gz"

    version('0.7.2', sha256='2d5460dc9db74a32bcc8f9f67de68b2c4f4d2f01fa3bd518764c69156d9cacd9')

    depends_on("py-setuptools", type='build')
