# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RVroom(RPackage):
    """Read and Write Rectangular Text Data Quickly.

    The goal of 'vroom' is to read and write data (like 'csv', 'tsv' and
    'fwf') quickly. When reading it uses a quick initial indexing step, then
    reads the values lazily , so only the data you actually use needs to be
    read. The writer formats the data in parallel and writes to disk
    asynchronously from formatting."""

    cran = "vroom"

    license("MIT")

    version("1.6.5", sha256="7bdca21e58c9c5049d7445d182f59fd399193cb2f4318d083de0a559ec9b5761")
    version("1.6.1", sha256="eb0e33d53212f9c7e8b38d632c98bd5015365cc13f55dadb15ff0d404b31807c")
    version("1.6.0", sha256="a718ccdf916442693af5392944774d8aec5ce48f417871f9de84dd1089d26ca6")
    version("1.5.7", sha256="d087cb148f71c222fc89199d03df2502689149873414a6d89c2f006d3a109fde")
    version("1.5.5", sha256="1d45688c08f162a3300eda532d9e87d144f4bc686769a521bf9a12e3d3b465fe")

    depends_on("r@3.1:", type=("build", "run"))
    depends_on("r@3.4:", type=("build", "run"), when="@1.6.0:")
    depends_on("r@3.6:", type=("build", "run"), when="@1.6.4:")
    depends_on("r-bit64", type=("build", "run"))
    depends_on("r-crayon", type=("build", "run"))
    depends_on("r-cli", type=("build", "run"))
    depends_on("r-cli@3.2.0:", type=("build", "run"), when="@1.6.0:")
    depends_on("r-glue", type=("build", "run"))
    depends_on("r-hms", type=("build", "run"))
    depends_on("r-lifecycle", type=("build", "run"))
    depends_on("r-lifecycle@1.0.3:", type=("build", "run"), when="@1.6.1:")
    depends_on("r-rlang@0.4.2:", type=("build", "run"))
    depends_on("r-tibble@2.0.0:", type=("build", "run"))
    depends_on("r-tzdb@0.1.1:", type=("build", "run"))
    depends_on("r-vctrs@0.2.0:", type=("build", "run"))
    depends_on("r-tidyselect", type=("build", "run"))
    depends_on("r-withr", type=("build", "run"))
    depends_on("r-progress@1.2.1:", type=("build", "run"))
    depends_on("r-cpp11@0.2.0:", type=("build", "run"))
