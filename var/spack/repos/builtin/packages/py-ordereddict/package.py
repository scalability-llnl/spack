# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOrdereddict(PythonPackage):
    """A drop-in substitute for Py2.7's new collections.
    OrderedDict that works in Python 2.4-2.6."""

    homepage = "https://pypi.python.org/pypi/ordereddict"
    url      = "https://pypi.io/packages/source/o/ordereddict/ordereddict-1.1.tar.gz"

    version('1.1', sha256='1c35b4ac206cef2d24816c89f89cf289dd3d38cf7c449bb3fab7bf6d43f01b1f')
