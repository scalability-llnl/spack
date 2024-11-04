# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySphinxTabs(PythonPackage):
    """Create tabbed content in Sphinx documentation when building HTML."""

    homepage = "https://github.com/executablebooks/sphinx-tabs"
    pypi = "sphinx-tabs/sphinx-tabs-3.2.0.tar.gz"

    maintainers("schmitts")

    license("MIT")

    version("3.4.5", sha256="ba9d0c1e3e37aaadd4b5678449eb08176770e0fc227e769b6ce747df3ceea531")
    version("3.4.4", sha256="f1b72c4f23d1ba9cdcaf880fd883524bc70689f561b9785719b8b3c3c5ed0aca")
    version("3.4.1", sha256="d2a09f9e8316e400d57503f6df1c78005fdde220e5af589cc79d493159e1b832")
    version("3.3.1", sha256="d10dd7fb2700329b8e5948ab9f8e3ef54fff30f79d2e42cfd1b0089ae26e8c5e")
    version("3.2.0", sha256="33137914ed9b276e6a686d7a337310ee77b1dae316fdcbce60476913a152e0a4")

    depends_on("python@3.6:3", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-sphinx", type=("build", "run"), when="@3.4.1:")
    depends_on("py-sphinx@2:4", type=("build", "run"), when="@:3.3.1")
    depends_on("py-pygments", type=("build", "run"))

    depends_on("py-docutils@0.16", when="@3.2.0", type=("build", "run"))
    depends_on("py-docutils@0.17", when="@3.3.1", type=("build", "run"))
    depends_on("py-docutils@0.18", when="@3.4.1:", type=("build", "run"))
