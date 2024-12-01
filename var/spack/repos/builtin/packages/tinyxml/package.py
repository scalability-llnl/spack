# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path

from spack.package import *


class Tinyxml(CMakePackage):
    """Simple, small, efficient, C++ XML parser"""

    homepage = "http://grinninglizard.com/tinyxml/"
    url = "https://downloads.sourceforge.net/project/tinyxml/tinyxml/2.6.2/tinyxml_2_6_2.tar.gz"

    license("Zlib")

    version("2.6.2", sha256="15bdfdcec58a7da30adc87ac2b078e4417dbe5392f3afb719f9ba6d062645593")

    variant("shared", default=True, description="Build a shared library")

    def url_for_version(self, version):
        url = "https://sourceforge.net/projects/tinyxml/files/tinyxml/{0}/tinyxml_{1}.tar.gz"
        return url.format(version.dotted, version.underscored)

    def patch(self):
        copy(join_path(os.path.dirname(__file__), "CMakeLists.txt"), "CMakeLists.txt")

    def cmake_args(self):
        return [self.define_from_variant("BUILD_SHARED_LIBS", "shared")]
