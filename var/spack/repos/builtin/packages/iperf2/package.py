# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Iperf2(AutotoolsPackage, SourceforgePackage):
    """This code is a continuation based from the no longer maintained iperf
    2.0.5 code base. Iperf 2.0.5 is still widely deployed and used by many for
    testing networks and for qualifying networking products."""

    homepage = "https://sourceforge.net/projects/iperf2/"
    sourceforge_mirror_path = "iperf2/iperf-2.0.12.tar.gz"

    version("2.1.9", sha256="5c0771aab00ef14520013aef01675977816e23bb8f5d9fde016f90eb2f1be788")
    version("2.1.8", sha256="8e2cf2fbc9d0d4d1cf9d109b1e328459f9622993dc9a4c5a7dc8a2088fb7beaf")
    version("2.1.7", sha256="1aba2e1d7aa43641ef841951ed88e16cffba898460e0c51e6b2806f3ff20e9d4")
    version("2.0.12", sha256="367f651fb1264b13f6518e41b8a7e08ce3e41b2a1c80e99ff0347561eed32646")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
