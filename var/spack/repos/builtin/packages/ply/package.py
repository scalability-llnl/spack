# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ply(AutotoolsPackage):
    """A light-weight dynamic tracer for Linux that leverages the
    kernel's BPF VM in concert with kprobes and tracepoints to attach
    probes to arbitrary points in the kernel."""

    homepage = "https://github.com/iovisor/ply"
    git = "https://github.com/iovisor/ply.git"

    license("GPL-2.0-only")

    version("2.1.1", commit="899afb0c35ba2191dd7aa21f13bc7fde2655c475")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autogen.sh")
