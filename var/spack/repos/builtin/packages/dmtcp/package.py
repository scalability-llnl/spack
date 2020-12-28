# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dmtcp(AutotoolsPackage):
    """DMTCP (Distributed MultiThreaded Checkpointing) transparently
    checkpoints a single-host or distributed computation in user-space --
    with no modifications to user code or to the O/S."""

    homepage = "http://dmtcp.sourceforge.net/"
    url      = "https://sourceforge.net/projects/dmtcp/files/2.6.0/dmtcp-2.6.0.tar.gz/download"

    version('2.6.0', sha256='3ed62a86dd0cb9c828b93ee8c7c852d6f9c96a0efa48bcfe867521adf7bced68')
    version('2.5.2', sha256='0e3e5e15bd401b7b6937f2b678cd7d6a252eab0a143d5740b89cc3bebb4282be')
    patch('for_aarch64.patch', when='@2.6.0 target=aarch64:')
