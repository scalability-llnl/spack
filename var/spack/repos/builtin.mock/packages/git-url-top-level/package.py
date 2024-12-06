# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GitUrlTopLevel(Package):
    """Mock package that top-level git and url attributes.

    This demonstrates how Spack infers fetch mechanisms from parameters
    to the ``version`` directive.

    """

    homepage = "http://www.git-fetch-example.com"

    git = "https://example.com/some/git/repo"
    url = "https://example.com/some/tarball-1.0.tar.gz"

    # These resolve to git fetchers
    version("develop", branch="develop")
    version("submodules", submodules=True)
    version("3.4", commit="abc34")
    version("3.3", branch="releases/v3.3", commit="abc33")
    version("3.2", branch="releases/v3.2")
    version("3.1", tag="v3.1", commit="abc31")
    version("3.0", tag="v3.0")

    # These resolve to URL fetchers
    version(
        "2.3",
        sha256="0000000000000000000000000000000000000000000000000000000000000023",
        url="https://www.example.com/foo2.3.tar.gz",
    )
    version(
        "2.2",
        sha256="0000000000000000000000000000000000000000000000000000000000000022",
        url="https://www.example.com/foo2.2.tar.gz",
    )
    version("2.1", sha256="0000000000000000000000000000000000000000000000000000000000000021")
    version("2.0", sha256="0000000000000000000000000000000000000000000000000000000000000020")

    # These result in a FetcherConflict b/c we can't tell what to use
    version(
        "1.3",
        sha256="f66bbef3ccb8b06542c57d69804c5b0aba72051f693c17761ad8525786d259fa",
        commit="abc13",
    )
    version(
        "1.2",
        sha512="f66bbef3ccb8b06542c57d69804c5b0aba72051f693c17761ad8525786d259fa"
        "9ed8f2e950a4fb8a4b936f33e689187784699357bc16e49f33dfcda8ab8b00e4",
        branch="releases/v1.2",
    )
    version("1.1", md5="00000000000000000000000000000011", tag="v1.1")
    version("1.0", md5="00000000000000000000000000000011", tag="abc123")
