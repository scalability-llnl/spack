# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBiocio(RPackage):
    """Standard Input and Output for Bioconductor Packages.

    Implements `import()` and `export()` standard generics for importing and
    exporting biological data formats. `import()` supports whole-file as well
    as chunk-wise iterative import. The `import()` interface optionally
    provides a standard mechanism for 'lazy' access via `filter()` (on row or
    element-like components of the file resource), `select()` (on column-like
    components of the file resource) and `collect()`. The `import()` interface
    optionally provides transparent access to remote (e.g. via https) as well
    as local access. Developers can register a file extension, e.g., `.loom`
    for dispatch from character-based URIs to specific `import()` / `export()`
    methods based on classes representing file types, e.g., `LoomFile()`."""

    bioc = "BiocIO"

    version("1.10.0", commit="1368ff1a7ddbb62515a87a88d7ec39981de557d5")
    version("1.8.0", commit="4a719fa41e014b7b948f7b245e581ede6a04eda1")
    version("1.6.0", commit="60c8aa1a961e43bf0ee5d563a6d9fcec84f7f8f8")
    version("1.4.0", commit="c335932526a38c75dbfa4970c1d90b8a21466d37")

    depends_on("r@4.0.0:", type=("build", "run"))
    depends_on("r@4.0:", type=("build", "run"), when="@1.8.0:")
    depends_on("r@4.3.0:", type=("build", "run"), when="@1.10.0:")
    depends_on("r-biocgenerics", type=("build", "run"))
    depends_on("r-s4vectors", type=("build", "run"))
