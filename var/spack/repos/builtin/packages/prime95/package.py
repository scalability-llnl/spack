# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Prime95(Package):
    """
    Prime95, also distributed as the command-line utility mprime for FreeBSD
    and Linux, is a freeware application.

    Prime95 is a CPU stress testing program. It tests your computer for
    stability issues by stressing your CPU to its maximum limit.
    Prime95 runs indefinitely and only terminates a stress test when it
    encounters an error and informs the user that the system may be unstable.
    """

    homepage = "https://www.mersenne.org/"
    url = "https://www.mersenne.org/ftp_root/gimps/p95v308b17.linux64.tar.gz"
    maintainers("saqibkh")

    license("Unlicense")

    version("95v308b17", sha256="5180c3843d2b5a7c7de4aa5393c13171b0e0709e377c01ca44154608f498bec7")
    version("95v308b16", sha256="9fa9b30dd175be287d3a3f4b85139d02d4e64aa2dad88324abd4fdfcbbfe10d4")
    version("95v309b3", sha256="afa5d1a72e98c94d58e0ac002d3e70ffb3887d975d9b83157d1ea41755efd32b")
    version("95v309b2", sha256="49f1d79c04c24260ab10ec080588c54d4c716f2c1088ad66a781a1784c4c3d59")
    version("95v309b1", sha256="0dbfa6e4dd04f8f2251669904c8c4029d42e2121c06c83b39bb13f0a40439bcb")

    depends_on("autoconf")
    depends_on("automake")
    depends_on("libtool")

    def install(self, spec, prefix):
        install_tree(".", prefix)
