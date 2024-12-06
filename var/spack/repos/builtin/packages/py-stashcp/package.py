# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyStashcp(PythonPackage):
    """Stashcp uses geo located nearby caches in order to copy from the OSG
    Connect's stash storage service to a job's workspace on a cluster."""

    homepage = "https://github.com/opensciencegrid/StashCache"
    pypi = "stashcp/stashcp-6.1.0.tar.gz"

    maintainers("wdconinc")

    version("6.1.0", sha256="40484b40aeb853eb6a5f5472daf533a176d61fa6ab839cd265ea0baa3fe63068")

    depends_on("py-setuptools", type=("build", "run"))
