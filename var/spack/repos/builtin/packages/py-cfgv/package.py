# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCfgv(PythonPackage):
    """Validate configuration and produce human readable error messages."""

    homepage = "https://github.com/asottile/cfgv/"
    pypi = "cfgv/cfgv-2.0.1.tar.gz"

    license("MIT")

    version("3.4.0", sha256="e52591d4c5f5dead8e0f673fb16db7949d2cfb3f7da4582893288f0ded8fe560")
    version("3.3.1", sha256="f5a830efb9ce7a445376bb66ec94c638a9787422f96264c98edc6bdeed8ab736")
    version("2.0.1", sha256="edb387943b665bf9c434f717bf630fa78aecd53d5900d2e05da6ad6048553144")

    depends_on("python@3.8:", when="@3.4:", type=("build", "run"))
    depends_on("python@3.6.1:", when="@3.1:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    # Historical dependencies
    depends_on("py-six", when="@:2", type=("build", "run"))
