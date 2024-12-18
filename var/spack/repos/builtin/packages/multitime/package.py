# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Multitime(AutotoolsPackage):
    """multitime is, in essence, a simple extension to time which runs a
    command multiple times and prints the timing means, standard deviations,
    mins, medians, and maxes having done so. This can give a much better
    understanding of the command's performance."""

    homepage = "https://tratt.net/laurie/src/multitime/"
    url = "https://tratt.net/laurie/src/multitime/releases/multitime-1.4.tar.gz"

    license("MIT")

    version("1.4", sha256="dd85c431c022d0b992f3a8816a1a3dfb414454a229c0ec22514761bf72d3ce47")

    depends_on("c", type="build")  # generated
