# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Speex(AutotoolsPackage):
    """Speex is an Open Source/Free Software patent-free
    audio compression format designed for speech."""

    homepage = "https://speex.org"
    url = "http://downloads.us.xiph.org/releases/speex/speex-1.2.0.tar.gz"

    license("BSD-3-Clause")

    version("1.2.1", sha256="4b44d4f2b38a370a2d98a78329fefc56a0cf93d1c1be70029217baae6628feea")
    version("1.2.0", sha256="eaae8af0ac742dc7d542c9439ac72f1f385ce838392dc849cae4536af9210094")

    depends_on("c", type="build")  # generated
