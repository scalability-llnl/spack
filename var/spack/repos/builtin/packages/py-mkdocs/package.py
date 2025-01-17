# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMkdocs(PythonPackage):
    """MkDocs is a fast, simple and downright gorgeous static site generator
    that's geared towards building project documentation."""

    homepage = "https://www.mkdocs.org/"
    pypi = "mkdocs/mkdocs-1.3.1.tar.gz"

    license("BSD-2-Clause")

    version("1.5.3", sha256="eb7c99214dcb945313ba30426c2451b735992c73c2e10838f76d09e39ff4d0e2")
    version("1.3.1", sha256="a41a2ff25ce3bbacc953f9844ba07d106233cd76c88bac1f59cb1564ac0d87ed")

    depends_on("py-hatchling", when="@1.4.1:", type="build")
    depends_on("py-click@7.0:", when="@1.4.1:", type=("build", "run"))
    depends_on("py-click@3.3:", type=("build", "run"))
    depends_on("py-jinja2@2.11.1:", when="@1.4.1:", type=("build", "run"))
    depends_on("py-jinja2@2.10.2:", type=("build", "run"))
    depends_on("py-markupsafe@2.0.1:", when="@1.5.0:", type=("build", "run"))
    depends_on("py-markdown@3.2.1:", when="@1.5.0:", type=("build", "run"))
    depends_on("py-markdown@3.2.1:3.3", when="@:1.4", type=("build", "run"))
    depends_on("py-pyyaml@5.1:", when="@1.4.1:", type=("build", "run"))
    depends_on("py-pyyaml@3.10:", type=("build", "run"))
    depends_on("py-watchdog@2.0:", type=("build", "run"))
    depends_on("py-ghp-import@1.0:", type=("build", "run"))
    depends_on("py-pyyaml-env-tag@0.1:", type=("build", "run"))
    depends_on("py-importlib-metadata@4.3:", when="@1.4.1: ^python@:3.9", type=("build", "run"))
    depends_on("py-importlib-metadata@4.3:", type=("build", "run"), when="@:1.4.0")
    depends_on("py-typing-extensions@3.10:", when="@1.4.1: ^python@:3.7", type=("build", "run"))
    depends_on("py-packaging@20.5:", type=("build", "run"))
    depends_on("py-mergedeep@1.3.4:", type=("build", "run"))
    depends_on("py-pathspec@0.11.1:", when="@1.5.0:", type=("build", "run"))
    depends_on("py-platformdirs@2.2.0:", when="@1.5.0:", type=("build", "run"))
    depends_on("py-colorama@0.4:", when="@1.4.1: platform=windows", type=("build", "run"))
    # Babel is listed as an optional dependency, but the spack install fails without it.
    depends_on("py-babel@2.9.0:", when="@1.4.1:", type=("build", "run"))
