# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PopplerData(CMakePackage):
    """This package consists of encoding files for use with poppler. The
    encoding files are optional and poppler will automatically read them if
    they are present.  When installed, the encoding files enables poppler to
    correctly render CJK and Cyrrilic properly.  While poppler is licensed
    under the GPL, these encoding files have different license, and thus
    distributed separately."""

    homepage = "https://poppler.freedesktop.org/"
    url = "https://poppler.freedesktop.org/poppler-data-0.4.9.tar.gz"

    license("GPL-2.0-or-later AND BSD-3-Clause AND MIT")

    version("0.4.12", sha256="c835b640a40ce357e1b83666aabd95edffa24ddddd49b8daff63adb851cdab74")
    version("0.4.9", sha256="1f9c7e7de9ecd0db6ab287349e31bf815ca108a5a175cf906a90163bdbe32012")

    depends_on("cmake@2.6:", type="build")
