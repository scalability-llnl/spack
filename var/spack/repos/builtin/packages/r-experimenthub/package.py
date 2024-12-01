# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RExperimenthub(RPackage):
    """Client to access ExperimentHub resources.

    This package provides a client for the Bioconductor ExperimentHub web
    resource. ExperimentHub provides a central location where curated data from
    experiments, publications or training courses can be accessed. Each
    resource has associated metadata, tags and date of modification. The client
    creates and manages a local cache of files retrieved enabling quick and
    reproducible access."""

    bioc = "ExperimentHub"

    version("2.8.0", commit="f25c854c51878844098290a05936cb35b235f30e")
    version("2.6.0", commit="557ba29720bce85902a85445dd0435b7356cdd7f")
    version("2.4.0", commit="bdce35d3a89e8633cc395f28991e6b5d1eccbe8e")
    version("2.2.1", commit="4e10686fa72baefef5d2990f41a7c44c527a7a7d")
    version("1.16.1", commit="61d51b7ca968d6cc1befe299e0784d9a19ca51f6")

    depends_on("r-biocgenerics@0.15.10:", type=("build", "run"))
    depends_on("r-annotationhub@2.19.3:", type=("build", "run"))
    depends_on("r-annotationhub@3.3.6:", type=("build", "run"), when="@2.4.0:")
    depends_on("r-biocfilecache@1.5.1:", type=("build", "run"))
    depends_on("r-s4vectors", type=("build", "run"))
    depends_on("r-biocmanager", type=("build", "run"))
    depends_on("r-rappdirs", type=("build", "run"))
    depends_on("r-curl", type=("build", "run"), when="@:2.6.0")
