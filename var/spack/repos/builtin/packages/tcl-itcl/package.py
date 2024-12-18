# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class TclItcl(AutotoolsPackage):
    """[incr Tcl] is the most widely used O-O system for Tcl. The name is a
    play on C++, and [incr Tcl] provides a similar object model, including
    multiple inheritence and public and private classes and variables."""

    homepage = "https://sourceforge.net/projects/incrtcl/"
    url = "https://sourceforge.net/projects/incrtcl/files/%5Bincr%20Tcl_Tk%5D-4-source/itcl%204.0.4/itcl4.0.4.tar.gz"

    version("4.0.4", sha256="63860438ca22f70049aecff70dc607b31bb1bea0edcc736e36ac6e36c24aecde")

    depends_on("c", type="build")  # generated

    extends("tcl")

    def configure_args(self):
        args = [
            "--enable-shared",
            "--enable-threads",
            "--with-tcl=" + self.spec["tcl"].libs.directories[0],
        ]
        return args
