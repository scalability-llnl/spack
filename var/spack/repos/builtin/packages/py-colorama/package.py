# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyColorama(PythonPackage):
    """Cross-platform colored terminal text."""

    homepage = "https://github.com/tartley/colorama"
    pypi = "colorama/colorama-0.3.7.tar.gz"

    license("BSD-3-Clause")

    version("0.4.6", sha256="08695f5cb7ed6e0531a20572697297273c47b8cae5a63ffc6d6ed5c201be6e44")
    version("0.4.5", sha256="e6c6b4334fc50988a639d9b98aa429a0b57da6e17b9a44f0451f930b6967b7a4")
    version("0.4.4", sha256="5941b2b48a20143d2267e95b1c2a7603ce057ee39fd88e7329b0c292aa16869b")
    version("0.4.1", sha256="05eed71e2e327246ad6b38c540c4a3117230b19679b875190486ddd2d721422d")
    version("0.3.7", sha256="e043c8d32527607223652021ff648fbb394d5e19cba9f1a698670b338c9d782b")

    depends_on("python@2.7:2,3.7:", when="@0.4.6:", type=("build", "run"))
    depends_on("python@2.7:2,3.5:", when="@0.4.2:", type=("build", "run"))
    depends_on("python@2.7:2,3.4:", type=("build", "run"))
    depends_on("py-setuptools", when="@:0.4.5", type="build")
    depends_on("py-hatchling@0.25.1:", when="@0.4.6:", type="build")
