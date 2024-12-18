# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHttpstan(PythonPackage):
    """HTTP-based REST interface to Stan, a package for Bayesian inference."""

    homepage = "https://mc-stan.org/"
    url = "https://github.com/stan-dev/httpstan/archive/refs/tags/4.6.1.tar.gz"

    maintainers("haralmha")

    license("ISC")

    version("4.8.0", sha256="cadfce05d24ec2af50d71c5212c648cbee5684a7f98fedd3838e124e5a9b4962")
    version("4.7.2", sha256="94f6631d969cbd91d136194b074d02642d8c9e2a05674877a39059be87c5bf7b")
    version("4.6.1", sha256="703e5e04e60651e0004574bb9695827d759fd13eb0d6bd67f827c1bfa0a1fd31")

    depends_on("cxx", type="build")  # generated

    depends_on("python@3.8:3", type=("build", "run"), when="@4.7:")
    depends_on("python@3.7:3", type=("build", "run"), when="@:4.6")
    depends_on("py-setuptools@41.0:", type=("build", "run"))
    depends_on("py-poetry-core@1.0.0:", type="build")
    depends_on("py-aiohttp@3.7:3", type=("build", "run"))
    depends_on("py-appdirs@1.4:1", type=("build", "run"))
    depends_on("py-webargs@8.0:8", type=("build", "run"))
    depends_on("py-marshmallow@3.10:3", type=("build", "run"))
    depends_on("py-numpy@1.19:1", type=("build", "run"), when="@4.7:")
    depends_on("py-numpy@1.16:1", type=("build", "run"), when="@:4.6")
    depends_on("py-pybind11")
