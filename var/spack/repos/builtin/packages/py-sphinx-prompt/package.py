# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxPrompt(PythonPackage):
    """Sphinx directive to add unselectable prompt."""

    homepage = "https://github.com/sbrunner/sphinx-prompt"
    pypi = "sphinx_prompt/sphinx_prompt-1.8.0.tar.gz"

    maintainers("LydDeb")

    version("1.8.0", sha256="47482f86fcec29662fdfd23e7c04ef03582714195d01f5d565403320084372ed")
    version("1.1.0", sha256="3d9cf382b750291f73d1f6f1713c4af0557c30208af124cd3d8731e607a4febf")

    depends_on("python@3.9:3", when="@1.8.0", type=("build", "run"))
    depends_on("py-poetry-core@1.0.0:", when="@1.8.0", type="build")
    depends_on("py-poetry-plugin-tweak-dependencies-version", when="@1.8.0", type="build")
    depends_on("py-poetry-dynamic-versioning", when="@1.8.0", type="build")
    depends_on("py-sphinx@7.2.5", when="@1.8.0", type=("build", "run"))
    depends_on("py-sphinx", when="@1.1.0", type=("build", "run"))
    depends_on("py-pygments@2.16.1", when="@1.8.0", type=("build", "run"))
    depends_on("py-pygments", when="@1.1.0", type=("build", "run"))
    depends_on("py-docutils@0.20.1", when="@1.8.0", type=("build", "run"))

    def url_for_version(self, version):
        if version >= Version("1.6"):
            url = "https://files.pythonhosted.org/packages/source/s/sphinx_prompt/sphinx_prompt-{0}.tar.gz"
        else:
            url = "https://files.pythonhosted.org/packages/source/s/sphinx_prompt/sphinx-prompt-{0}.tar.gz"
        return url.format(version)
