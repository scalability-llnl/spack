# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Mvapich2(Package):
    homepage = "http://www.homepage.org"
    url = "http://www.someurl"

    version("1.5", md5="9c5d5d4fe1e17dd12153f40bc5b6dbc0")

    variant(
        "file_systems",
        description="List of the ROMIO file systems to activate",
        values=auto_or_any_combination_of("lustre", "gpfs", "nfs", "ufs"),
    )
