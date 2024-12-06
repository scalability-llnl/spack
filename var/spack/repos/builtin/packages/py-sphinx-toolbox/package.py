# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxToolbox(PythonPackage):
    """Box of handy tools for Sphinx."""

    homepage = "https://github.com/sphinx-toolbox/sphinx-toolbox"
    pypi = "sphinx_toolbox/sphinx_toolbox-3.4.0.tar.gz"

    maintainers("LydDeb")

    version("3.4.0", sha256="e1cf2a3dea5ce80e175a6a9cee8b5b2792240ecf6c28993d87a63b6fcf606293")

    depends_on("py-whey", type="build")

    depends_on("py-apeye@0.4.0:", type=("build", "run"))
    depends_on("py-autodocsumm@0.2.0:", type=("build", "run"))
    depends_on("py-beautifulsoup4@4.9.1:", type=("build", "run"))
    depends_on("py-cachecontrol@0.12.6:+filecache", type=("build", "run"))
    depends_on("py-dict2css@0.2.3:", type=("build", "run"))
    depends_on("py-docutils@0.16:0.18", type=("build", "run"))
    depends_on("py-domdf-python-tools@2.9.0:", type=("build", "run"))
    depends_on("py-html5lib@1.1:", type=("build", "run"))
    depends_on("py-lockfile@0.12.2:", type=("build", "run"))
    depends_on("py-ruamel-yaml@0.16.12:", type=("build", "run"))
    depends_on("py-sphinx@3.2.0:", type=("build", "run"))
    depends_on("py-sphinx-autodoc-typehints@1.11.1:", type=("build", "run"))
    depends_on("py-sphinx-jinja2-compat@0.1.0:", type=("build", "run"))
    depends_on("py-sphinx-prompt@1.1.0:", type=("build", "run"))
    depends_on("py-sphinx-tabs@1.2.1:3.4", type=("build", "run"))
    depends_on("py-tabulate@0.8.7:", type=("build", "run"))
    depends_on("py-typing-extensions@3.7.4.3:3.10.0.0,3.10.0.2:", type=("build", "run"))
    depends_on("py-typing-inspect@0.6.0:", when="^python@:3.7", type=("build", "run"))
