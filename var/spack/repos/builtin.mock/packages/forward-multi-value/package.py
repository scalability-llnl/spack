# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ForwardMultiValue(Package):
    """A package that forwards the value of a multi-valued variant to a dependency"""

    homepage = "http://www.llnl.gov"
    url = "http://www.llnl.gov/mpileaks-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    variant("cuda", default=False, description="Build with CUDA")
    variant("cuda_arch", values=any_combination_of("10", "11"), when="+cuda")

    depends_on("dependency-mv")

    requires("^dependency-mv cuda_arch=10", when="+cuda cuda_arch=10 ^dependency-mv+cuda")
    requires("^dependency-mv cuda_arch=11", when="+cuda cuda_arch=11 ^dependency-mv+cuda")
