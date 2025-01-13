# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSvglite(RPackage):
    """An 'SVG' Graphics Device.

    A graphics device for R that produces 'Scalable Vector Graphics'. 'svglite'
    is a fork of the older 'RSvgDevice' package."""

    cran = "svglite"

    license("GPL-2.0-or-later")

    version("2.1.3", sha256="f0a8564e6f9127f4d1e05cf5a5f36b4e244aee0008e27473e504c63873ef0a54")
    version("2.1.1", sha256="48700169eec1b05dbee9e2bae000aa84c544617b018cb3ac431a128cfd8dac56")
    version("2.1.0", sha256="ad40f590c7e80ae83001a3826b6e8394ba733446ed51fd55faeda974ab839c9b")
    version("2.0.0", sha256="76e625fe172a5b7ce99a67b6d631b037b3f7f0021cfe15f2e15e8851b89defa5")

    depends_on("r+X", type=("build", "run"))
    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@2.1.2:")
    depends_on("r-systemfonts@1.0.0:", type=("build", "run"))
    depends_on("r-cpp11", type=("build", "run"))
    depends_on("libpng")
