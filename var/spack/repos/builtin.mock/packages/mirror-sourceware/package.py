# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MirrorSourceware(AutotoolsPackage, SourcewarePackage):
    """Simple sourceware.org package"""

    homepage = "https://sourceware.org/bzip2/"
    sourceware_mirror_path = "bzip2/bzip2-1.0.8.tar.gz"

    version("1.0.8", sha256="ab5a03176ee106d3f0fa90e381da478ddae405918153cca248e682cd0c4a2269")
