# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Utf8cpp(Package):
    """A simple, portable and lightweight generic library for handling UTF-8
    encoded strings."""

    homepage = "https://utfcpp.sourceforge.net/"

    version("2.3.4", sha256="3373cebb25d88c662a2b960c4d585daf9ae7b396031ecd786e7bb31b15d010ef")

    def url_for_version(self, version):
        url = (
            "https://sourceforge.net/projects/utfcpp/files/utf8cpp_2x/Release%20{0}/utf8_v{1}.zip"
        )
        return url.format(version, version.underscored)

    def install(self, spec, prefix):
        install_tree("doc", prefix.share.doc)
        install_tree("source", prefix.include)
