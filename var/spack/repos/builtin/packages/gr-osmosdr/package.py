# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class GrOsmosdr(CMakePackage):
    """While primarily being developed for the OsmoSDR hardware, this
    block as well supports:

    FunCube Dongle through libgnuradio-fcd,
    FUNcube Dongle Pro+ through gr-fcdproplus,
    sysmocom OsmoSDR Devices through libosmosdr,
    Nuand LLC bladeRF through libbladeRF library,
    Great Scott Gadgets HackRF through libhackrf,
    Ettus USRP Devices through Ettus UHD library,
    Fairwaves UmTRX through Fairwaves' fork of Ettus' UHD library,
    RFSPACE SDR-IQ, SDR-IP, NetSDR (incl. X2 option),
    RTL2832U based DVB-T dongles through librtlsdr,
    RTL-TCP spectrum server (see librtlsdr project),
    MSi2500 based DVB-T dongles through libmirisdr,
    SDRplay RSP through SDRplay API library,
    AirSpy R820t dongles through libairspy,
    gnuradio .cfile input through libgnuradio-blocks"""

    homepage = "https://osmocom.org/projects/gr-osmosdr/wiki/GrOsmoSDR"
    url = "https://github.com/osmocom/gr-osmosdr/archive/v0.2.2.tar.gz"

    maintainers("aweits")

    variant("hackrf", default=True, description="Support HackRF Hardware")

    license("GPL-3.0-only")

    version("0.2.2", sha256="5a7ce7afee38a56191b5d16cb4a91c92476729ff16ed09cbba5a3851ac619713")

    depends_on("cxx", type="build")  # generated

    depends_on("gnuradio")
    depends_on("swig", type="build")
    depends_on("hackrf-host", when="+hackrf")
