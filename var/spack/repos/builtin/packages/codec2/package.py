# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Codec2(CMakePackage):
    """Open source speech codec designed for communications quality speech
    between 450 and 3200 bit/s. The main application is low bandwidth
    HF/VHF digital radio."""

    homepage = "http://www.rowetel.com/codec2.html"
    url      = "https://github.com/drowe67/codec2/archive/v0.9.2.tar.gz"

    version('0.9.2', sha256='19181a446f4df3e6d616b50cabdac4485abb9cd3242cf312a0785f892ed4c76c')
