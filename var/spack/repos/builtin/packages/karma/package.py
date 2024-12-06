# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Karma(Package):
    """Karma is a toolkit for interprocess communications, authentication,
    encryption, graphics display, user interface and manipulating the Karma
    network data structure. It contains KarmaLib (the structured libraries
    and API) and a large number of modules (applications)
    to perform many standard tasks."""

    homepage = "https://www.atnf.csiro.au/computing/software/karma/"
    url = "ftp://ftp.atnf.csiro.au/pub/software/karma/karma-1.7.25-common.tar.bz2"

    version(
        "1.7.25-common", sha256="afda682d79c0923df5a6c447a32b09294da1582933abae3205c008104da54fbd"
    )

    depends_on("libx11", type=("build", "run"))
    depends_on("libxaw", type=("build", "run"))

    resource(
        name="karma-linux",
        url="ftp://ftp.atnf.csiro.au/pub/software/karma/karma-1.7.25-amd64_Linux_libc6.3.tar.bz2",
        sha256="effc3ed61c28b966b357147d90357d03c22d743c6af6edb49a863c6eb625a441",
        destination="./",
    )

    def install(self, spec, prefix):
        install_tree("./karma-1.7.25/amd64_Linux_libc6.3/bin", prefix.bin)
        install_tree("./karma-1.7.25/amd64_Linux_libc6.3/lib", prefix.lib)
