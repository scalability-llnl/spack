# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPathlib(PythonPackage):
    """Object-oriented filesystem paths.

    Attention: this backport module isn't maintained anymore. If you want to
    report issues or contribute patches, please consider the pathlib2 project
    instead."""

    homepage = "https://pathlib.readthedocs.org/"
    url      = "https://pypi.io/packages/source/p/pathlib/pathlib-1.0.1.tar.gz"

    version('1.0.1', sha256='6940718dfc3eff4258203ad5021090933e5c04707d5ca8cc9e73c94a7894ea9f')
