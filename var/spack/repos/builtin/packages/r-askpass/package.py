# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAskpass(RPackage):
    """Safe Password Entry for R, Git, and SSH.

    Cross-platform utilities for prompting the user for credentials or a
    passphrase, for example to authenticate with a server or read a protected
    key. Includes native programs for MacOS and Windows, hence no 'tcltk' is
    required. Password entry can be invoked in two different ways: directly
    from R via the askpass() function, or indirectly as password-entry back-end
    for 'ssh-agent' or 'git-credential' via the SSH_ASKPASS and GIT_ASKPASS
    environment variables. Thereby the user can be prompted for credentials or
    a passphrase if needed when R calls out to git or ssh."""

    cran = "askpass"

    license("MIT")

    version("1.2.0", sha256="b922369781934d0ffc8d0c0177e8ace56796c2e6a726f65e460c16f792592cef")
    version("1.1", sha256="db40827d1bdbb90c0aa2846a2961d3bf9d76ad1b392302f9dd84cc2fd18c001f")

    depends_on("r-sys@2.1:", type=("build", "run"))
