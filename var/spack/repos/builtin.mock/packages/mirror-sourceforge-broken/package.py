# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MirrorSourceforgeBroken(AutotoolsPackage, SourceforgePackage):
    """Simple sourceforge.net package"""

    homepage = "http://www.tcl.tk"
    url = "http://prdownloads.sourceforge.net/tcl/tcl8.6.5-src.tar.gz"

    version("8.6.8", sha256="c43cb0c1518ce42b00e7c8f6eaddd5195c53a98f94adc717234a65cbcfd3f96a")
