# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Iperf2(AutotoolsPackage, SourceforgePackage):
    """This code is a continuation based from the no longer maintained iperf
    2.0.5 code base. Iperf 2.0.5 is still widely deployed and used by many for
    testing networks and for qualifying networking products."""

    homepage = "https://sourceforge.net/projects/iperf2"
    sourceforge_mirror_path = "iperf2/iperf-2.0.12.tar.gz"

    version('2.0.12', sha256='367f651fb1264b13f6518e41b8a7e08ce3e41b2a1c80e99ff0347561eed32646')
