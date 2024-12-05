# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Librtlsdr(CMakePackage):
    """turns your Realtek RTL2832 based DVB dongle into a SDR receiver."""

    homepage = "https://osmocom.org/projects/rtl-sdr/wiki"
    url = "https://github.com/steve-m/librtlsdr/archive/0.6.0.tar.gz"

    license("GPL-2.0-or-later")

    version("0.6.0", sha256="80a5155f3505bca8f1b808f8414d7dcd7c459b662a1cde84d3a2629a6e72ae55")
    version("0.5.4", sha256="6fd0d298c1a18fc8005b0c2f6199b08bc15e3fb4f4312f551eea2ae269c940c5")

    depends_on("c", type="build")  # generated

    depends_on("libusb")
