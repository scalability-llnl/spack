# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCallr(RPackage):
    """Call R from R.

    It is sometimes useful to perform a computation in a separate R process,
    without affecting the current R process at all. This packages does exactly
    that."""

    cran = "callr"

    license("MIT")

    version("3.7.6", sha256="e4bce367e869e42eaeea05566d2033d8cee2103179b11cd9a401440b58a351f8")
    version("3.7.3", sha256="567bfedf073a1d4c5785f0553341608a214938110567b9a6495ff20ebb2fd04e")
    version("3.7.2", sha256="12da8a212679e450d8d43c3c6e61ed09b82047f376f316f6f6392f1638580307")
    version("3.7.0", sha256="d67255148595c6d0ba4c4d241bc9f6b5e00cafe25fdc13e38c10acc38653360a")
    version("3.5.1", sha256="ce338c648cc9ab501168a55f93e68fc81e31dc5ec881e908b5b4a9d6f5bd8696")
    version("3.4.3", sha256="01b7277f20c1d662c6bebbfa2798d179922b36d4148b4298853579aeda0382b5")
    version("3.3.1", sha256="bf60da47357d3336aa395b0c9643235a621763c80d28bc9bb2257767d0a37967")
    version("3.2.0", sha256="4bb47b1018e8eb5c683a86c05d0d9b8b25848db1f1b30e92cfebedc0ce14b0e8")
    version("3.0.0", sha256="e36361086c65660a6ecbbc09b5ecfcddee6b59caf75e983e48b21d3b8defabe7")
    version("1.0.0", sha256="2c56808c723aba2ea8a8b6bbdc9b8332c96f59b119079861dd52f5988c27f715")

    depends_on("r@3.4:", type=("build", "run"), when="@3.7.2:")

    depends_on("r-processx@3.4.0:", type=("build", "run"), when="@3.0.0:")
    depends_on("r-processx@3.5.0:", type=("build", "run"), when="@3.6.0:")
    depends_on("r-processx@3.6.1:", type=("build", "run"), when="@3.7.2:")
    depends_on("r-r6", type=("build", "run"), when="@3.0.0:")
