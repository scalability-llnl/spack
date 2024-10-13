# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libpciaccess(AutotoolsPackage, XorgPackage):
    """Generic PCI access library."""

    homepage = "https://cgit.freedesktop.org/xorg/lib/libpciaccess/"
    xorg_mirror_path = "lib/libpciaccess-0.13.5.tar.gz"

    license("X11")

    version("0.17", sha256="bf6985a77d2ecb00e2c79da3edfb26b909178ffca3f2e9d14ed0620259ab733b")
    version("0.16", sha256="84413553994aef0070cf420050aa5c0a51b1956b404920e21b81e96db6a61a27")
    version("0.13.5", sha256="fe26ec788732b4ef60b550f2d3fa51c605d27f646e18ecec878f061807a3526e")
    version("0.13.4", sha256="74d92bda448e6fdb64fee4e0091255f48d625d07146a121653022ed3a0ca1f2f")

    depends_on("c", type="build")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")

    patch("nvhpc.patch", when="%nvhpc")

    # A known issue exists when building with PGI as documented here:
    # https://bugs.freedesktop.org/show_bug.cgi?id=94398
    # https://www.pgroup.com/userforum/viewtopic.php?f=4&t=5126
    # https://gitlab.freedesktop.org/xorg/lib/libpciaccess/issues/7
    #
    # When the ability to use dependencies built by another compiler, using a
    # libpciaccess built by gcc should be usable by PGI builds.
    conflicts("%pgi")

    conflicts("platform=darwin")

    def configure_args(self):
        config_args = []

        if self.spec.satisfies("%nvhpc@:20.11") and (
            self.spec.target.family == "aarch64" or self.spec.target.family == "ppc64le"
        ):
            config_args.append("--disable-strict-compilation")
            config_args.append("--disable-selective-werror")

        return config_args
