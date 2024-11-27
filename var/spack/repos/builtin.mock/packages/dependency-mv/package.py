# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class DependencyMv(Package):
    """Package providing a virtual dependency and with a multivalued variant."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/foo-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    variant("cuda", default=False, description="Build with CUDA")
    variant("cuda_arch", values=any_combination_of("10", "11"), when="+cuda")
