# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libmonitor(AutotoolsPackage):
    """Libmonitor is a library providing callback functions for the
    begin and end of processes and threads.  It provides a layer on
    which to build process monitoring tools and profilers."""

    homepage = "https://github.com/HPCToolkit/libmonitor"
    git = "https://github.com/HPCToolkit/libmonitor.git"
    maintainers("mwkrentel")

    license("BSD-3-Clause")

    version("master", branch="master")
    version("2023.03.15", commit="48520940b915352748950ea718fadc82f87f659d")
    version("2023.02.13", commit="6db182b25202552f75a087116ab57193652d150f")
    version("2022.09.02", commit="4ae16dab0ba5fbda0ffe28df523613ea22cb85ae")
    version("2021.11.08", commit="22aa52c621534f12d401fa37f6963bfca7441e20")
    version("2021.04.27", commit="a2d1b6be23410ef1ad2c9d0006672453803243c2")
    version("2020.10.15", commit="36e5cb7ebeadfff01476b79ff04f6ec772ba831d")
    version("2019.05.31", commit="c9767087d52e58a719aa7f149136b101e499db44")
    version("2018.07.18", commit="d28cc1d3c08c02013a68a022a57a6ac73db88166")
    version("2013.02.18", commit="4f2311e413fd90583263d6f20453bbe552ccfef3")

    depends_on("c", type="build")  # generated

    # Configure for Rice HPCToolkit.
    variant("hpctoolkit", default=False, description="Configure for HPCToolkit")

    # Configure for OpenSpeedshop and Survey.
    # Configure for adding MPI Post Comm Rank support
    variant("commrank", default=False, description="Build with MPI Post Comm Rank support patch.")

    variant("dlopen", default=True, description="Override dlopen and dlclose")

    patch("libmonitorkrell-0001.patch", when="@2013.02.18+commrank")
    patch("libmonitorkrell-0002.patch", when="@2013.02.18+commrank")

    patch("add-monitor-comm-rank-notification.patch", when="@2020.10.15+commrank")

    signals = "SIGBUS, SIGSEGV, SIGPROF, 36, 37, 38"

    # Set default cflags (-g -O2) and move to the configure line.
    def flag_handler(self, name, flags):
        if name != "cflags":
            return (flags, None, None)

        if "-g" not in flags:
            flags.append("-g")
        for flag in flags:
            if flag.startswith("-O"):
                break
        else:
            flags.append("-O2")

        return (None, None, flags)

    def configure_args(self):
        args = []

        if self.spec.satisfies("+hpctoolkit"):
            args.append("--enable-client-signals=%s" % self.signals)

        if self.spec.satisfies("+dlopen"):
            args.append("--enable-dlfcn")
        else:
            args.append("--disable-dlfcn")

        return args
