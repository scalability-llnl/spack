# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RYulabUtils(RPackage):
    """Supporting Functions for Packages Maintained by 'YuLab-SMU'.

    Miscellaneous functions commonly used by 'YuLab-SMU'."""

    cran = "yulab.utils"

    version("0.1.6", sha256="589be7ad1425f7d84dc3748f352fc432e494edb725209c05e28ca2a44f34beec")
    version("0.0.6", sha256="973a51b8d1284060aec34e94849eea6783439dbcbf85083dd4f1a5df4f927b25")
    version("0.0.5", sha256="6ecd4dc5dae40e86b7a462fdac3ab8c0b276dcae5a284eb43390a05b01e3056b")
    version("0.0.4", sha256="38850663de53a9166b8e85deb85be1ccf1a5b310bbe4355f3b8bc823ed1b49ae")

    depends_on("r-cli", when="@0.1.0:", type=("build", "run"))
    depends_on("r-digest", when="@0.1.0:", type=("build", "run"))
    depends_on("r-fs", when="@0.1.0:", type=("build", "run"))
    depends_on("r-httr2", when="@0.1.6:", type=("build", "run"))
    depends_on("r-rlang", when="@0.0.7:", type=("build", "run"))

    depends_on("r-memoise", when="@0.0.7:0.1.5", type=("build", "run"))
