# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyShroud(PythonPackage):
    """Create Fortran wrappers for a C++ library."""

    homepage = "https://github.com/LLNL/shroud"
    git      = "https://github.com/LLNL/shroud.git"

    version('develop', branch='develop')
    version('master',  branch='master')
    version('0.12.1', tag='v0.12.1')
    version('0.11.0', tag='v0.11.0')
    version('0.10.1', tag='v0.10.1')
    version('0.9.0', tag='v0.9.0')
    version('0.8.0', tag='v0.8.0')

    depends_on("py-setuptools", type=('build', 'run'))
    depends_on("py-pyyaml@4.2b1:", type=('build', 'run'))
