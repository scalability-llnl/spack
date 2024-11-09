# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Argobots(AutotoolsPackage):
    """Argobots, which was developed as a part of the Argo project, is
    a lightweight runtime system that supports integrated computation
    and data movement with massive concurrency. It will directly
    leverage the lowest-level constructs in the hardware and OS:
    lightweight notification mechanisms, data movement engines, memory
    mapping, and data placement strategies. It consists of an
    execution model and a memory model."""

    homepage = "https://www.argobots.org/"
    url = "https://github.com/pmodels/argobots/releases/download/v1.2/argobots-1.2.tar.gz"
    git = "https://github.com/pmodels/argobots.git"
    maintainers("yfguo")

    tags = ["e4s"]

    version("main", branch="main")
    version("1.2", sha256="1c056429d9c0a27c041d4734f6318b801fc2ec671854e42c35251c4c7d0d43e1")
    version("1.1", sha256="f0f971196fc8354881681c2282a2f2adb6d48ff5e84cf820ca657daad1549005")
    version("1.0.1", sha256="fa05a02d7f8f74d845647636609219ee02f6adf628ebcbf40393f829987d9036")
    version("1.0", sha256="36a0815f7bf99900a9c9c1eef61ef9b3b76aa2cfc4594a304f6c8c3296da8def")

    depends_on("c", type="build")  # generated

    variant("perf", default=True, description="Add performance optimization flags")
    variant("valgrind", default=False, description="Enable Valgrind")
    variant("debug", default=False, description="Compiled with debugging symbols")
    variant("stackunwind", default=False, description="Enable function stack unwinding")
    variant(
        "stackguard",
        default="none",
        description="Enable stack guard",
        values=("none", "canary-32", "mprotect", "mprotect-strict"),
        multi=False,
    )
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
        if self.spec.satisfies("+perf"):
            args.append("--enable-perf-opt")

        if self.spec.satisfies("+valgrind"):
            args.append("--enable-valgrind")
        else:
            args.append("--disable-valgrind")

        if self.spec.satisfies("+debug"):
            args.append("--enable-debug=yes")
        else:
            args.append("--disable-debug")

        if self.spec.satisfies("+stackunwind"):
            args.append("--enable-stack-unwind")
            args.append("--with-libunwind={0}".format(self.spec["libunwind"].prefix))

        stackguard = self.spec.variants["stackguard"].value
        if stackguard != "none":
            args.append("--enable-stack-overflow-check={0}".format(stackguard))

        if self.spec.satisfies("+tool"):
            args.append("--enable-tool")

        if self.spec.satisfies("+affinity"):
            args.append("--enable-affinity")

        return args
