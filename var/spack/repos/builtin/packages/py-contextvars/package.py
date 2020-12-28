# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyContextvars(PythonPackage):
    """This package implements a backport of Python 3.7 contextvars module
    (see PEP 567) for Python 3.6."""

    homepage = "https://github.com/MagicStack/contextvars"
    url      = "https://pypi.io/packages/source/c/contextvars/contextvars-2.4.tar.gz"

    version('2.4', sha256='f38c908aaa59c14335eeea12abea5f443646216c4e29380d7bf34d2018e2c39e')

    depends_on('py-setuptools', type='build')
    depends_on('py-immutables@0.9:', type=('build', 'run'))
