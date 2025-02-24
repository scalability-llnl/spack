# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MirrorSourceforge(AutotoolsPackage, SourceforgePackage):
    """Simple sourceforge.net package"""

    homepage = "http://www.tcl.tk"
    sourceforge_mirror_path = "tcl/tcl8.6.5-src.tar.gz"

    version("8.6.8", sha256="c43cb0c1518ce42b00e7c8f6eaddd5195c53a98f94adc717234a65cbcfd3f96a")
