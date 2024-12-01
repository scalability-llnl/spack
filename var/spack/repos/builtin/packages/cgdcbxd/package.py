# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cgdcbxd(AutotoolsPackage):
    """cgdcbxd is a daemon used to monitor DCB netlink events and manage
    the net_prio control group subsystem. The daemon keeps the hierarchy
    and priority mappings in sync with DCBX Application events"""

    homepage = "https://github.com/jrfastab/cgdcbxd"
    url = "https://github.com/jrfastab/cgdcbxd/archive/v1.0.2.tar.gz"

    license("GPL-2.0-only")

    version("1.0.2", sha256="ef626c60e27005d3cae1e19a60d0133be0d1f0a012b695f7f1f6ad5a2afa4166")
    version("1.0.1", sha256="663b87a5ab4a760e2446e479fec36f6300d53e6113af1408efc156325219900c")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("libcgroup@0.32:")
    depends_on("libmnl")

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./bootstrap.sh")

    @property
    def install_targets(self):
        # Without DESTDIR=self.prefix, an attempt would be made to install
        # configuration files to /etc, which would faild the build and even
        # when privileges for this exist, spack could not remove it on uninstall:
        return ["install", "DESTDIR={0}".format(self.prefix)]
