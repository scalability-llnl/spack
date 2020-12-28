# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAnnotationforge(RPackage):
    """Tools for building SQLite-based annotation data packages.

       Provides code for generating Annotation packages and their databases.
       Packages produced are intended to be used with AnnotationDbi."""

    homepage = "https://bioconductor.org/packages/AnnotationForge"
    git      = "https://git.bioconductor.org/packages/AnnotationForge.git"

    version('1.26.0', commit='5d181f32df1fff6446af64a2538a7d25c23fe46e')
    version('1.24.0', commit='3e1fe863573e5b0f69f35a9ad6aebce11ef83d0d')
    version('1.22.2', commit='8eafb1690c1c02f6291ccbb38ac633d54b8217f8')
    version('1.20.0', commit='7b440f1570cb90acce8fe2fa8d3b5ac34f638882')
    version('1.18.2', commit='44ca3d4ef9e9825c14725ffdbbaa57ea059532e1')

    depends_on('r@2.7.0:', type=('build', 'run'))
    depends_on('r-biocgenerics@0.15.10:', type=('build', 'run'))
    depends_on('r-biobase@1.17.0:', type=('build', 'run'))
    depends_on('r-annotationdbi@1.33.14:', type=('build', 'run'))
    depends_on('r-dbi', type=('build', 'run'))
    depends_on('r-rsqlite', type=('build', 'run'))
    depends_on('r-xml', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-rcurl', type=('build', 'run'))
