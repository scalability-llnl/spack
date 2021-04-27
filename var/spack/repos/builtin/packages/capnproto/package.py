# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Capnproto(AutotoolsPackage):
    """Cap'n Proto is an insanely fast data interchange
    format and capability-based RPC system.
    """

    homepage = "https://capnproto.org/"
    url      = "https://capnproto.org/capnproto-c++-0.7.0.tar.gz"
    git      = "https://github.com/capnproto/capnproto"

    version('0.8.0', sha256='d1f40e47574c65700f0ec98bf66729378efabe3c72bc0cda795037498541c10d')
    version('0.7.0', sha256='c9a4c0bd88123064d483ab46ecee777f14d933359e23bff6fb4f4dbd28b4cd41')

    def configure_args(self):
        return ['--without-openssl']
