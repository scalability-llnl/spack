# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rlwrap(AutotoolsPackage):
    """rlwrap is a 'readline wrapper', a small utility that uses the GNU
    readline library to allow the editing of keyboard input for any command."""

    homepage = "https://github.com/hanslub42/rlwrap"
    url = "https://github.com/hanslub42/rlwrap/releases/download/v0.43/rlwrap-0.43.tar.gz"

    license("GPL-2.0-or-later")

    version("0.46.1", sha256="2711986a1248f6ac59e2aecf5586205835970040d300a42b4bf8014397e73e37")
    version("0.46", sha256="b4bd79fda824426dae65236e338ba7daf3f0d0acad7c1561d4d5e6dadcfd539d")
    version("0.45.2", sha256="9f8870deb46e473d21b5db89d709b6497f4ef9fa06d44eebc5f821daa00c8eca")
    version("0.44", sha256="cd7ff50cde66e443cbea0049b4abf1cca64a74948371fa4f1b5d9a5bbce1e13c")
    version("0.43", sha256="8e86d0b7882d9b8a73d229897a90edc207b1ae7fa0899dca8ee01c31a93feb2f")

    depends_on("c", type="build")  # generated

    depends_on("readline@4.2:")

    def url_for_version(self, version):
        if version < Version("0.46.1"):
            return super().url_for_version(version)
        # The latest release (0.46.1) removed the "v" prefix.
        url_fmt = "https://github.com/hanslub42/rlwrap/releases/download/{0}/rlwrap-{0}.tar.gz"
        return url_fmt.format(version)
