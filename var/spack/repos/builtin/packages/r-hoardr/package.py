# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RHoardr(RPackage):
    """Manage Cached Files.

    Suite of tools for managing cached files, targeting use in other R
    packages. Uses 'rappdirs' for cross-platform paths. Provides utilities to
    manage cache directories, including targeting files by path or by key;
    cached directories can be compressed and uncompressed easily to save disk
    space."""

    cran = "hoardr"

    license("MIT")

    version("0.5.4", sha256="4e031ac1317584451c09bc8288ed73fb2d6ceea3c10d29dbb4be08157e489a37")
    version("0.5.3", sha256="b9e4d1350e1fde7db922e55128306e3768ee46ff9532f05c96543dcae383647c")
    version("0.5.2", sha256="819113f0e25da105f120a676b5173872a4144f2f6f354cad14b35f898e76dc54")

    depends_on("r-r6@2.2.0:", type=("build", "run"))
    depends_on("r-rappdirs@0.3.1:", type=("build", "run"))
    depends_on("r-digest", type=("build", "run"))
