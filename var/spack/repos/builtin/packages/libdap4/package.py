# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libdap4(AutotoolsPackage):
    """
    libdap4 is is a c++ library to serve as a client for the OPeNDAP framework
    that simplifies all aspects of scientific data networking and provides
    software which makes local data accessible to remote locations regardless
    of local storage format.
    """

    homepage = "https://www.opendap.org/"
    url = "https://github.com/OPENDAP/libdap4/archive/version-3.20.4.tar.gz"

    maintainers("tjhei")

    license("LGPL-2.1-or-later")

    version("3.20.6", sha256="e44e83043c158d8c9d0a37a1821626ab0db4a1a6578b02182440170c0b060e6d")
    version("3.20.4", sha256="c39fa310985cc8963029ad0d0aba784e7dbf1f70c566bd7ae58242f1bb06d24a")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("bison", type="build")

    depends_on("flex")
    depends_on("curl")
    depends_on("libxml2")
    depends_on("uuid")
    depends_on("rpc")

    def setup_build_environment(self, env):
        # Configure script will search for RPC library, but not actually add RPC library references
        # during configure tests. This can cause a failure with libtirpc if the following variable
        # is not set.
        if self.spec.satisfies("^libtirpc"):
            env.set("TIRPC_LIBS", self.spec["rpc"].libs.link_flags)

    def configure_args(self):
        # libxml2 exports ./include/libxml2/ instead of ./include/, which we
        # need, so grab this path manually:
        libxml2_include = self.spec["libxml2"].prefix.include
        args = ["CPPFLAGS=-I{0}".format(libxml2_include)]
        return args
