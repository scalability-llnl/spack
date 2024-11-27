# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Macfuse(Package):
    """FUSE for macOS allows you to extend macOS via third party file systems."""

    homepage = "https://osxfuse.github.io/"
    git = "https://github.com/osxfuse/osxfuse.git"
    has_code = False  # only distributed in binary form

    version("4.1.2")

    provides("fuse")
    conflicts("platform=linux", msg="macfuse does not support linux, use libfuse instead")

    def install(self, spec, prefix):
        msg = """
macFUSE is only distributed in binary form.
To use macFUSE with Spack, manually download the .dmg from:

    https://github.com/osxfuse/osxfuse/releases

and double-click to install. Once macFUSE is installed,
add it as an external package by running:

    $ spack config edit packages

and add an entry like so:

    packages:
      macfuse:
        buildable: false
        externals:
        - spec: macfuse@4.1.2
          prefix: /Library/Frameworks/macFUSE.framework"""

        raise InstallError(msg)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.set("FUSE_LIBRARY_PATH", self.prefix.macFUSE)
