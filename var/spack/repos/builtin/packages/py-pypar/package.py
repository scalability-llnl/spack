# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPypar(PythonPackage):
    """Pypar is an efficient but easy-to-use module that allows programs
       written in Python to run in parallel on multiple processors and
       communicate using MPI."""
    homepage = "http://code.google.com/p/pypar/"
    url      = "https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/pypar/pypar-2.1.5_108.tgz"

    version('2.1.5_108', sha256='6076c47d32d48424a07c7b7b29ac16e12cc4b2d28b681b895f94fa76cd82fa12')

    depends_on('mpi')
    depends_on('py-numpy', type=('build', 'run'))

    build_directory = 'source'
