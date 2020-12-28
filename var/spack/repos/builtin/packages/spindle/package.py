# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Spindle(AutotoolsPackage):
    """Spindle improves the library-loading performance of dynamically
       linked HPC applications.  Without Spindle large MPI jobs can
       overload on a shared file system when loading dynamically
       linked libraries, causing site-wide performance problems.
    """
    homepage = "https://computing.llnl.gov/project/spindle/"
    url      = "https://github.com/hpc/Spindle/archive/v0.8.1.tar.gz"

    version('0.8.1', sha256='c1e099e913faa8199be5811dc7b8be0266f0d1fd65f0a3a25bb46fbc70954ed6')

    depends_on("launchmon")
