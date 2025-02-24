# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCluster(RPackage):
    """ "Finding Groups in Data": Cluster Analysis Extended Rousseeuw et al.

    Methods for Cluster analysis. Much extended the original from Peter
    Rousseeuw, Anja Struyf and Mia Hubert, based on Kaufman and Rousseeuw
    (1990) "Finding Groups in Data"."""

    cran = "cluster"

    license("GPL-2.0-or-later")

    version("2.1.6", sha256="d1c50efafd35a55387cc5b36086b97d5591e0b33c48dc718005d2f5907113164")
    version("2.1.4", sha256="c6f10ceca29a176ba833f24ebf71fd451629052c2338398ba286df5689d6f5b6")
    version("2.1.3", sha256="a3ad7a9455d634c4e0c6ccf8ea7a3a392a0ecf9c2bdb368d127ffa68a93164a9")
    version("2.1.2", sha256="5c8aa760fb6dda4fcfe6196e561ffcd2dc12b1a6c7659cb90be2cde747311499")
    version("2.1.0", sha256="eaf955bef8f616ea563351ec7f597c445aec43e65991ca975e382ef1fd70aa14")
    version("2.0.7-1", sha256="b10141090cf3c2b62260611a0ea822eb2f7bab9f4fd656c48bdc12b65c5c3dbf")
    version("2.0.5", sha256="4b309133bc2ad7b8fe4fa538dd69635bc8a4cd724a3c95f01084098876c57bae")
    version("2.0.4", sha256="d4d925c4fc1fc4f2e2e3c9208e518507aad6c28bb143b4358a05a8a8944ac6e4")

    depends_on("r@3.0.1:", type=("build", "run"))
    depends_on("r@3.2.0:", type=("build", "run"), when="@2.0.7:")
    depends_on("r@3.3.0:", type=("build", "run"), when="@2.0.8:")
    depends_on("r@3.4.0:", type=("build", "run"), when="@2.1.2:")
    depends_on("r@3.5.0:", type=("build", "run"), when="@2.1.3:")
