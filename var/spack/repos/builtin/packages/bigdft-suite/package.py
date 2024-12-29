# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class BigdftSuite(BundlePackage):
    """BigDFT-suite: the complete suite of BigDFT for electronic structure calculation
    based on Daubechies wavelets."""

    homepage = "https://bigdft.org/"
    url = "https://gitlab.com/l_sim/bigdft-suite/-/archive/1.9.2/bigdft-suite-1.9.2.tar.gz"
    git = "https://gitlab.com/l_sim/bigdft-suite.git"

    version("develop", branch="devel")
    version("1.9.5")
    version("1.9.4")
    # version("1.9.3") # bigdft-core broken
    version("1.9.2")
    version("1.9.1")
    version("1.9.0")

    depends_on("python@3.0:", type=("run"))

    for vers in ["1.9.0", "1.9.1", "1.9.2", "1.9.4", "1.9.5", "develop"]:
        depends_on("bigdft-futile@{0}".format(vers), when="@{0}".format(vers))
        depends_on("bigdft-psolver@{0}".format(vers), when="@{0}".format(vers))
        depends_on("bigdft-libabinit@{0}".format(vers), when="@{0}".format(vers))
        depends_on("bigdft-chess@{0}".format(vers), when="@{0}".format(vers))
        depends_on("bigdft-core@{0}".format(vers), when="@{0}".format(vers))
        depends_on("bigdft-spred@{0}".format(vers), when="@{0}".format(vers))
        depends_on("bigdft-atlab@{0}".format(vers), when="@{0}".format(vers))
        depends_on("py-bigdft@{0}".format(vers), when="@{0}".format(vers))
