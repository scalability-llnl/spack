# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class UtilMacros(AutotoolsPackage, XorgPackage):
    """This is a set of autoconf macros used by the configure.ac scripts in
    other Xorg modular packages, and is needed to generate new versions
    of their configure scripts with autoconf."""

    homepage = "https://gitlab.freedesktop.org/xorg/util/macros"
    xorg_mirror_path = "util/util-macros-1.19.1.tar.xz"

    maintainers("robert-mijakovic", "wdconinc")

    license("MIT")

    version("1.20.1", sha256="0b308f62dce78ac0f4d9de6888234bf170f276b64ac7c96e99779bb4319bcef5")
    version("1.19.3", sha256="0f812e6e9d2786ba8f54b960ee563c0663ddbe2434bf24ff193f5feab1f31971")
    version("1.19.2", sha256="d7e43376ad220411499a79735020f9d145fdc159284867e99467e0d771f3e712")
    version("1.19.1", sha256="18d459400558f4ea99527bc9786c033965a3db45bf4c6a32eefdc07aa9e306a6")
    version("1.19.0", sha256="2835b11829ee634e19fa56517b4cfc52ef39acea0cd82e15f68096e27cbed0ba")

    # note: url_for_version can only return a single url, no mirrors
    def url_for_version(self, version):
        if self.spec.satisfies("@:1.19"):
            return spack.url.substitute_version(self.urls[0].replace("xz", "bz2"), version)

    def setup_dependent_build_environment(self, env, dependent_spec):
        """Adds the ACLOCAL path for autotools."""
        env.append_path("ACLOCAL_PATH", self.prefix.share.aclocal)
