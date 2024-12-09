# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pflask(CMakePackage):
    """Pflask is a simple tool for creating process containers on LInux."""

    homepage = "https://ghedo.github.io/pflask/"
    url = "https://github.com/ghedo/pflask/archive/v0.2.tar.gz"

    license("BSD-2-Clause")

    version("0.2", sha256="dabbd060d1c50174de5fffae9ec97dc1d41b22de898a8280166cba768c940ebd")
    version("0.1", sha256="3c41c670fd8c48b7b6a41d697b444df8bf95380937ba4f734b41af135d5c5816")

    depends_on("c", type="build")  # generated
