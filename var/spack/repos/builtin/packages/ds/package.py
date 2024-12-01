# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from os import symlink

from spack.package import *


class Ds(AutotoolsPackage):
    """SAOImage DS9 is an astronomical imaging and data visualization
    application."""

    homepage = "https://ds9.si.edu/"
    url = "http://ds9.si.edu/download/source/ds9.8.0.tar.gz"

    version("9.8.0", sha256="f3bdb46c1653997202f98c6f76632a4eb444707f4b64c14f8b96863d9c890304")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("m4", type="build")
    depends_on("libtool", type="build")

    depends_on("libx11")
    depends_on("libxml2")
    depends_on("libxslt")
    depends_on("openssl")
    depends_on("tcl")
    depends_on("tcl-tclxml")
    depends_on("tk")

    def patch(self):
        # the package provides it's own Tcl utilities
        # compiling and manually setting paths for all of them is contrived
        # (most of the utilities are small and not included in spack)

        # inject libxml, libxslt prefixes into configure search paths
        filter_file(
            "/usr/bin/xml2-config",
            join_path(self.spec["libxml2"].prefix, "bin/xml2-config"),
            "tclxml/configure",
            string=True,
        )

        filter_file(
            "/usr/bin/xslt-config",
            join_path(self.spec["libxslt"].prefix, "bin/xslt-config"),
            "tclxml/configure",
            string=True,
        )

        # symlink the master configure script into the source directory
        symlink("unix/configure", "configure")

    def configure_args(self):
        srcdir = join_path(self.stage.source_path, "unix")
        return ["--srcdir={0}".format(srcdir)]

    def install(self, spec, prefix):
        # no install target provided in Makefile, install manually

        install_tree("bin", prefix.bin)
        install_tree("share", prefix.share)
        install_tree("lib", prefix.lib)
