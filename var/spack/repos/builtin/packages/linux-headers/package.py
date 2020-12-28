# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LinuxHeaders(Package):
    """The Linux kernel headers."""

    homepage = "https://www.kernel.org/"
    url      = "https://www.kernel.org/pub/linux/kernel/v4.x/linux-4.9.10.tar.xz"
    list_url = "https://www.kernel.org/pub/linux/kernel"
    list_depth = 2

    version('4.9.10', sha256='bd6e05476fd8d9ea4945e11598d87bc97806bbc8d03556abbaaf809707661525')

    def setup_build_environment(self, env):
        # This variable is used in the Makefile. If it is defined on the
        # system, it can break the build if there is no build recipe for
        # that specific ARCH
        env.unset('ARCH')

    def install(self, spec, prefix):
        make('headers_install', 'INSTALL_HDR_PATH={0}'.format(prefix))
