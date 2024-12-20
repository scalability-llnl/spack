# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Jujutsu(CargoPackage):
    """A Git-compatible VCS that is both simple and powerful"""

    homepage = "https://jj-vcs.github.io/jj/latest/"
    url = "https://github.com/jj-vcs/jj/archive/refs/tags/v0.24.0.tar.gz"

    maintainers("pranav-sivaraman")

    license("Apache-2.0", checked_by="github_user1")

    version(
        "0.24.0",
        sha256="c0e92ec25b7500deec2379a95ab655c6c92021cf4ccb29511fee2377e37b35d6",
    )

    depends_on("rust@1.76:")
