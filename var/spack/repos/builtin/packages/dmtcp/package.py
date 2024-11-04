# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dmtcp(AutotoolsPackage):
    """DMTCP (Distributed MultiThreaded Checkpointing) transparently
    checkpoints a single-host or distributed computation in user-space --
    with no modifications to user code or to the O/S."""

    homepage = "https://dmtcp.sourceforge.net/"
    url = "https://github.com/dmtcp/dmtcp/archive/refs/tags/3.0.0.tar.gz"
    git = "https://github.com/dmtcp/dmtcp.git"

    license("LGPL-3.0-only")

    maintainers("karya0")
    version("main", branch="main")
    version("3.0.0", sha256="2c7e95e1dbc55db33433bfee48a65f274298e98f246a36ab6dad1e0694750d37")
    version("2.6.0", sha256="3ed62a86dd0cb9c828b93ee8c7c852d6f9c96a0efa48bcfe867521adf7bced68")
    version("2.5.2", sha256="0e3e5e15bd401b7b6937f2b678cd7d6a252eab0a143d5740b89cc3bebb4282be")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    patch("for_aarch64.patch", when="@2.6.0 target=aarch64:")
