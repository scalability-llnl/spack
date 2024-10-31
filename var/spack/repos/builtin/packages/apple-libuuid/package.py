# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AppleLibuuid(BundlePackage):
    """Placeholder package for Apple's analogue to non-GNU libuuid"""

    homepage = "https://opensource.apple.com/tarballs/Libsystem/"

    version("1353.100.2")

    provides("uuid")

    # Only supported on 'platform=darwin'
    conflicts("platform=linux")
    conflicts("platform=windows")

    @property
    def headers(self):
        return HeaderList(
            join_path(self.prefix, "System/Library/Frameworks/Kernel.framework/Headers")
        )

    @property
    def libs(self):
        return LibraryList(join_path(self.prefix, "System/Library/Frameworks/Kernel.framework"))
