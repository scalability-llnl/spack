# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class DecentralizedInternet(MakefilePackage):
    """A library for building decentralized and grid computing projects"""

    homepage = "https://lonero.readthedocs.io"
    url = "https://github.com/Lonero-Team/Decentralized-Internet/releases/download/4.2.3/Decentralized.Internet.tar.gz"

    license("MIT")

    maintainers("Lonero-Team", "Mentors4edu")
    version("4.2.3", sha256="2922b9128b411ece2f04d07942a453f1e772548aa27b3936c9f9bcfbc0737058")

    depends_on("c", type="build")  # generated
