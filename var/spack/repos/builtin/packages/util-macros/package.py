# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class UtilMacros(AutotoolsPackage, XorgPackage):
    """This is a set of autoconf macros used by the configure.ac scripts in
    other Xorg modular packages, and is needed to generate new versions
    of their configure scripts with autoconf."""

    homepage = "http://cgit.freedesktop.org/xorg/util/macros/"
    xorg_mirror_path = "util/util-macros-1.19.1.tar.bz2"

    version('1.19.1', sha256='18d459400558f4ea99527bc9786c033965a3db45bf4c6a32eefdc07aa9e306a6')
    version('1.19.0', sha256='2835b11829ee634e19fa56517b4cfc52ef39acea0cd82e15f68096e27cbed0ba')

    def setup_dependent_build_environment(self, env, dependent_spec):
        """Adds the ACLOCAL path for autotools."""
        env.append_path('ACLOCAL_PATH', self.prefix.share.aclocal)
