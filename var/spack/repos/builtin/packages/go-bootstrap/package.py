# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform
import re

from spack.package import *

# THIS PACKAGE SHOULD NOT EXIST
# it exists to make up for the inability to:
# * use an external go compiler
# * have go depend on itself
# * have a sensible way to find gccgo without a dep on gcc


class GoBootstrap(Package):
    """Old C-bootstrapped go to bootstrap real go"""

    homepage = "https://golang.org"
    url = "https://go.dev/dl/go1.20.1.darwin-amd64.tar.gz"

    extendable = True

    maintainers("alecbcs")

    executables = ["^go$"]

    # List binary go releases for multiple operating systems and architectures.
    # These binary versions are not intended to stay up-to-date. Instead we
    # should update these binary releases on a yearly schedule as
    # bootstrapping requirements are modified by new releases of go.
    go_releases = {
        "1.20.6": {
            "darwin": {
                "amd64": "98a09c085b4c385abae7d35b9155195d5e584d14988347ac7f18e4cbe3b5ef3d",
                "arm64": "1163be1998835a13f00dfc869a8e3cdebf86984ad41ff2fff43e35ac2a0d8344",
            },
            "linux": {
                "amd64": "b945ae2bb5db01a0fb4786afde64e6fbab50b67f6fa0eb6cfa4924f16a7ff1eb",
                "arm64": "4e15ab37556e979181a1a1cc60f6d796932223a0f5351d7c83768b356f84429b",
                "ppc64le": "a1b91a42a40bba54bfd5c96c23d72250e0c424038d0d2b5c7950b828b4905822",
            },
        },
        "1.17.13": {
            "darwin": {
                "amd64": "c101beaa232e0f448fab692dc036cd6b4677091ff89c4889cc8754b1b29c6608",
                "arm64": "e4ccc9c082d91eaa0b866078b591fc97d24b91495f12deb3dd2d8eda4e55a6ea",
            },
            "linux": {
                "amd64": "4cdd2bc664724dc7db94ad51b503512c5ae7220951cac568120f64f8e94399fc",
                "arm64": "914daad3f011cc2014dea799bb7490442677e4ad6de0b2ac3ded6cee7e3f493d",
                "ppc64le": "bd0763fb130f8412672ffe1e4a8e65888ebe2419e5caa9a67ac21e8c298aa254",
            },
        },
    }

    # Normalize architectures returned by platform to those used by the
    # Go project.
    go_targets = {
        "aarch64": "arm64",
        "arm64": "arm64",
        "ppc64le": "ppc64le",
        "amd64": "amd64",
        "x86_64": "amd64",
    }

    # determine system os and architecture/target
    os = platform.system().lower()
    target = go_targets.get(platform.machine().lower(), platform.machine().lower())

    license("BSD-3-Clause")

    # construct releases for current system configuration
    for release in go_releases:
        if os in go_releases[release] and target in go_releases[release][os]:
            version(release, sha256=go_releases[release][os][target])
            provides(f"go-or-gccgo-bootstrap@{release}", when=f"@{release}")

    # When the user adds a go compiler using ``spack external find go-bootstrap``,
    # this lets us get the version for packages.yaml. Then, the solver can avoid
    # to build the bootstrap go compiler(for aarch64, it's only gccgo) from source:
    @classmethod
    def determine_version(cls, exe):
        """Return the version of an externally provided go executable or ``None``"""
        output = Executable(exe)("version", output=str, error=str)
        match = re.search(r"go version go(\S+)", output)
        return match.group(1) if match else None

    def url_for_version(self, version):
        # allow maintainers to checksum multiple architectures via
        # `spack checksum go-bootstrap@1.18.9-darwin-arm64`
        match = re.search(r"(\S+)-(\S+)-(\S+)", str(version))
        if match:
            version = match.group(1)
            os = match.group(2)
            target = match.group(3)
        else:
            os = self.os
            target = self.target

        url = "https://go.dev/dl/go{0}.{1}-{2}.tar.gz"
        return url.format(version, os, target)

    def install(self, spec, prefix):
        install_tree(".", prefix)

    def setup_dependent_build_environment(self, env, dependent_spec):
        """Set GOROOT_BOOTSTRAP: When using an external compiler, get its GOROOT env"""
        if self.spec.external:
            # Use the go compiler added by ``spack external find go-bootstrap``:
            goroot = Executable(self.spec.prefix.bin.go)("env", "GOROOT", output=str)
        else:
            goroot = self.spec.prefix
        env.set("GOROOT_BOOTSTRAP", goroot)
