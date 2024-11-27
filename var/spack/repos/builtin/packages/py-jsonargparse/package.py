# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJsonargparse(PythonPackage):
    """An extension to python's argparse which simplifies parsing of configuration options from
    command line arguments, json configuration files (yaml or jsonnet supersets), environment
    variables and hard-coded defaults.
    """

    homepage = "https://github.com/omni-us/jsonargparse"
    pypi = "jsonargparse/jsonargparse-4.19.0.tar.gz"

    license("MIT")

    version("4.28.0", sha256="ac835a290ef18cc2a5309e6bfa8ada9c5d63f46ff18701583fc8f3e95314679c")
    version("4.27.5", sha256="88ad908387ea5c8285a48e7d94bfd025e6f536b0dbae616d755d701248ab85d9")
    version("4.25.0", sha256="4eaadae69c387a3d83a76b1eaf20ca98d5274d8637f180dca0754ce5405adb6b")
    version("4.19.0", sha256="63aa3c7bbdb219d0f254a5ae86f3d54384ebc1ffa905e776cc19283bc843787b")

    variant("signatures", default=False, description="Enable signature features")

    depends_on("py-setuptools@65.6.3:", when="@4.25:", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-wheel@0.38.4:", when="@4.25:", type="build")
    depends_on("py-pyyaml@3.13:", type=("build", "run"))

    with when("+signatures"):
        depends_on("py-typing-extensions@3.10:", when="@4.25: ^python@:3.9", type=("build", "run"))
        depends_on("py-docstring-parser@0.15:", type=("build", "run"))
        depends_on("py-typeshed-client@2.1:", type=("build", "run"))
