# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCryolobm(PythonPackage):
    """The crYOLO boxmanger was written to produce annotation data for crYOLO
    as deep learning based particle picking procedure for cryo electro microscopy."""

    homepage = "https://pypi.org/project/cryoloBM/#description"
    pypi = "cryoloBM/cryoloBM-1.3.7.tar.gz"

    license("MIT")

    version("1.3.7", sha256="e3505c95cddac3a344d1c6eddf1a9ff576a1384f9194b580287c76367912bedc")

    depends_on("python@3.4.0:")
    depends_on("py-setuptools", type="build")
    depends_on("py-matplotlib@2.2.3:", type=("build", "run"))
    depends_on("py-numpy@1.14.5:", type=("build", "run"))
