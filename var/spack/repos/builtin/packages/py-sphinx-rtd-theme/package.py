# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxRtdTheme(PythonPackage):
    """ReadTheDocs.org theme for Sphinx."""

    homepage = "https://github.com/readthedocs/sphinx_rtd_theme"
    pypi = "sphinx-rtd-theme/sphinx_rtd_theme-0.5.1.tar.gz"

    license("MIT")

    version("1.2.2", sha256="01c5c5a72e2d025bd23d1f06c59a4831b06e6ce6c01fdd5ebfe9986c0a880fc7")
    version("1.2.0", sha256="a0d8bd1a2ed52e0b338cbe19c4b2eef3c5e7a048769753dac6a9f059c7b641b8")
    version("1.0.0", sha256="eec6d497e4c2195fa0e8b2016b337532b8a699a68bcb22a512870e16925c6a5c")
    version("0.5.2", sha256="32bd3b5d13dc8186d7a42fc816a23d32e83a4827d7d9882948e7b837c232da5a")
    version("0.5.1", sha256="eda689eda0c7301a80cf122dad28b1861e5605cbf455558f3775e1e8200e83a5")
    version("0.5.0", sha256="22c795ba2832a169ca301cd0a083f7a434e09c538c70beb42782c073651b707d")
    version("0.4.3", sha256="728607e34d60456d736cc7991fd236afb828b21b82f956c5ea75f94c8414040a")

    depends_on("py-setuptools", type="build")

    depends_on("py-sphinx@1.6:6", when="@1:", type=("build", "run"))
    depends_on("py-sphinx@:6", when="@0", type=("build", "run"))
    depends_on("py-docutils@:0.18", when="@1.2:", type=("build", "run"))
    depends_on("py-docutils@:0.17", when="@1:1.1", type=("build", "run"))
    depends_on("py-docutils@:0.16", when="@0.5.2:0", type=("build", "run"))
    depends_on("py-sphinxcontrib-jquery@4", when="@1.2.2:", type=("build", "run"))
    depends_on("py-sphinxcontrib-jquery@2:", when="@1.2:1.2.1", type=("build", "run"))
    conflicts("^py-sphinxcontrib-jquery@3.0.0")

    def setup_build_environment(self, env):
        # Hack to prevent usage of npm in 0.5+
        # https://github.com/readthedocs/sphinx_rtd_theme/issues/1014
        env.set("CI", True)
