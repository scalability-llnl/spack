# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPartd(PythonPackage):
    """Key-value byte store with appendable values."""

    homepage = "https://github.com/dask/partd/"
    pypi = "partd/partd-0.3.8.tar.gz"

    license("BSD-3-Clause", checked_by="wdconinc")

    version("1.4.2", sha256="d022c33afbdc8405c226621b015e8067888173d85f7f5ecebb3cafed9a20f02c")
    version("1.4.1", sha256="56c25dd49e6fea5727e731203c466c6e092f308d8f0024e199d02f6aa2167f67")
    version("1.4.0", sha256="aa0ff35dbbcc807ae374db56332f4c1b39b46f67bf2975f5151e0b4186aed0d5")
    version("1.1.0", sha256="6e258bf0810701407ad1410d63d1a15cfd7b773fd9efe555dac6bb82cc8832b0")
    version("0.3.10", sha256="33722a228ebcd1fa6f44b1631bdd4cff056376f89eb826d7d880b35b637bcfba")
    version("0.3.8", sha256="67291f1c4827cde3e0148b3be5d69af64b6d6169feb9ba88f0a6cfe77089400f")

    depends_on("python@3.5:", type=("build", "run"), when="@1.1.0:")
    depends_on("python@3.7:", type=("build", "run"), when="@1.4.0:")
    depends_on("python@3.9:", type=("build", "run"), when="@1.4.2:")
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@61.2:", type="build", when="@1.4.2:")
    depends_on("py-versioneer@0.29 +toml", type="build", when="@1.4.2:")
    depends_on("py-locket", type=("build", "run"))
    depends_on("py-toolz", type=("build", "run"))
