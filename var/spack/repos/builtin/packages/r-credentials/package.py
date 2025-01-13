# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCredentials(RPackage):
    """Tools for Managing SSH and Git Credentials.

    Setup and retrieve HTTPS and SSH credentials for use with 'git' and other
    services. For HTTPS remotes the package interfaces the 'git-credential'
    utility which 'git' uses to store HTTP usernames and passwords. For SSH
    remotes we provide convenient functions to find or generate appropriate SSH
    keys. The package both helps the user to setup a local git installation,
    and also provides a back-end for git/ssh client libraries to authenticate
    with existing user credentials."""

    cran = "credentials"

    license("MIT")

    version("2.0.1", sha256="2c7cfc45bd4afa9a2c2b85d43e907b212da3468781e1b617737bd095253c358b")
    version("1.3.2", sha256="2ffa7c11bedbfa034adf553d0a2f2e4f6a496b858af753a09a89219cff9028b8")
    version("1.3.0", sha256="c119ec26fd97b977c3b0cd1eb8fad3c59b84df6262c3adbf5ee9f3d6c9903ff1")

    depends_on("r-openssl@1.3:", type=("build", "run"))
    depends_on("r-sys@2.1:", type=("build", "run"))
    depends_on("r-curl", type=("build", "run"))
    depends_on("r-jsonlite", type=("build", "run"))
    depends_on("r-askpass", type=("build", "run"))
    depends_on("git", type="run")
