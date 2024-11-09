# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Clustalw(AutotoolsPackage):
    """Multiple alignment of nucleic acid and protein sequences."""

    homepage = "http://www.clustal.org/clustal2/"
    url = "http://www.clustal.org/download/2.1/clustalw-2.1.tar.gz"

    license("LGPL-3.0-only")

    version("2.1", sha256="e052059b87abfd8c9e695c280bfba86a65899138c82abccd5b00478a80f49486")

    depends_on("cxx", type="build")  # generated
