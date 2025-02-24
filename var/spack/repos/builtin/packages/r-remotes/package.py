# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRemotes(RPackage):
    """R Package Installation from Remote Repositories, Including 'GitHub'.

    Download and install R packages stored in 'GitHub', 'BitBucket', or plain
    'subversion' or 'git' repositories. This package provides the 'install_*'
    functions in 'devtools'. Indeed most of the code was copied over from
    'devtools'."""

    cran = "remotes"

    license("MIT")

    version("2.5.0", sha256="4d663f1426cd88d42f4070f23d969305c575e0499ed1397be6607b0770d2850c")
    version("2.4.2", sha256="f2ef875f24a485bf4f55a8c830f87cdd5db868f9a8cdb624dc452d0bf66ba516")
    version("2.2.0", sha256="12f234fd8c46f4ac54e06a3c60e4015ed2193a32762ca4dd6854f120136f33b8")
    version("2.1.1", sha256="4e590746fce618094089372b185e1ea234b3337b23c44c44118e942d0fb5118b")
    version("2.1.0", sha256="8944c8f6fc9f0cd0ca04d6cf1221b716eee08facef9f4b4c4d91d0346d6d68a7")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("subversion", type="run")
    depends_on("git", type="run")
