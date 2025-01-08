# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class REuropepmc(RPackage):
    """R Interface to the Europe PubMed Central RESTful Web Service.

    An R Client for the Europe PubMed Central RESTful Web Service (see
    <https://europepmc.org/RestfulWebService> for more information). It gives
    access to both metadata on life science literature and open access full
    texts. Europe PMC indexes all PubMed content and other literature sources
    including Agricola, a bibliographic database of citations to the
    agricultural literature, or Biological Patents. In addition to
    bibliographic metadata, the client allows users to fetch citations and
    reference lists. Links between life-science literature and other EBI
    databases, including ENA, PDB or ChEMBL are also accessible. No
    registration or API key is required. See the vignettes for usage
    examples."""

    cran = "europepmc"

    license("GPL-3.0-only")

    version("0.4.3", sha256="25945534527bd89a6dcd9e371e3c2a68f3fe2046587daf1563be16eac9dd1998")
    version("0.4.1", sha256="c1ba91a2a99432cabe18e86fea33ac9d20dbb3ac0b58f430d464b4d8ecba4a9a")
    version("0.4", sha256="d55f62963d0ee84830654bbc78f4ad8285e376b04be137cbeaf8ad2a98b7969c")
    version("0.3", sha256="5044a253d223e2bb8502063cd03c0fe4db856467e497d650da7ccd8f75d0f8d9")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r-httr", type=("build", "run"))
    depends_on("r-jsonlite", type=("build", "run"))
    depends_on("r-plyr", type=("build", "run"))
    depends_on("r-dplyr", type=("build", "run"))
    depends_on("r-progress", type=("build", "run"))
    depends_on("r-urltools", type=("build", "run"))
    depends_on("r-purrr", type=("build", "run"))
    depends_on("r-xml2", type=("build", "run"))
    depends_on("r-tibble", type=("build", "run"), when="@0.4:")
    depends_on("r-tidyr", type=("build", "run"), when="@0.4:")
    depends_on("r-rlang", type=("build", "run"), when="@0.4:")
