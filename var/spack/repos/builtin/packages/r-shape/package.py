# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RShape(RPackage):
    """Functions for Plotting Graphical Shapes, Colors.

    Functions for plotting graphical shapes such as ellipses, circles,
    cylinders, arrows, ..."""

    cran = "shape"

    license("GPL-3.0-or-later")

    version("1.4.6.1", sha256="43f9bd0f997fd6cf1838efd8b2509c9a6396513f4e54a20360481634affd22a4")
    version("1.4.6", sha256="b9103e5ed05c223c8147dbe3b87a0d73184697343634a353a2ae722f7ace0b7b")
    version("1.4.5", sha256="094a79b8f42226189227fd7af71868e42106caa25a4d7f80a26977e8bc84189f")
    version("1.4.4", sha256="f4cb1b7d7c84cf08d2fa97f712ea7eb53ed5fa16e5c7293b820bceabea984d41")
    version("1.4.3", sha256="720f6ca9c70a39a3900af9d074bff864b18ac58013b21d48b779047481b93ded")
    version("1.4.2", sha256="c6c08ba9cc2e90e5c9d3d5223529b57061a041f637886ad7665b9fa27465637a")

    depends_on("r@2.1:", type=("build", "run"))
