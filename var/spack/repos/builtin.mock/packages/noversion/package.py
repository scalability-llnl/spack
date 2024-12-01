# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Noversion(Package):
    """
    Simple package with no version, which should be rejected since a version
    is required.
    """

    homepage = "http://www.example.com"
    url = "http://www.example.com/a-1.0.tar.gz"

    def install(self, spec, prefix):
        touch(join_path(prefix, "an_installation_file"))
