# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxClick(PythonPackage):
    """Sphinx plugin that allows you to automatically extract documentation
    from a Click-based application and include it in your docs"""

    homepage = "https://sphinx-click.readthedocs.io/en/latest"
    pypi = "sphinx_click/sphinx_click-6.0.0.tar.gz"

    maintainers("TomMelt")

    license("MIT", checked_by="tommelt")

    version("6.0.0", sha256="f5d664321dc0c6622ff019f1e1c84e58ce0cecfddeb510e004cf60c2a3ab465b")

    depends_on("py-setuptools", type="build")

    depends_on("py-click@8:", type=("build", "run"))
    depends_on("py-sphinx@4:", type=("build", "run"))
    depends_on("py-docutils", type=("build", "run"))
    depends_on("py-pbr", type=("build", "run"))
