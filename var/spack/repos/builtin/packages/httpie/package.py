# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Httpie(PythonPackage):
    """Modern, user-friendly command-line HTTP client for the API era."""

    homepage = "https://httpie.io/"
    pypi = "httpie/httpie-2.6.0.tar.gz"
    maintainers("BoboTiG")

    license("BSD-3-Clause")

    version("3.2.1", sha256="c9c0032ca3a8d62492b7231b2dd83d94becf3b71baf8a4bbcd9ed1038537e3ec")
    version("2.6.0", sha256="ef929317b239bbf0a5bb7159b4c5d2edbfc55f8a0bcf9cd24ce597daec2afca5")
    version("2.5.0", sha256="fe6a8bc50fb0635a84ebe1296a732e39357c3e1354541bf51a7057b4877e47f9")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-charset-normalizer@2:", when="@2.6:", type=("build", "run"))
    depends_on("py-defusedxml@0.6:", type=("build", "run"))
    depends_on("py-requests@2.11:", type=("build", "run"))
    depends_on("py-requests@2.22:+socks", type=("build", "run"))
    depends_on("py-pygments@2.1.3:", type=("build", "run"))
    depends_on("py-pygments@2.5.2:", type=("build", "run"))
    depends_on("py-requests-toolbelt@0.9.1:", type=("build", "run"))
    depends_on("py-multidict@4.7.0:", when="@3.2.1:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-importlib-metadata@1.4.0:", when="@3: ^python@:3.7", type=("build", "run"))
    depends_on("py-rich@9.10.0:", when="@3.2.1:", type=("build", "run"))
    depends_on("py-colorama@0.2.4:", when="platform=windows", type=("build", "run"))
