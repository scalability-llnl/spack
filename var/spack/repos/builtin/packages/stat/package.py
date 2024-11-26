# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Stat(AutotoolsPackage):
    """Library to create, manipulate, and export graphs Graphlib."""

    homepage = "https://paradyn.org/STAT/STAT.html"
    url = "https://github.com/LLNL/STAT/archive/v2.0.0.tar.gz"
    git = "https://github.com/llnl/stat.git"
    maintainers("lee218llnl")

    version("develop", branch="develop")
    version(
        "4.2.1",
        sha256="137529889ec5b5f9b9bae3a0864a385c5814e989d0074228dd3500e3e713801d",
        url="https://github.com/LLNL/STAT/releases/download/v4.2.1/stat-4.2.1.tar.gz",
    )
    version(
        "4.2.0",
        sha256="d244d53585b0949e308354eb024f7a89ee3467fd2866b818e8aa6c8b5d372ced",
        url="https://github.com/LLNL/STAT/releases/download/v4.2.0/stat-4.2.0.tar.gz",
    )
    version(
        "4.1.0",
        sha256="1d5b00afd563cf3bd9dd40818c44a03d7d4b13356216881513c058566c3b0080",
        url="https://github.com/LLNL/STAT/files/6193568/stat-4.1.0.tar.gz",
    )
    version(
        "4.0.2",
        sha256="9ece10dde8e1579c9db469ac8d2391b26e59498c0947dbb271c2d01d7ef0a65d",
        url="https://github.com/LLNL/STAT/releases/download/v4.0.2/stat-4.0.2.tar.gz",
    )
    version(
        "4.0.1",
        sha256="ae3fbd6946003fb16233d82d40285780a9a802da5fe30d09adb8a8b2a2cc4ad6",
        url="https://github.com/LLNL/STAT/files/2489327/stat-4.0.1.tar.gz",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # TODO: dysect requires Dyninst patch for version 3.0.0b
    variant("dysect", default=False, description="enable DySectAPI")
    variant("examples", default=False, description="enable examples")
    variant("fgfs", default=True, description="enable file broadcasting")
    variant("gui", default=True, description="enable GUI")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("dyninst", when="@4.2.1:")
    depends_on("dyninst@:11.9", when="~dysect @:4.2.0")
    depends_on("dyninst@:9", when="@:4.0.1")
    depends_on("dyninst@8.2.1+stat_dysect", when="+dysect")
    # we depend on fgfs@master to avoid seg faults with fgfs 1.1
    depends_on("fast-global-file-status@1.1.1:", when="+fgfs")
    depends_on("graphlib@3.0.0")
    depends_on("graphviz", type=("build", "link", "run"))
    # we depend on mpa@master for bug fixes since launchmon 1.0.2
    depends_on("launchmon@1.2.0:")
    depends_on("mrnet")
    depends_on("python")
    depends_on("py-xdot@1.0", when="+gui")
    depends_on("swig")
    depends_on("mpi", when="+examples")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)

    # No Mac support due to dependencies like dyninst, elf etc.
    conflicts("platform=darwin", msg="macOS is not supported")

    def configure_args(self):
        spec = self.spec
        args = [
            "--with-launchmon=%s" % spec["launchmon"].prefix,
            "--with-mrnet=%s" % spec["mrnet"].prefix,
            "--with-graphlib=%s" % spec["graphlib"].prefix,
            "--with-stackwalker=%s" % spec["dyninst"].prefix,
            "--with-python=%s" % spec["python"].command.path,
            "--with-boost=%s" % spec["boost"].prefix,
        ]
        if "+fgfs" in spec:
            args.append("--with-fgfs=%s" % spec["fast-global-file-status"].prefix)
        if "+dysect" in spec:
            args.append("--enable-dysectapi")
        if "~gui" in spec:
            args.append("--disable-gui")
        if "~examples" in spec:
            args.append("--disable-examples")
        return args
