# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxDesign(PythonPackage):
    """A sphinx extension for designing beautiful, screen-size responsive web components."""

    homepage = "https://sphinx-design.readthedocs.io"
    pypi = "sphinx-design/sphinx_design-0.3.0.tar.gz"

    maintainers("ax3l", "adamjstewart")

    license("MIT")

    version("0.6.1", sha256="b44eea3719386d04d765c1a8257caca2b3e6f8421d7b3a5e742c0fd45f84e632")
    version("0.6.0", sha256="ec8e3c5c59fed4049b3a5a2e209360feab31829346b5f6a0c7c342b894082192")
    version("0.5.0", sha256="e8e513acea6f92d15c6de3b34e954458f245b8e761b45b63950f65373352ab00")
    version("0.4.1", sha256="5b6418ba4a2dc3d83592ea0ff61a52a891fe72195a4c3a18b2fa1c7668ce4708")
    version("0.4.0", sha256="b92948614900967499617d99aadd38ce5975ede924a18c7478cc6b8ec188f76b")
    version("0.3.0", sha256="7183fa1fae55b37ef01bda5125a21ee841f5bbcbf59a35382be598180c4cefba")

    depends_on("python@3.7:", type=("build", "run"), when="@:0.4")
    depends_on("python@3.8:", type=("build", "run"), when="@0.5")
    depends_on("python@3.9:", type=("build", "run"), when="@0.6:")
    depends_on("py-flit-core@3.4:3", type=("build"))
    depends_on("py-sphinx@4:5", when="@0.3", type=("build", "run"))
    depends_on("py-sphinx@4:6", when="@0.4", type=("build", "run"))
    depends_on("py-sphinx@5:7", when="@0.5:0.6.0", type=("build", "run"))
    depends_on("py-sphinx@6:8", when="@0.6.1:", type=("build", "run"))
