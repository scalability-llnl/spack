# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTsne(RPackage):
    """A "pure R" implementation of the t-SNE algorithm."""

    homepage = "https://cloud.r-project.org/package=tsne"
    url      = "https://cloud.r-project.org/src/contrib/tsne_0.1-3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/tnse"

    version('0.1-3', sha256='66fdf5d73e69594af529a9c4f261d972872b9b7bffd19f85c1adcd66afd80c69')
    version('0.1-2', sha256='c6c3455e0f0f5dcac14299b3dfeb1a5f1bfe5623cdaf602afc892491d3d1058b')
    version('0.1-1', sha256='c953991215a660cf144e55848d2507bcf7932618e164b0e56901fb33831fd1d3')
