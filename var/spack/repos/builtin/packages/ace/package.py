# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ace(MakefilePackage):
    """ACE is an open-source framework that provides many components and
       patterns for developing high-performance, distributed real-time and
       embedded systems. ACE provides powerful, yet efficient abstractions
       for sockets, demultiplexing loops, threads, synchronization
       primitives."""

    homepage = "http://www.dre.vanderbilt.edu/~schmidt/ACE.html"
    url = "http://download.dre.vanderbilt.edu/previous_versions/ACE-6.5.1.tar.gz"

    version('6.5.12', 'de96c68a6262d6b9ba76b5057c02c7e6964c070b1328a63bf70259e9530a7996')
    version('6.5.6', '7717cad84d4a9c3d6b2c47963eb555d96de0be657870bcab6fcef4c0423af0de')
    version('6.5.1', '1f318adadb19da23c9be570a9c600a330056b18950fe0bf0eb1cf5cac8b72a32')
    version('6.5.0', 'b6f9ec922fbdcecb4348e16d851d0d1f135df1836dfe77d2e0b64295ddb83066')

    def edit(self, spec, prefix):

        # Dictionary mapping: compiler-name : ACE config-label
        supported = {'intel': '_icc', 'gcc': ''}

        if not(self.compiler.name in supported):
            raise Exception('compiler ' + self.compiler.name +
                            ' not supported in ace spack-package')

        env['ACE_ROOT'] = self.stage.source_path

        with working_dir('./ace'):
            with open('config.h', 'w') as f:
                f.write('#include "ace/config-linux.h"\n')

        with working_dir(join_path(self.stage.source_path,
                                   'include/makeinclude')):
            with open('platform_macros.GNU', 'w') as f:
                f.write("include $(ACE_ROOT)/include/makeinclude/"
                        "platform_linux" + supported[self.compiler.name]
                        + ".GNU\n")
                f.write("INSTALL_PREFIX=%s" % prefix)
