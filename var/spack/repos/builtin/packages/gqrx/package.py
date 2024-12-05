# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Gqrx(CMakePackage):
    """Gqrx is an open source software defined radio (SDR) receiver
    implemented using GNU Radio and the Qt GUI toolkit. Currently it
    works on Linux and Mac with hardware supported by gr-osmosdr,
    including Funcube Dongle, RTL-SDR, Airspy, HackRF, BladeRF,
    RFSpace, USRP and SoapySDR.

    Gqrx can operate as an AM/FM/SSB receiver with audio output or as
    an FFT-only instrument. There are also various hooks for
    interacting with external application using nertwork sockets."""

    homepage = "https://gqrx.dk/"
    url = "https://github.com/csete/gqrx/archive/v2.13.1.tar.gz"

    maintainers("aweits")

    license("GPL-3.0-or-later")

    version("2.13.1", sha256="08b7b930bed00c6ac79330695c24919a9d779112e1a3dd37d22cc9ee38561e82")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("cmake@3.2.0:", type="build")
    depends_on("gnuradio")
    depends_on("pkgconfig", type="build")
    depends_on("gr-osmosdr")
    depends_on("qt")
    depends_on("pulseaudio")
