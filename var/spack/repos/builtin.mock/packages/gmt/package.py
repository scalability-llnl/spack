# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Gmt(Package):
    url = "http://www.example.com/"
    url = "http://www.example.com/2.0.tar.gz"

    version("2.0", md5="abcdef1234567890abcdef1234567890")
    version("1.0", md5="abcdef1234567890abcdef1234567890")

    depends_on("mvdefaults", when="@1.0")
