# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJunit2html(PythonPackage):
    """
    Simple self-contained python tool to produce a single html file from a single junit xml file.
    """

    homepage = "https://gitlab.com/inorton/junit2html"

    url = "https://gitlab.com/inorton/junit2html/-/archive/v31.0.2/junit2html-v31.0.2.tar.gz"

    maintainers("LydDeb")

    version("31.0.2", sha256="8d90ae83163dde6bf0bde9c3e8d21c0ab0796de7c5f33917cfdbb9d319212213")

    depends_on("py-setuptools", type=("build"))
    depends_on("py-jinja2@3.0:", type=("build", "run"))
