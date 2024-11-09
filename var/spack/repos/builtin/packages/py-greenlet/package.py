# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGreenlet(PythonPackage):
    """Lightweight in-process concurrent programming"""

    homepage = "https://github.com/python-greenlet/greenlet"
    pypi = "greenlet/greenlet-0.4.17.tar.gz"

    # Requires objgraph
    skip_modules = ["greenlet.tests"]

    license("MIT AND PSF-2.0", checked_by="tgamblin")

    version("3.0.0a1", sha256="1bd4ea36f0aeb14ca335e0c9594a5aaefa1ac4e2db7d86ba38f0be96166b3102")
    version(
        "2.0.2",
        sha256="e7c8dc13af7db097bed64a051d2dd49e9f0af495c26995c00a9ee842690d34c0",
        preferred=True,
    )
    version("1.1.3", sha256="bcb6c6dd1d6be6d38d6db283747d07fda089ff8c559a835236560a4410340455")
    version("1.1.2", sha256="e30f5ea4ae2346e62cedde8794a56858a67b878dd79f7df76a0767e356b1744a")
    version("1.1.0", sha256="c87df8ae3f01ffb4483c796fe1b15232ce2b219f0b18126948616224d3f658ee")
    version("0.4.17", sha256="41d8835c69a78de718e466dd0e6bfd4b46125f21a67c3ff6d76d8d8059868d6b")
    version("0.4.13", sha256="0fef83d43bf87a5196c91e73cb9772f945a4caaff91242766c5916d1dd1381e4")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    with default_args(type=("build", "link", "run")):
        depends_on("python")
        depends_on("python@:3.11", when="@:2")
        depends_on("python@:3.12", when="@:3.0")

    depends_on("py-setuptools", type="build")
