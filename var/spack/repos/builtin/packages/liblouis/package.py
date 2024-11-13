# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Liblouis(AutotoolsPackage):
    """Liblouis is an open-source braille translator and back-translator
    named in honor of Louis Braille."""

    homepage = "http://liblouis.org/"
    url = "https://github.com/liblouis/liblouis/releases/download/v3.15.0/liblouis-3.15.0.tar.gz"

    license("GPL-3.0-or-later")

    version("3.25.0", sha256="d720aa5fcd51de925a28ae801b8b2ca76ee67e2360b40055c679bce8e565f251")
    version("3.17.0", sha256="78c71476467850935d145010c8fcb26b513df1843505b3eb4c41888541a0113d")
    version("3.15.0", sha256="3a381b132b140747e5fcd47354da6cf43959da2167f8bc598430bbac51224467")
    version("3.14.0", sha256="f5b25f8059dd76595aeb419b1522dda78f281a75a7c56dceaaa443f8c437306a")
    version("3.13.0", sha256="2803b89a2bff9f02032125fa7b7d0a204a60d8d14f232242344b5f09535e9a01")
    version("3.12.0", sha256="87d9bad6d75916270bad14bb22fa5f487c7edee4774878c04bef82833bc9467d")
    version("3.11.0", sha256="b802aba0bff49636907ca748225e21c56ecf3f3ebc143d582430036d4d9f6259")

    depends_on("c", type="build")  # generated
