# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Datamash(AutotoolsPackage, GNUMirrorPackage):
    """GNU datamash is a command-line program which performs basic numeric,
    textual and statistical operations on input textual data files.
    """

    homepage = "https://www.gnu.org/software/datamash/"
    gnu_mirror_path = "datamash/datamash-1.0.5.tar.gz"

    license("GPL-3.0-or-later")

    version("1.8", sha256="7ad97e8c7ef616dd03aa5bd67ae24c488272db3e7d1f5774161c18b75f29f6fd")
    version("1.3", sha256="eebb52171a4353aaad01921384098cf54eb96ebfaf99660e017f6d9fc96657a6")
    version("1.1.0", sha256="a9e5acc86af4dd64c7ac7f6554718b40271aa67f7ff6e9819bdd919a25904bb0")
    version("1.0.7", sha256="1a0b300611a5dff89e08e20773252b00f5e2c2d65b2ad789872fc7df94fa8978")
    version("1.0.6", sha256="0154c25c45b5506b6d618ca8e18d0ef093dac47946ac0df464fb21e77b504118")
    version("1.0.5", sha256="cb7c0b7bf654eea5bb80f10c1710c8dffab8106549fd6b4341cba140e15a9938")

    depends_on("c", type="build")  # generated

    build_directory = "spack-build"
