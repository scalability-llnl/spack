# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PkgA(Package):
    homepage = "http://www.example.com"
    has_code = False

    version("1.0")
    depends_on("pkg-b")
