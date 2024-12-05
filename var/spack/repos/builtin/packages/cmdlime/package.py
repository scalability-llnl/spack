# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cmdlime(CMakePackage):
    """cmdlime is a C++17 header-only library for command line parsing that
    provides a concise, declarative interface without many details to remember."""

    homepage = "https://github.com/kamchatka-volcano/cmdlime"
    url = "https://github.com/kamchatka-volcano/cmdlime/archive/refs/tags/v2.5.0.tar.gz"

    license("MS-PL")

    version("2.5.0", sha256="d5188d7f075142fcb546099a4ee2a967f8248109c0bee8c084e0e00f37603481")

    depends_on("cxx", type="build")  # generated
