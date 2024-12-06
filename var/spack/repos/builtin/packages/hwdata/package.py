# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hwdata(AutotoolsPackage):
    """Hardware identification and configuration data."""

    homepage = "https://github.com/vcrhonek/hwdata"
    url = "https://github.com/vcrhonek/hwdata/archive/v0.337.tar.gz"

    license("GPL-2.0-or-later OR XFree86-1.1")

    version("0.345", sha256="fafcc97421ba766e08a2714ccc3eebb0daabc99e67d53c2d682721dd01ccf7a7")
    version("0.340", sha256="e3a0ef18af6795a362345a2c2c7177be351cb27b4cc0ed9278b7409759258802")
