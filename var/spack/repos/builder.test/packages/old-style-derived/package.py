# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.pkg.builder.test.old_style_autotools
from spack.package import *


class OldStyleDerived(spack.pkg.builder.test.old_style_autotools.OldStyleAutotools):
    """Package used to verify that old-style packages work correctly when executing the
    installation procedure.
    """

    homepage = "http://www.example.com"
    url = "http://www.example.com/a-1.0.tar.gz"

    version("2.0", md5="abcdef0123456789abcdef0123456789")
    version("1.0", md5="0123456789abcdef0123456789abcdef")

    def configure_args(self):
        return ["--with-bar"] + super().configure_args()
