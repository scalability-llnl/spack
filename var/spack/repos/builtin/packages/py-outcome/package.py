# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOutcome(PythonPackage):
    """Capture the outcome of Python function calls. Extracted from the Trio project."""

    pypi = "outcome/outcome-1.3.0.tar.gz"

    maintainers("paugier")
    license("MIT", checked_by="paugier")

    version(
        "1.3.0.post0", sha256="9dcf02e65f2971b80047b377468e72a268e15c0af3cf1238e6ff14f7f91143b8"
    )
    version("1.2.0", sha256="6f82bd3de45da303cf1f771ecafa1633750a358436a8bb60e06a1ceb745d2672")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-attrs@19.2.0:", type="run")
