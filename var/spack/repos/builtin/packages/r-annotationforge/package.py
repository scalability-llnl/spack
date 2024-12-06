# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAnnotationforge(RPackage):
    """Tools for building SQLite-based annotation data packages.

    Provides code for generating Annotation packages and their databases.
    Packages produced are intended to be used with AnnotationDbi."""

    bioc = "AnnotationForge"

    version("1.42.0", commit="2eac005012b11317c33c8b0062b968b2ac378308")
    version("1.40.0", commit="f77d3a942eb6b18c18888b7af3f0e652596cf19f")
    version("1.38.1", commit="2dcedf353bc57bf80818e6adb1f7129c21886f6b")
    version("1.38.0", commit="1f77750562ea3a01f0f1a46c299184fc31196ffd")
    version("1.36.0", commit="523b5f0c3ffb77e59e1568e5f36a5a470bfeeae5")
    version("1.32.0", commit="3d17c2a945951c02fe152e5a8a8e9c6cb41e30f7")
    version("1.26.0", commit="5d181f32df1fff6446af64a2538a7d25c23fe46e")
    version("1.24.0", commit="3e1fe863573e5b0f69f35a9ad6aebce11ef83d0d")
    version("1.22.2", commit="8eafb1690c1c02f6291ccbb38ac633d54b8217f8")
    version("1.20.0", commit="7b440f1570cb90acce8fe2fa8d3b5ac34f638882")
    version("1.18.2", commit="44ca3d4ef9e9825c14725ffdbbaa57ea059532e1")

    depends_on("r@2.7.0:", type=("build", "run"))
    depends_on("r-biocgenerics@0.15.10:", type=("build", "run"))
    depends_on("r-biobase@1.17.0:", type=("build", "run"))
    depends_on("r-annotationdbi@1.33.14:", type=("build", "run"))
    depends_on("r-dbi", type=("build", "run"))
    depends_on("r-rsqlite", type=("build", "run"))
    depends_on("r-xml", type=("build", "run"))
    depends_on("r-s4vectors", type=("build", "run"))
    depends_on("r-rcurl", type=("build", "run"))
