# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHtseq(PythonPackage):
    """HTSeq is a Python package that provides infrastructure to process
    data from high-throughput sequencing assays."""

    homepage = "http://htseq.readthedocs.io/en/release_0.9.1/overview.html"
    url      = "https://github.com/simon-anders/htseq/archive/release_0.9.1.tar.gz"

    version('0.11.2', sha256='dfc707effa699d5ba9034e1bb9f13c0fb4e9bc60d31ede2444aa49c7e2fc71aa')
    version('0.9.1', sha256='28b41d68aa233fce0d57699e649b69bb11957f8f1b9b7b82dfe3415849719534')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-pysam', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-cython', type=('build', 'run'))
    depends_on('swig', type=('build', 'run'))
