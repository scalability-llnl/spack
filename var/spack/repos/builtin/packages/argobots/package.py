# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Argobots(AutotoolsPackage):
    """Argobots, which was developed as a part of the Argo project, is
    a lightweight runtime system that supports integrated computation
    and data movement with massive concurrency. It will directly
    leverage the lowest-level constructs in the hardware and OS:
    lightweight notification mechanisms, data movement engines, memory
    mapping, and data placement strategies. It consists of an
    execution model and a memory model."""

    homepage = "http://www.argobots.org/"
    url      = "https://github.com/pmodels/argobots/releases/download/v1.0b1/argobots-1.0b1.tar.gz"
    git      = "https://github.com/pmodels/argobots.git"
    maintainers = ['shintaro-iwasaki']

    version("main", branch="main")
    version("1.1", sha256="f0f971196fc8354881681c2282a2f2adb6d48ff5e84cf820ca657daad1549005")
    version("1.0.1", sha256="fa05a02d7f8f74d845647636609219ee02f6adf628ebcbf40393f829987d9036")
    version("1.0", sha256="36a0815f7bf99900a9c9c1eef61ef9b3b76aa2cfc4594a304f6c8c3296da8def")

    variant("perf", default=True, description="Add performance optimization flags")
    variant("valgrind", default=False, description="Enable Valgrind")
    variant("debug", default=False, description="Compiled with debugging symbols")
    variant("stackunwind", default=False, description="Enable function stack unwinding")
    variant("stackguard", default="none", description="Enable stack guard",
            values=('none', 'canary-32', 'mprotect', 'mprotect-strict'), multi=False)
    variant("tool", default=False, description="Enable ABT_tool interface")
    variant("affinity", default=False, description="Enable affinity setting")

    depends_on("m4", type=("build"), when="@main")
    depends_on("autoconf", type=("build"), when="@main")
    depends_on("automake", type=("build"), when="@main")
    depends_on("libtool", type=("build"), when="@main")
    depends_on("valgrind", when="+valgrind")
    depends_on("libunwind", when="+stackunwind")

    def configure_args(self):
        args = []
        if '+perf' in self.spec:
            args.append('--enable-perf-opt')

        if '+valgrind' in self.spec:
            args.append('--enable-valgrind')
        else:
            args.append('--disable-valgrind')

        if '+debug' in self.spec:
            args.append('--enable-debug=yes')
        else:
            args.append('--disable-debug')

        if '+stackunwind' in self.spec:
            args.append('--enable-stack-unwind')
            args.append('--with-libunwind={0}'.format(self.spec['libunwind'].prefix))

        stackguard = self.spec.variants['stackguard'].value
        if stackguard != 'none':
            args.append('--enable-stack-overflow-check={0}'.format(stackguard))

        if '+tool' in self.spec:
            args.append('--enable-tool')

        if '+affinity' in self.spec:
            args.append('--enable-affinity')

        return args
