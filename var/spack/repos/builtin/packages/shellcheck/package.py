# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.package import *

_versions = {
    "0.9.0": {
        "darwin-x86_64": "7d3730694707605d6e60cec4efcb79a0632d61babc035aa16cda1b897536acf5",
        "linux-aarch64": "179c579ef3481317d130adebede74a34dbbc2df961a70916dd4039ebf0735fae",
        "linux-armv6hf": "03deed9ded9dd66434ccf9649815bcde7d275d6c9f6dcf665b83391673512c75",
        "linux-x86_64": "700324c6dd0ebea0117591c6cc9d7350d9c7c5c287acbad7630fa17b1d4d9e2f",
    }
}


class Shellcheck(Package):
    """ShellCheck is a GPLv3 tool that gives warnings and suggestions for bash/sh shell scripts.

    Note: Spack does not have a Haskell toolchain, so a ShellCheck binary is downloaded instead of
    being compiled from source.
    """

    homepage = "https://www.shellcheck.net"
    url = "https://github.com/koalaman/shellcheck/releases/download/v0.9.0/shellcheck-v0.9.0.linux.x86_64.tar.xz"

    maintainers("aphedges")

    # The following installs the binaries for shellcheck. The reason for
    # installing binaries is that shellcheck is a Haskell package and the
    # Haskell framework is not yet in Spack. See #1408 for a discussion of the
    # challenges with Haskell, and see the pandoc package for a precedent of
    # downloading a Haskell-derived binary.

    license("GPL-3.0")

    for ver, packages in _versions.items():
        system = platform.system().lower()
        machine = platform.machine().lower()
        key = "{0}-{1}".format(system, machine)
        pkg_hash = packages.get(key)
        if pkg_hash:
            url = (
                "https://github.com/koalaman/shellcheck/releases/download"
                "/v{0}/shellcheck-v{0}.{1}.{2}.tar.xz".format(ver, system, machine)
            )
            version(ver, sha256=pkg_hash, url=url)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("shellcheck", prefix.bin)
