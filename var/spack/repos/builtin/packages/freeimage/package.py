# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Freeimage(MakefilePackage):
    """FreeImage is an Open Source library project for developers who would like
    to support popular graphics image formats like PNG, BMP, JPEG, TIFF and
    others as needed by today's multimedia applications"""

    homepage = "https://freeimage.sourceforge.net/"

    version("3.18.0", sha256="f41379682f9ada94ea7b34fe86bf9ee00935a3147be41b6569c9605a53e438fd")

    patch("install_fixes.patch", when="@3.18.0")

    def edit(self, spec, prefix):
        env["DESTDIR"] = prefix
        env["CXXFLAGS"] = "-std=c++14"

    def url_for_version(self, version):
        url = "https://downloads.sourceforge.net/project/freeimage/Source%20Distribution/{0}/FreeImage{1}.zip"
        return url.format(version, version.joined)
