# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Systemtap(AutotoolsPackage):
    """SystemTap provides free software (GPL) infrastructure to
    simplify the gathering of information about the running
    Linux system. This assists diagnosis of a performance or
    functional problem. SystemTap eliminates the need for the
    developer to go through the tedious and disruptive instrument,
    recompile, install, and reboot sequence that may be otherwise
    required to collect data."""

    homepage = "https://sourceware.org/systemtap/"
    url = "https://sourceware.org/systemtap/ftp/releases/systemtap-4.3.tar.gz"

    license("GPL-2.0-only")

    version("4.3", sha256="f8e206ed654c13a8b42245a342c1b5a4aafdf817c97bf3becbe3c8a43a4489ce")
    version("4.2", sha256="0984ebe3162274988252ec35074021dc1e8420d87a8b35f437578562fce08781")
    version("4.1", sha256="8efa1ee2b34f1c6b2f33a25313287d59c8ed1b00265e900aea874da8baca1e1d")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("gettext")
    depends_on("elfutils@0.151:")
    depends_on("sqlite")
    depends_on("py-setuptools", type="build")
    depends_on("python", type=("build", "run"))

    def flag_handler(self, name, flags):
        if name == "ldlibs" and "intl" in self.spec["gettext"].libs.names:
            flags.append("-lintl")
        return self.build_system_flags(name, flags)
