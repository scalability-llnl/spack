# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tempestremap(AutotoolsPackage):
    """TempestRemap is a conservative, consistent and monotone remapping
    package for arbitrary grid geometry with support for finite volumes
    and finite elements.

    There is still quite a bit of work to be done, but any feedback is
    appreciated on the software in its current form
    """

    homepage = "https://github.com/ClimateGlobalChange/tempestremap"
    url = "https://github.com/ClimateGlobalChange/tempestremap/archive/v2.0.5.tar.gz"

    maintainers("iulian787", "vijaysm", "paullric")

    version("2.1.6", sha256="d2208b5d6952eba5003ee7abcf22f46a254ba03f6b76dcc4d246068573d424e2")
    version("2.0.5", sha256="8618f5cbde450922efa1d77e67b062c557788b0cf4304adca30237afe3ade887")
    version("2.0.4", sha256="8349eeb604e97b13d2ecde8626a69e579a7af70ad0e8a6925a8bb4306a4963a4")
    version("2.0.3", sha256="b4578c2cb101ba091a10dc914e15ac968257f5db27ca78bc9fb5dbd70bce191f")
    version("2.0.2", sha256="2347bf804d19d515cb630a76b87e6dc6edcc1a828ff8c0f2a8a28e77794bad13")
    version("2.0.1", sha256="a3f1bef8cc413a689d429ac56f2bcc2e1d282d99797c3375233de792a7448ece")
    version("2.0.0", sha256="5850e251a4ad04fc924452f49183e5e12c38725832a568e57fa424a844b8a000")

    depends_on("cxx", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    depends_on("netcdf-c")
    depends_on("blas")
    depends_on("lapack")

    def configure_args(self):
        spec = self.spec
        options = []
        options.append("--with-netcdf=%s" % spec["netcdf-c"].prefix)
        options.append("--with-blas=%s" % spec["blas"].libs.ld_flags)
        options.append("--with-lapack=%s" % spec["lapack"].libs.ld_flags)
        return options
