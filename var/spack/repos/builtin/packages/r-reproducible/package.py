# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RReproducible(RPackage):
    """A Set of Tools that Enhance Reproducibility Beyond Package Management

    Collection of high-level, machine- and OS-independent tools for
    making deeply reproducible and reusable content in R. The two
    workhorse functions are Cache and prepInputs; these allow for:
    nested caching, robust to environments, and objects with
    environments (like functions); and data retrieval and processing
    in continuous workflow environments. In all cases, efforts are
    made to make the first and subsequent calls of functions have
    the same result, but vastly faster at subsequent times by way of
    checksums and digesting. Several features are still under active
    development, including cloud storage of cached objects, allowing
    for sharing between users. Several advanced options are
    available, see ?reproducibleOptions."""

    homepage = "https://reproducible.predictiveecology.org/"
    url      = "https://cloud.r-project.org/src/contrib/reproducible_1.2.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/reproducible"

    maintainers = ['dorton21']

    version('1.2.4', sha256='0525deefa6a0713c3fe2da8bfc529f62d6352bebf2ef08866503b4853412f149')

    depends_on('r@3.5:', type=('build', 'run'))
    depends_on('r-data-table@1.10.4:', type=('build', 'run'))
    depends_on('r-dbi', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-fpcompare', type=('build', 'run'))
    depends_on('r-glue', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-require', type=('build', 'run'))
    depends_on('r-raster', type=('build', 'run'))
    depends_on('r-rsqlite', type=('build', 'run'))
    depends_on('r-rlang', type=('build', 'run'))
    depends_on('r-sp@1.4-2:', type=('build', 'run'))
    depends_on('unrar', type=('build', 'run'))
