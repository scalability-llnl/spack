# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyRocrate(PythonPackage):
    """RO-Crate metadata generator/parser"""

    homepage = "https://github.com/ResearchObject/ro-crate-py/"
    pypi = "rocrate/rocrate-0.7.0.tar.gz"

    license("Apache-2.0")

    version("0.7.0", sha256="f7537132f45b724bfa6a212b2ed3daa0aaee1d602a773f0f049b8ca9a14958e1")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-requests", type=("build", "run"))
    depends_on("py-arcp@0.2.1", type=("build", "run"))
    depends_on("py-galaxy2cwl", type=("build", "run"))
    depends_on("py-jinja2", type=("build", "run"))
    depends_on("py-python-dateutil", type=("build", "run"))
    depends_on("py-click", type=("build", "run"))
