# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Heppdt(AutotoolsPackage):
    """The HepPID library contains translation methods for particle ID's
    to and from various Monte Carlo generators and the PDG standard
    numbering scheme. We realize that the generators adhere closely
    to the standard, but there are occasional differences."""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/heppdt/wiki"
    url = "https://lcgpackages.web.cern.ch/lcgpackages/tarFiles/sources/HepPDT-2.06.01.tar.gz"

    tags = ["hep"]

    version("3.04.01", sha256="2c1c39eb91295d3ded69e0d3f1a38b1cb55bc3f0cde37b725ffd5d722f63c0f6")
    version("3.04.00", sha256="c5f0eefa19dbbae99f2b6a2ab1ad8fd5d5f844fbbbf96e62f0ddb68cc6a7d5f3")
    version("3.03.02", sha256="409d940badbec672c139cb8972c88847b3f9a2476a336f4f7ee6924f8d08426c")
    version("3.03.01", sha256="1aabb0add1a26dcb010f99bfb24e666a881cb03f796503220c93d3d4434b4e32")
    version("3.03.00", sha256="c9fab0f7983234137d67e83d3e94e194856fc5f8994f11c6283194ce60010840")
    version(
        "2.06.01",
        sha256="12a1b6ffdd626603fa3b4d70f44f6e95a36f8f3b6d4fd614bac14880467a2c2e",
        preferred=True,
    )

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated
