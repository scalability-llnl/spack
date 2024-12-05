# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDataladHirni(PythonPackage):
    """DataLad extension for raw data capturing and conversion workflows"""

    homepage = "https://github.com/psychoinformatics-de/datalad-hirni"
    pypi = "datalad_hirni/datalad_hirni-0.0.8.tar.gz"

    version("0.0.8", sha256="4a43fd8b895763fe930a7f98dabcf5c152a0680b6fdadccc1defce460d135dc7")

    depends_on("py-setuptools", type="build")
    depends_on("py-datalad+full@0.14.0:", type=("build", "run"))
    depends_on("py-datalad-metalad@0.2.0:", type=("build", "run"))
    depends_on("py-datalad-neuroimaging@0.3.1:", type=("build", "run"))
    depends_on("py-datalad-container@1.1.2:", type=("build", "run"))
    depends_on("py-datalad-webapp@0.3:", type=("build", "run"))
    depends_on("git-annex", type="run")
