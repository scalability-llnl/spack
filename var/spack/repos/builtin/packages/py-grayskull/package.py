# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGrayskull(PythonPackage):
    """Project to generate recipes for conda packages."""

    homepage = "https://github.com/conda/grayskull"
    pypi = "grayskull/grayskull-2.5.0.tar.gz"

    license("Apache-2.0")

    version("2.7.3", sha256="9396245439584b92d656fdefb03d6911b5987f91a5ae714772ddcb338768cbb9")
    version("2.5.0", sha256="b021138655be550fd1b93b8db08b9c66169fac9cba6bcdad1411263e12fc703f")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools@61:", type="build")
    depends_on("py-setuptools-scm@6.2:+toml", type="build")
    depends_on("py-beautifulsoup4", type=("build", "run"))
    depends_on("py-colorama", type=("build", "run"))
    depends_on("py-conda-souschef@2.2.3:", type=("build", "run"))
    depends_on("py-packaging@21.3:", type=("build", "run"))
    depends_on("py-pip", type=("build", "run"))
    depends_on("py-pkginfo", type=("build", "run"))
    depends_on("py-progressbar2@3.53:", type=("build", "run"))
    depends_on("py-rapidfuzz@3:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-ruamel-yaml@0.16.10:", type=("build", "run"))
    depends_on("py-ruamel-yaml-jinja2", type=("build", "run"))
    depends_on("py-setuptools@30.3:", type=("build", "run"))
    depends_on("py-semver@3.0", type=("build", "run"))
    depends_on("py-stdlib-list", type=("build", "run"))
    depends_on("py-tomli", type=("build", "run"))
    depends_on("py-tomli-w", type=("build", "run"))
