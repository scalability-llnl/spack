# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Libgtop(AutotoolsPackage):
    """Contains the GNOME top libraries for collecting system monitoring data"""

    homepage = "https://gitlab.gnome.org/GNOME/libgtop"
    url = "https://download.gnome.org/sources/libgtop/2.41/libgtop-2.41.3.tar.xz"

    maintainers("teaguesterling")

    license("GPLv2", checked_by="teaguesterling")

    version("2.41.2", sha256="d9026cd8a48d27cdffd332f8d60a92764b56424e522c420cd13a01f40daf92c3")
    version("2.41.1", sha256="43ea9ad13f7caf98303e64172b191be9b96bab340b019deeec72251ee140fe3b")

    depends_on("c", type="build")  # generated

    depends_on("pkgconfig", type="build")
    with default_args(type=("build", "link", "run")):
        depends_on("glib@2.65:", when="@2.40:")
        depends_on("gettext@:0.19", when="@:2.40.0")
