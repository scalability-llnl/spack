# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPathlib2(PythonPackage):
    """Backport of pathlib from python 3.4"""

    pypi = "pathlib2/pathlib2-2.3.2.tar.gz"

    license("MIT")

    version(
        "2.3.7.post1", sha256="9fe0edad898b83c0c3e199c842b27ed216645d2e177757b2dd67384d4113c641"
    )
    version("2.3.6", sha256="7d8bcb5555003cdf4a8d2872c538faa3a0f5d20630cb360e518ca3b981795e5f")
    version("2.3.3", sha256="25199318e8cc3c25dcb45cbe084cc061051336d5a9ea2a12448d3d8cb748f742")
    version("2.3.2", sha256="8eb170f8d0d61825e09a95b38be068299ddeda82f35e96c3301a8a5e7604cb83")
    version("2.1.0", sha256="deb3a960c1d55868dfbcac98432358b92ba89d95029cddd4040db1f27405055c")

    depends_on("py-setuptools", type="build")
    depends_on("py-six", type=("build", "run"))
