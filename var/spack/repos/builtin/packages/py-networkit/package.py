# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNetworkit(PythonPackage):
    """NetworKit is a growing open-source toolkit for large-scale network
       analysis. Its aim is to provide tools for the analysis of large networks
       in the size range from thousands to billions of edges. For this purpose,
       it implements efficient graph algorithms, many of them parallel to
       utilize multicore architectures. These are meant to compute standard
       measures of network analysis, such as degree sequences, clustering
       coefficients, and centrality measures. In this respect, NetworKit is
       comparable to packages such as NetworkX, albeit with a focus on
       parallelism and scalability."""

    homepage = "https://networkit.github.io/"
    url      = "https://pypi.io/packages/source/n/networkit/networkit-6.1.tar.gz"

    version('7.1', sha256='8609dc7a574a8a82d8880b8b1e3dfdd9c59ad67cd02135628e675c482fe98a96')
    version('7.0', sha256='eea4b5e565d6990b674e1c7f4d598be9377d57b61d0d82883ecc39edabaf3631')
    version('6.1', sha256='f7fcb50dec66a8253f85c10ff9314100de013c7578d531c81d3f71bc6cf8f093')

    # Required dependencies
    depends_on('cmake', type='build')
    depends_on('libnetworkit@7.1', type=('build', 'link'), when='@7.1')
    depends_on('libnetworkit@7.0', type=('build', 'link'), when='@7.0')
    depends_on('libnetworkit@6.1', type=('build', 'link'), when='@6.1')
    depends_on('llvm-openmp', when='%apple-clang')
    depends_on('ninja', type='build')
    depends_on('py-cython', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    phases = ['build_ext', 'install']

    # Overwrite build_ext to enable ext. core-library + parallel build
    def build_ext_args(self, spec, prefix):
        args = ['--networkit-external-core', '-j{0}'.format(make_jobs)]
        return args
