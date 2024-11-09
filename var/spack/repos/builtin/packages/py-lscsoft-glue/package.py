# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLscsoftGlue(PythonPackage):
    """Glue (Grid LSC User Environment) is a suite of python modules and
    programs to allow users to run LSC codes on the grid. It also provides
    certain metadata services, such as the LSC segment database."""

    homepage = "https://www.lsc-group.phys.uwm.edu/daswg/projects/glue.html"
    pypi = "lscsoft-glue/lscsoft-glue-2.0.0.tar.gz"

    license("GPL-3.0-only")

    version("2.0.0", sha256="9bdfaebe4c921d83d1e3d1ca24379a644665e9d7530e7070665f387767c66923")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-six", type=("build", "run"))
    depends_on("py-pyopenssl", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-ligo-segments", type=("build", "run"))
