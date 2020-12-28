# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CodeServer(Package):
    """code-server is VS Code running on a remote server,
    accessible through the browser."""

    homepage = "https://github.com/cdr/code-server"
    url      = "https://github.com/cdr/code-server/releases/download/3.1.0/code-server-3.1.0-linux-x86_64.tar.gz"

    version('3.4.1', sha256='957cc7bafb399b4d8c82fcfc9dc0b4e6ce50d095f2636a31320a628ada75d6a8')
    version('3.1.1', sha256='5dd922d28b2e351c146081849d987fb1e439ee7d53b941434b2eecb2a194da71')
    version('3.1.0', sha256='5ef85c8f280ce781a176a8b77386b333efe892755a5c325a1782e4eac6016e59')

    depends_on('git@2:')

    def install(self, spec, prefix):
        install_tree('.', prefix)

        if spec.version <= Version('3.1.1'):
            mkdir(prefix.bin)
            symlink('{0}/code-server'.format(prefix), prefix.bin)
