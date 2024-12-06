# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RubySvn2git(RubyPackage):
    """svn2git is a tiny utility for migrating projects from Subversion to Git
    while keeping the trunk, branches and tags where they should be. It uses
    git-svn to clone an svn repository and does some clean-up to make sure
    branches and tags are imported in a meaningful way, and that the code
    checked into master ends up being what's currently in your svn trunk rather
    than whichever svn branch your last commit was in."""

    homepage = "https://github.com/nirvdrum/svn2git/"
    url = "https://github.com/nirvdrum/svn2git/archive/v2.4.0.tar.gz"

    license("MIT")

    version("2.4.0", sha256="81d0a3eff5b12b729d0fe8ad117db386954c635067f1c86007360c6c76dec253")

    depends_on("git")
    depends_on("subversion+perl")
