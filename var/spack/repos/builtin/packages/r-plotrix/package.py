# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPlotrix(RPackage):
    """Various Plotting Functions.

    Lots of plots, various labeling, axis and color scaling functions."""

    cran = "plotrix"

    license("GPL-2.0-or-later")

    version("3.8-4", sha256="e6a22d93ab61c67af21cbbe1fe333c06934cf576a44745bf2beee59bceaae8d6")
    version("3.8-2", sha256="bb72953102889cea41cd6521874e35d2458ebd10aab97ba6f262e102cac0bc1f")
    version("3.7-8", sha256="8ccd1f7e656413b9956cea614c986ce9cc61366deba356afb38cee6672a59480")
    version("3.7-6", sha256="83d5f7574592953288b4fe39c4c0dd7670d097598ad7f6bddbb0687a32954e46")
    version("3.7-5", sha256="b22f3f9d93961d23ad46e41597d1e45d2665ced04dcad8c40f6806a67cded14c")
    version("3.6-4", sha256="883b7d0a00c1b2b418f9167c72ed9e86eca3c9865d34158a7a6ad0b9bf95bff3")
    version("3.6-3", sha256="217164bdd04405c3280a0c8b2691f289287f9851fa8248648a5ae38f54962741")

    depends_on("r@3.5.0:", type=("build", "run"), when="@3.7-6:")
