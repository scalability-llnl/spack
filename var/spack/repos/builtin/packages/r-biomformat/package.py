# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBiomformat(RPackage):
    """An interface package for the BIOM file format.

    This is an R package for interfacing with the BIOM format. This package
    includes basic tools for reading biom-format files, accessing and
    subsetting data tables from a biom object (which is more complex than a
    single table), as well as limited support for writing a biom-object back
    to a biom-format file. The design of this API is intended to match the
    python API and other tools included with the biom-format project, but
    with a decidedly "R flavor" that should be familiar to R users. This
    includes S4 classes and methods, as well as extensions of common core
    functions/methods."""

    bioc = "biomformat"

    version("1.28.0", commit="9240e78dc378abcf6c62ef8dbf2e60f7241232a3")
    version("1.26.0", commit="f851ba2428b57769f6fbb287874bad0dc84dd69c")
    version("1.24.0", commit="4e14692dbcc34c3bd51defd74c728df5de9d0829")
    version("1.22.0", commit="ab7c6411a038fec010baa72e663f362fd972cb34")
    version("1.18.0", commit="dc18859c139f4d76805adb6f01e199573cdd5a8b")
    version("1.12.0", commit="6e946123bb59da262cbb0c17dc5ab49328a89d4a")
    version("1.10.1", commit="e67c6f4b70201f748fa49a4938e1af0cd0613f09")
    version("1.8.0", commit="acd207377b24e4d8310eaff06c16dcfe6c04509a")
    version("1.6.0", commit="61fb8c7b34ad561c3c46cacc0dd1957be56da85e")
    version("1.4.0", commit="83b4b1883bc56ea93a0a6ca90fc1b18712ef0f1a")

    depends_on("r@3.2:", type=("build", "run"))
    depends_on("r-plyr@1.8:", type=("build", "run"))
    depends_on("r-jsonlite@0.9.16:", type=("build", "run"))
    depends_on("r-matrix@1.2:", type=("build", "run"))
    depends_on("r-rhdf5", type=("build", "run"))
