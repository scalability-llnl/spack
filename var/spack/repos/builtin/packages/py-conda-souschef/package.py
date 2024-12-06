# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCondaSouschef(PythonPackage):
    """Project to handle conda recipes."""

    homepage = "https://github.com/marcelotrevisani/souschef"
    pypi = "conda-souschef/conda-souschef-2.2.3.tar.gz"

    license("Apache-2.0")

    version("2.2.3", sha256="9bf3dba0676bc97616636b80ad4a75cd90582252d11c86ed9d3456afb939c0c3")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools@30.3:", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-ruamel-yaml@0.15.3:", type=("build", "run"))
    depends_on("py-ruamel-yaml-jinja2", type=("build", "run"))
