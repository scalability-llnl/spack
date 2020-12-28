# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDeprecation(PythonPackage):
    """The deprecation library provides a deprecated decorator and a
    fail_if_not_removed decorator for your tests. """

    homepage = "http://deprecation.readthedocs.io/"
    url      = "https://pypi.io/packages/source/d/deprecation/deprecation-2.0.7.tar.gz"

    version('2.0.7', sha256='c0392f676a6146f0238db5744d73e786a43510d54033f80994ef2f4c9df192ed')

    depends_on('py-setuptools', type='build')
    depends_on('py-packaging', type='build')
