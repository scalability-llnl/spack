# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPicmistandard(PythonPackage):
    """Standard input format for Particle-In-Cell codes"""

    homepage = "https://picmi-standard.github.io"
    git = "https://github.com/picmi-standard/picmi.git"
    pypi = "picmistandard/picmistandard-0.30.0.tar.gz"

    maintainers("ax3l", "dpgrote", "RemiLehe")

    version("master", branch="master")
    version("0.30.0", sha256="28b892b242e0cc044ad987d6bdc12811fe4a478d5096d6bc5989038ee9d9dab6")
    version("0.29.0", sha256="dc0bf3ddd3635df9935ac569b3085de387150c4f8e9851897078bb12d123dde8")
    version("0.28.0", sha256="aa980b0fb49fc3ff9c7e32b5927b3700c4660aefbf96567bac1f8c9c93bb7831")
    version("0.26.0", sha256="b22689f576d064bf0cd8f435621e912359fc2ee9347350eab845d2d36ebb62eb")
    version("0.25.0", sha256="3fe6a524822d382e52bfc9d3378249546075d28620969954c5ffb43e7968fb02")
    version("0.24.0", sha256="55a82adcc14b41eb612caf0d9e47b0e2a56ffc196a58b41fa0cc395c6924be9a")
    version("0.23.2", sha256="2853fcfaf2f226a88bb6063ae564832b7e69965294fd652cd2ac04756fa4599a")
    version("0.23.1", sha256="c7375010b7a3431b519bc0accf097f2aafdb520e2a0126f42895cb96dcc7dcf1")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-numpy@1.15:1", type=("build", "run"))
    depends_on("py-scipy@1.5:1", type=("build", "run"))
    depends_on("py-setuptools", type="build")
