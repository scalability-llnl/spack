# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxcontribPlantuml(PythonPackage):
    """PlantUML for Sphinx."""

    homepage = "https://github.com/sphinx-contrib/plantuml/"
    pypi = "sphinxcontrib-plantuml/sphinxcontrib-plantuml-0.30.tar.gz"

    maintainers("greenc-FNAL", "knoepfel", "marcpaterno")

    license("BSD-2-Clause", checked_by="greenc-FNAL")

    version("0.30", sha256="2a1266ca43bddf44640ae44107003df4490de2b3c3154a0d627cfb63e9a169bf")

    depends_on("py-setuptools", type="build")

    depends_on("plantuml", type=("build", "run"))
    depends_on("py-sphinx@1.6:", type=("build", "run"))
