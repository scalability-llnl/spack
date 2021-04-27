# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RGert(RPackage):
    """Simple Git Client for R

    Simple git client for R based on 'libgit2' with support for SSH and HTTPS
    remotes. All functions in 'gert' use basic R data types (such as vectors
    and data-frames) for their arguments and return values. User credentials
    are shared with command line 'git' through the git-credential store and ssh
    keys stored on disk or ssh-agent. On Linux, a somewhat recent version of
    'libgit2' is required; we provide a 'PPA' for older Ubuntu 'LTS'
    versions."""

    homepage = "https://docs.ropensci.org/gert/"
    url      = "https://cloud.r-project.org/src/contrib/gert_1.0.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/gert"

    version('1.0.2', sha256='36687ab98291d50a35752fcb2e734a926a6b845345c18d36e3f48823f68304d3')

    depends_on('r-askpass', type=('build', 'run'))
    depends_on('r-credentials@1.2.1:', type=('build', 'run'))
    depends_on('r-openssl@1.4.1:', type=('build', 'run'))
    depends_on('r-rstudioapi@0.11:', type=('build', 'run'))
    depends_on('r-zip@2.1.0:', type=('build', 'run'))
    depends_on('libgit2@0.26:')
