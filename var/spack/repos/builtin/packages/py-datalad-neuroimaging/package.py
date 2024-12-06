# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDataladNeuroimaging(PythonPackage):
    """DataLad extension package for neuro/medical imaging"""

    homepage = "https://github.com/datalad/datalad-neuroimaging"
    pypi = "datalad_neuroimaging/datalad_neuroimaging-0.3.1.tar.gz"

    license("MIT")

    version("0.3.3", sha256="49a6852e68892e6cd13f245bca2d400abded5ea4fd2a69c9be41c710d0c49bb1")
    version("0.3.1", sha256="aaf7a3d10e8e7df1d8dee09e485bbe26787f496fb2302ed7ddea55a470a0f96e")

    depends_on("py-setuptools@43:", when="@0.3.2:", type="build")
    depends_on("py-setuptools", type="build")

    depends_on("py-datalad@0.16.7:", when="@0.3.2:", type=("build", "run"))
    depends_on("py-datalad@0.12:", type=("build", "run"))
    depends_on("py-datalad-deprecated@0.2.7:", when="@0.3.3:", type=("build", "run"))
    depends_on("py-pydicom", type=("build", "run"))
    depends_on("py-pybids@0.15.1:", when="@0.3.2:", type=("build", "run"))
    depends_on("py-pybids@0.9.2:", type=("build", "run"))
    depends_on("py-nibabel", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-datalad-metalad@0.4.5:", when="@0.3.2:", type=("build", "run"))
    depends_on("git-annex", type="run")
