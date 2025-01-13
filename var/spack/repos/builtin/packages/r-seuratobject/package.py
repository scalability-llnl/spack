# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSeuratobject(RPackage):
    """Data Structures for Single Cell Data.

    Defines S4 classes for single-cell genomic data and associated information,
    such as dimensionality reduction embeddings, nearest-neighbor graphs, and
    spatially-resolved coordinates. Provides data access methods and R-native
    hooks to ensure the Seurat object is familiar to other R users. See Satija
    R, Farrell J, Gennert D, et al (2015) <doi:10.1038/nbt.3192>, Macosko E,
    Basu A, Satija R, et al (2015) <doi:10.1016/j.cell.2015.05.002>, and Stuart
    T, Butler A, et al (2019) <doi:10.1016/j.cell.2019.05.031> for more
    details."""

    cran = "SeuratObject"

    version("5.0.2", sha256="ded30d21f445b7e353fe4a0c4954d45ad19fbe162615d9addf6732f9318ba0cf")
    version("4.1.3", sha256="585d2754f6165a367f0f458523f0a25d4d4160c929c931b27c5603cc6bd986d3")
    version("4.1.2", sha256="6a5945f501b573dbe44a15e7d969e63fd5be0c4f8e9d716b71ca29f695236d0d")
    version("4.1.0", sha256="9ca406cb3bd95c588e1a81c5383e3173a446cc0667142b139ca32685b4b20a05")
    version("4.0.4", sha256="585261b7d2045193accf817a29e2e3356e731f57c554bed37d232fa49784088c")

    depends_on("r@4.0.0:", type=("build", "run"))
    depends_on("r@4.1.0:", when="@5.0.2:", type=("build", "run"))
    depends_on("r-future", type=("build", "run"), when="@4.1.0:")
    depends_on("r-future-apply", type=("build", "run"), when="@4.1.0:")
    depends_on("r-generics", when="@5:", type=("build", "run"))
    depends_on("r-lifecycle", when="@5:", type=("build", "run"))
    depends_on("r-matrix@1.3-3:", type=("build", "run"))
    depends_on("r-matrix@1.5-0:", type=("build", "run"), when="@4.1.2:")
    depends_on("r-matrix@1.6-4:", when="@5.0.2:", type=("build", "run"))
    depends_on("r-progressr", type=("build", "run"), when="@4.1.0:")
    depends_on("r-rcpp@1.0.5:", type=("build", "run"))
    depends_on("r-sp", type=("build", "run"), when="@4.1.0:")
    depends_on("r-sp@1.5-0:", type=("build", "run"), when="@4.1.2:")
    depends_on("r-spam", when="@5:", type=("build", "run"))
    depends_on("r-rlang@0.4.7:", type=("build", "run"))
    depends_on("r-rcppeigen", type=("build", "run"))

    depends_on("r-rgeos", type=("build", "run"), when="@4.1.0:4.1.2")
