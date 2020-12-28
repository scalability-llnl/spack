# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPlanar(PythonPackage):
    """2D planar geometry library for Python."""

    homepage = "https://bitbucket.org/caseman/planar/src/default/"
    url      = "https://pypi.io/packages/source/p/planar/planar-0.4.zip"

    version('0.4', sha256='cbfb9cbae8b0e296e6e7e3552b7d685c7ed5cae295b7a61f2b2b096b231dad76')
