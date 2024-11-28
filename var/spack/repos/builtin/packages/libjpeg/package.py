# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libjpeg(AutotoolsPackage):
    """libjpeg is a widely used free library with functions for handling the
    JPEG image data format. It implements a JPEG codec (encoding and decoding)
    alongside various utilities for handling JPEG data."""

    homepage = "http://www.ijg.org"
    url = "https://www.ijg.org/files/jpegsrc.v9d.tar.gz"

    license("BitTorrent-1.0")

    version("9f", sha256="04705c110cb2469caa79fb71fba3d7bf834914706e9641a4589485c1f832565b")
    version("9e", sha256="4077d6a6a75aeb01884f708919d25934c93305e49f7e3f36db9129320e6f4f3d")
    version("9d", sha256="6c434a3be59f8f62425b2e3c077e785c9ce30ee5874ea1c270e843f273ba71ee")
    version("9c", sha256="650250979303a649e21f87b5ccd02672af1ea6954b911342ea491f351ceb7122")
    version("9b", sha256="240fd398da741669bf3c90366f58452ea59041cacc741a489b99f2f6a0bad052")
    version("9a", sha256="3a753ea48d917945dd54a2d97de388aa06ca2eb1066cbfdc6652036349fe05a7")

    depends_on("c", type="build")  # generated

    provides("jpeg")

    def check(self):
        # Libjpeg has both 'check' and 'test' targets that are aliases.
        # Only need to run the tests once.
        make("check")
