# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RIrdisplay(RPackage):
    """'Jupyter' Display Machinery.

    An interface to the rich display capabilities of 'Jupyter' front-ends (e.g.
    'Jupyter Notebook') <https://jupyter.org>. Designed to be used from a
    running 'IRkernel' session <https://irkernel.github.io>."""

    cran = "IRdisplay"

    version("1.1", sha256="83eb030ff91f546cb647899f8aa3f5dc9fe163a89a981696447ea49cc98e8d2b")
    version("0.7.0", sha256="91eac9acdb92ed0fdc58e5da284aa4bb957ada5eef504fd89bec136747999089")
    version("0.4.4", sha256="e83a0bc52800618bf9a3ac5ef3d432512e00f392b7216fd515fca319377584a6")

    depends_on("r@3.0.1:", type=("build", "run"))
    depends_on("r-repr", type=("build", "run"))
