# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Jump(GoPackage):
    """Jump integrates with your shell and learns about your navigational habits
    by keeping track of the directories you visit. It gives you the most visited
    directory for the shortest search term you type."""

    homepage = "https://github.com/gsamokovarov/jump"
    url = "https://github.com/gsamokovarov/jump/archive/refs/tags/v0.51.0.tar.gz"

    maintainers("fthaler")

    license("MIT", checked_by="fthaler")

    version("0.51.0", sha256="ce297cada71e1dca33cd7759e55b28518d2bf317cdced1f3b3f79f40fa1958b5")

    depends_on("go@1.16:", type="build")
