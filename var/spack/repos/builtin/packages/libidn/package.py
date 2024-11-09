# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libidn(AutotoolsPackage, GNUMirrorPackage):
    """GNU Libidn is a fully documented implementation of the Stringprep,
    Punycode and IDNA 2003 specifications. Libidn's purpose is to
    encode and decode internationalized domain names."""

    homepage = "https://www.gnu.org/software/libidn/"
    gnu_mirror_path = "libidn/libidn-1.42.tar.gz"

    maintainers("snehring")

    license("LGPL-2.1-or-later", checked_by="snehring")

    version("1.42", sha256="d6c199dcd806e4fe279360cb4b08349a0d39560ed548ffd1ccadda8cdecb4723")
    version("1.38", sha256="de00b840f757cd3bb14dd9a20d5936473235ddcba06d4bc2da804654b8bbf0f6")
    version("1.34", sha256="3719e2975f2fb28605df3479c380af2cf4ab4e919e1506527e4c7670afff6e3c")
    version("1.28", sha256="dd357a968449abc97c7e5fa088a4a384de57cb36564f9d4e0d898ecc6373abfb")

    depends_on("c", type="build")  # generated
