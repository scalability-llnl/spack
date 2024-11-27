# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMkdocs(PythonPackage):
    """MkDocs is a fast, simple and downright gorgeous static site generator
    that's geared towards building project documentation."""

    homepage = "https://www.mkdocs.org/"
    pypi = "mkdocs/mkdocs-1.3.1.tar.gz"

    license("BSD-2-Clause")

    version("1.3.1", sha256="a41a2ff25ce3bbacc953f9844ba07d106233cd76c88bac1f59cb1564ac0d87ed")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-click@3.3:", type=("build", "run"))
    depends_on("py-jinja2@2.10.2:", type=("build", "run"))
    depends_on("py-markdown@3.2.1:3.3", type=("build", "run"))
    depends_on("py-pyyaml@3.10:", type=("build", "run"))
    depends_on("py-watchdog@2.0:", type=("build", "run"))
    depends_on("py-ghp-import@1.0:", type=("build", "run"))
    depends_on("py-pyyaml-env-tag@0.1:", type=("build", "run"))
    depends_on("py-importlib-metadata@4.3:", type=("build", "run"))
    depends_on("py-packaging@20.5:", type=("build", "run"))
    depends_on("py-mergedeep@1.3.4:", type=("build", "run"))
