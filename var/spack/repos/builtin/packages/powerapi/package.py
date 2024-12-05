# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Powerapi(AutotoolsPackage):
    """This software is a reference implementation of the PowerAPI"""

    homepage = "https://powerapi.sandia.gov/"
    git = "https://github.com/pwrapi/pwrapi-ref.git"

    license("BSD-3-Clause")

    version("2020-01-30", commit="21f75b1469261d99e604f7ddc18f30513ebdd048")
    version("1.1.1", commit="93f66dfa29f014067823f2b790a1862e5841a11c")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("hwloc", default=False, description="Build hwloc support")
    variant("debug", default=False, description="Enable debug support")
    variant("mpi", default=False, description="Enable MPI support")
    variant("gnu-ld", default=False, description="Assume GNU compiled uses gnu-ld")

    depends_on("autoconf")
    depends_on("automake")
    depends_on("libtool")
    depends_on("m4")

    depends_on("hwloc", when="+hwloc")
    depends_on("mpi", when="+mpi")

    # C++11 requires a space between literal and identifier.
    patch("add_space.patch")

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autogen.sh")

    def configure_args(self):
        spec = self.spec
        args = ["--prefix={0}".format(self.prefix)]

        if "+hwloc" in spec:
            args.append("--with-hwloc={0}".format(spec["hwloc"].prefix))

        if "+mpi" in spec:
            args.append("--with-mpi={0}".format(spec["mpi"].prefix))

        args.extend(
            [
                "--with%s-gnu-ld" % ("" if "+gnu-ld" in spec else "out"),
                "--%sable-debug" % ("en" if "+debug" in spec else "dis"),
            ]
        )

        return args

    def install(self, spec, prefix):
        make("install")
