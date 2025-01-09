# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMultitaper(RPackage):
    """Spectral Analysis Tools using the Multitaper Method.

    Implements multitaper spectral analysis using discrete prolate spheroidal
    sequences (Slepians) and sine tapers. It includes an adaptive weighted
    multitaper spectral estimate, a coherence estimate, Thomson's Harmonic
    F-test, and complex demodulation. The Slepians sequences are generated
    efficiently using a tridiagonal matrix solution, and jackknifed confidence
    intervals are available for most estimates. This package is an
    implementation of the method described in D.J. Thomson (1982) "Spectrum
    estimation and harmonic analysis" <doi:10.1109/PROC.1982.12433>."""

    cran = "multitaper"

    license("GPL-2.0-or-later")

    version("1.0-17", sha256="3430ca62be2ee491d29b05e461647327a8977743241af2d3c39277c920170af3")
    version("1.0-15", sha256="837d71f3b46fbce2bea210449cf75e609f5363ff23b7808f5f115fdc51e6a3be")
    version("1.0-14", sha256="c84c122541dc2874131446e23b212259b3b00590d701efee49e6740fd74a8d13")

    depends_on("r@3.0:", type=("build", "run"))
