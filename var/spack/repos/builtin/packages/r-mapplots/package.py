# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMapplots(RPackage):
    """Data Visualisation on Maps.

    Create simple maps; add sub-plots like pie plots to a map or any other
    plot; format, plot and export gridded data. The package was developed for
    displaying fisheries data but most functions can be used for more generic
    data visualisation."""

    cran = "mapplots"

    license("GPL-2.0-or-later")

    version("1.5.2", sha256="ed0e151d6865549d1a10882984a7fb29bc89a7b94ad69e512f90937b981c8a18")
    version("1.5.1", sha256="37e96d34f37922180e07bb63b4514e07d42eee5bbf0885b278286ee48cf142a3")

    depends_on("r@2.10.0:", type=("build", "run"))
