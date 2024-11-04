# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


def is_string(x):
    """validate a string"""
    try:
        return isinstance(x, str)
    except ValueError:
        return False


class Dataspaces(AutotoolsPackage):
    """an extreme scale data management framework."""

    homepage = "http://www.dataspaces.org"
    url = "https://dataspaces.rdi2.rutgers.edu/downloads/dataspaces-1.6.2.tar.gz"

    license("BSD-3-Clause")

    version("1.8.0", sha256="7f204bb3c03c2990f5a2d76a29185466b584793c63ada03e5e694627e6060605")
    version("1.6.2", sha256="3c43d551c1e8198a4ab269c83928e1dc6f8054e6d41ceaee45155d91a48cf9bf")

    variant("dimes", default=False, description="enabled DIMES transport mode")
    variant("cray-drc", default=False, description="using Cray Dynamic Credentials library")
    variant(
        "gni-cookie",
        default="0x5420000",
        description="Cray UGNI communication token",
        values=is_string,
    )
    variant("ptag", default="250", description="Cray UGNI protection tag", values=is_string)
    variant("mpi", default=True, description="Use MPI for collective communication")

    depends_on("m4", type="build")
    depends_on("automake", type="build")
    depends_on("autoconf", type="build")
    depends_on("libtool", type="build")
    depends_on("mpi", when="+mpi")

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autogen.sh")

    def setup_build_environment(self, env):
        if self.spec.satisfies("+mpi"):
            env.set("CC", self.spec["mpi"].mpicc)
            env.set("FC", self.spec["mpi"].mpifc)

        env.set("CFLAGS", self.compiler.cc_pic_flag)

        if self.spec.satisfies("%gcc@10:"):
            env.set("FCFLAGS", "-fallow-argument-mismatch")

    def configure_args(self):
        args = []
        cookie = self.spec.variants["gni-cookie"].value
        ptag = self.spec.variants["ptag"].value
        if self.spec.satisfies("+dimes"):
            args.append("--enable-dimes")
        if self.spec.satisfies("+cray-drc"):
            args.append("--enable-drc")
        else:
            args.append("--with-gni-cookie=%s" % cookie)
            args.append("--with-gni-ptag=%s" % ptag)
        return args
