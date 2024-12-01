# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAnnotate(RPackage):
    """Annotation for microarrays.

    Using R enviroments for annotation."""

    bioc = "annotate"

    version("1.78.0", commit="ca6415a463ec682f340ba5d1dc6246a92e836143")
    version("1.76.0", commit="0181d5c41d594e36be06adb6a02302db0ad2c507")
    version("1.74.0", commit="200c71743417792880f8171d59b2ac0ddd3902a8")
    version("1.72.0", commit="67ac76a9ff6d60dc1620763d3aa98aef39443110")
    version("1.68.0", commit="98cdb12c612b3f3fc06329a89a1ffb0a92b555c0")
    version("1.62.0", commit="19af0b39747ea83fe8fe9b8bbb6036363bc815cd")
    version("1.60.1", commit="9d8f87db02bf0c1593e79da754335a24d3a8ed16")
    version("1.58.0", commit="d1b5dd5feb8793f4f816d9a4aecbebb5ec7df7bc")
    version("1.56.2", commit="95ec3b004f5356bd78b2a60cbf7f93e0d48cf346")
    version("1.54.0", commit="860cc5b696795a31b18beaf4869f9c418d74549e")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-annotationdbi@1.27.5:", type=("build", "run"))
    depends_on("r-xml", type=("build", "run"))
    depends_on("r-biobase", type=("build", "run"))
    depends_on("r-dbi", type=("build", "run"))
    depends_on("r-xtable", type=("build", "run"))
    depends_on("r-biocgenerics@0.13.8:", type=("build", "run"))
    depends_on("r-httr", type=("build", "run"), when="@1.68.0:")

    depends_on("r-rcurl", type=("build", "run"), when="@:1.62.0")
