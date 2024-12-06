# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from os.path import join

from spack.package import *


class Tcptrace(AutotoolsPackage):
    """tcptrace is a tool written by Shawn Ostermann at Ohio University for
    analysis of TCP dump files. It can take as input the files produced by
    several popular packet-capture programs, including tcpdump, snoop,
    etherpeek, HP Net Metrix, and WinDump."""

    homepage = "http://www.tcptrace.org/"
    url = "http://www.tcptrace.org/download/tcptrace-6.6.7.tar.gz"

    license("GPL-2.0-only")

    version("6.6.7", sha256="63380a4051933ca08979476a9dfc6f959308bc9f60d45255202e388eb56910bd")

    depends_on("bison", type="build")
    depends_on("flex", type="build")
    depends_on("libpcap")

    # Fixes incorrect API access in libpcap.
    # See https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=545595
    patch("tcpdump.patch")

    @run_after("configure")
    def patch_makefile(self):
        # see https://github.com/blitz/tcptrace/blob/master/README.linux
        makefile = FileFilter("Makefile")
        makefile.filter("PCAP_LDLIBS = -lpcap", "DEFINES += -D_BSD_SOURCE\nPCAP_LDLIBS = -lpcap")

    def install(self, spec, prefix):
        # The build system has trouble creating directories
        mkdirp(prefix.bin)
        install("tcptrace", join(prefix.bin, "tcptrace"))
