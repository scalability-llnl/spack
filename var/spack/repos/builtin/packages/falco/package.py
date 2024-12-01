# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Falco(AutotoolsPackage):
    """A C++ drop-in replacement of FastQC to assess the quality of sequence read data"""

    homepage = "https://github.com/smithlabcode/falco"
    url = "https://github.com/smithlabcode/falco/releases/download/v1.2.1/falco-1.2.1.tar.gz"

    license("GPL-3.0-only")

    version("1.2.1", sha256="33de8aafac45c7aea055ed7ab837d0a39d12dcf782816cea8a6c648acb911057")

    depends_on("cxx", type="build")  # generated

    variant("htslib", default=False, description="Add support for BAM files")

    depends_on("gmake", type="build")
    depends_on("zlib-ng")
    depends_on("htslib", when="+htslib")

    def configure_args(self):
        if self.spec.satisfies("+htslib"):
            return ["--enable-htslib"]
        return []
