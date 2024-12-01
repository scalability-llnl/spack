# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class GitFilterRepo(Package):
    """Quickly rewrite Git repository history (filter-branch replacement)"""

    homepage = "https://github.com/newren/git-filter-repo"
    url = "https://github.com/newren/git-filter-repo/releases/download/v2.34.0/git-filter-repo-2.34.0.tar.xz"

    maintainers("aphedges")

    license("MIT")

    version("2.38.0", sha256="db954f4cae9e47c6be3bd3161bc80540d44f5379cb9cf9df498f4e019f0a41a9")
    version("2.34.0", sha256="b1bf46af1e6a91a54056d0254e480803db8e40f631336c559a1a94d2a08389c4")

    depends_on("git@2.22.0:", type="run")
    depends_on("python@3.5:", type="run")

    def install(self, spec, prefix):
        new_shebang = "#!{0}\n".format(self.spec["python"].command)
        filter_file("^#!/usr/bin/env python3?$", new_shebang, "git-filter-repo")
        mkdirp(prefix.bin)
        install("git-filter-repo", prefix.bin)

        mkdirp(prefix.share.man.man1)
        install("Documentation/man1/git-filter-repo.1", prefix.share.man.man1)
