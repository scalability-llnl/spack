# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RCredentials(RPackage):
    """Tools for Managing SSH and Git Credentials

    Setup and retrieve HTTPS and SSH credentials for use with 'git' and other
    services. For HTTPS remotes the package interfaces the 'git-credential'
    utility which 'git' uses to store HTTP usernames and passwords. For SSH
    remotes we provide convenient functions to find or generate appropriate SSH
    keys. The package both helps the user to setup a local git installation,
    and also provides a back-end for git/ssh client libraries to authenticate
    with existing user credentials."""

    homepage = "https://docs.ropensci.org/credentials"
    url      = "https://cloud.r-project.org/src/contrib/credentials_1.3.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/credentials"

    version('1.3.0', sha256='c119ec26fd97b977c3b0cd1eb8fad3c59b84df6262c3adbf5ee9f3d6c9903ff1')

    depends_on('r-openssl@1.3:', type=('build', 'run'))
    depends_on('r-sys@2.1:', type=('build', 'run'))
    depends_on('r-curl', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-askpass', type=('build', 'run'))
    depends_on('git', type='run')
