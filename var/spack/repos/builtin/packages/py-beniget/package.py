# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBeniget(PythonPackage):
    """Extract semantic information about static Python code."""

    homepage = "https://github.com/serge-sans-paille/beniget/"
    pypi = "beniget/beniget-0.3.0.tar.gz"

    license("BSD-3-Clause")

    version("0.4.1", sha256="75554b3b8ad0553ce2f607627dad3d95c60c441189875b98e097528f8e23ac0c")
    version("0.4.0", sha256="72bbd47b1ae93690f5fb2ad3902ce1ae61dcd868ce6cfbf33e9bad71f9ed8749")
    version("0.3.0", sha256="062c893be9cdf87c3144fb15041cce4d81c67107c1591952cd45fdce789a0ff1")
    version("0.2.3", sha256="350422b0598c92fcc5f8bcaf77f2a62f6744fb8f2fb495b10a50176c1283639f")

    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-gast@0.5.0:0.5", when="@0.4.0:", type=("build", "run"))
    depends_on("py-gast@0.4.0:0.4", when="@0.3.0:0.3", type=("build", "run"))
    depends_on("py-gast@0.3.3:0.3", when="@:0.2", type=("build", "run"))
