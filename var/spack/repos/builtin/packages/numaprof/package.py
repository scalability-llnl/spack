# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Numaprof(CMakePackage):
    """
    NumaProf is a NUMA memory access profiling tool. It is based on Intel-PIN to intercept
    all the memory access and report them on NUMA counters so we can tell by annotating the
    source code where you make local, remote, unpinned memory accessed. It also provide
    some charts to better understand the NUMA behavior of the application.
    """

    # Infos
    homepage = "https://memtt.github.io/numaprof"
    url = "https://github.com/memtt/numaprof/releases/download/v1.1.4/numaprof-1.1.4.tar.bz2"
    maintainers("svalat")

    license("CECILL-C")

    # Versions
    version("1.1.5", sha256="7c479cc6d39f2fe685532b9aaeb9efce8153350177fdcc24133e447dd0776323")
    version("1.1.4", sha256="96cc5e153895f43d8be58e052433c9e7c9842071cc6bf915b3b1b346908cbbff")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # Variants
    variant(
        "qt", default=False, description="Build the QT embeded webview with Pyton + QT web toolkit"
    )

    # Dependencies
    depends_on("python", type=("build", "run"))
    depends_on("intel-pin", type=("build", "link", "run"))
    depends_on("numactl")
    depends_on("py-pyqt5", "+qt", type=("build", "run"))

    # Patches
    patch(
        "numaprof-1.1.4-pin-layout.patch",
        when="@1.1.4:",
        sha256="a2e3242f72b502285da2ad41dd896382e99a8987bda9ff38e081a048776ee7b3",
    )

    # Generate build command
    def cmake_args(self):
        spec = self.spec
        args = ["-DPINTOOL_PREFIX=" + spec["intel-pin"].prefix]
        return args
