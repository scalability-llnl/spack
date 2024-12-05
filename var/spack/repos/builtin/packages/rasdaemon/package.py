# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rasdaemon(AutotoolsPackage):
    """Rasdaemon is a RAS (Reliability, Availability and Serviceability)
    logging tool. It records memory errors, using the EDAC tracing events.
    EDAC is a Linux kernel subsystem with handles detection of ECC errors
    from memory controllers for most chipsets on i386 and x86_64
    architectures. EDAC drivers for other architectures like arm also
    exists."""

    homepage = "https://github.com/mchehab/rasdaemon"
    url = "https://github.com/mchehab/rasdaemon/archive/v0.6.6.tar.gz"

    license("GPL-2.0-or-later")

    version("0.6.6", sha256="eea5fefc68583cca2e6daec58508a554553056aeec5eeee0989417c89607eaba")
    version("0.6.5", sha256="1d85580778a0b7c0587b42e24dfe6c02f4c07c6ca9bbb80737d50b58ac830c92")
    version("0.6.4", sha256="c70e2dae1e15af496873b9e5a4d89847759fffd6cbf5ed1d74d28cd250c0771b")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.sbin)
