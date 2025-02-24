# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RE1071(RPackage):
    """Misc Functions of the Department of Statistics, Probability Theory Group
    (Formerly: E1071), TU Wien.

    Functions for latent class analysis, short time Fourier transform, fuzzy
    clustering, support vector machines, shortest path computation, bagged
    clustering, naive Bayes classifier, generalized k-nearest neighbour ..."""

    cran = "e1071"

    license("GPL-2.0-only OR GPL-3.0-only")

    version("1.7-14", sha256="754d97ab073acc07b909a190f87f021e31e07269c8632c53166a6c2843e65195")
    version("1.7-13", sha256="da94e191af6e69aa0f9e3250d4b823674cc869339d914f761ebf2824177b6b2f")
    version("1.7-12", sha256="91e052d0a521db74a66df90adb28db601f2a2cca38b03dcad030ac2fdc5c5dcf")
    version("1.7-11", sha256="48c18e10e7cabc742d37b563672e2eddb6061f2378b69e5563be79ab9948d92f")
    version("1.7-9", sha256="9bf9a15e7ce0b9b1a57ce3048d29cbea7f2a5bb2e91271b1b6aaafe07c852226")
    version("1.7-4", sha256="e6ab871b06f500dc65f8f781cc7253f43179698784c06dab040b4aa6592f2309")
    version("1.7-2", sha256="721c299ce83047312acfa3e0c4b3d4c223d84a4c53400c73465cca2c92913752")
    version("1.7-1", sha256="5c5f04a51c1cd2c7dbdf69987adef9bc07116804c63992cd36d804a1daf89dfe")
    version("1.6-7", sha256="7048fbc0ac17d7e3420fe68081d0e0a2176b1154ee3191d53558ea9724c7c980")

    depends_on("r-class", type=("build", "run"))
    depends_on("r-proxy", type=("build", "run"), when="@1.7-9:")
