# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class TclTcllib(AutotoolsPackage):
    """Tcllib is a collection of utility modules for Tcl. These modules provide
    a wide variety of functionality, from implementations of standard data
    structures to implementations of common networking protocols. The intent is
    to collect commonly used function into a single library, which users can
    rely on to be available and stable."""

    homepage = "http://www.tcl.tk/software/tcllib"
    url = "https://sourceforge.net/projects/tcllib/files/tcllib/1.19/tcllib-1.19.tar.gz"
    list_url = "https://sourceforge.net/projects/tcllib/files/tcllib/"
    list_depth = 1

    license("TCL")

    version("1.19", sha256="01fe87cf1855b96866cf5394b6a786fd40b314022714b34110aeb6af545f6a9c")
    version("1.18", sha256="72667ecbbd41af740157ee346db77734d1245b41dffc13ac80ca678dd3ccb515")
    version("1.17", sha256="00c16aa28512ff6a67f199ffa5e04acaeb7b8464b2b7dc70ad8d00ce4c8d25ce")
    version("1.16", sha256="0b3a87577bf1ea79c70479be5230f0ba466587b4621828ec4941c4840fa1b2e8")
    version("1.15", sha256="6d308980d9dace24c6252b96223c1646e83795ba03dbf996525ad27e1b56bffd")
    version("1.14", sha256="dd149fcb37ceb04da83531276a9d7563827807dcee49f9b9f63bedea9e130584")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    extends("tcl")
