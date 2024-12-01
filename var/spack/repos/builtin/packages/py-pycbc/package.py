# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPycbc(PythonPackage):
    """PyCBC is a software package used to explore astrophysical sources of
    gravitational waves. It contains algorithms to analyze gravitational-wave
    data from the LIGO and Virgo detectors, detect coalescing compact binaries,
    and measure the astrophysical parameters of detected sources. PyCBC was
    used in the first direct detection of gravitational waves and is used in
    the flagship analysis of LIGO and Virgo data."""

    homepage = "https://pycbc.org/"
    pypi = "PyCBC/PyCBC-1.14.1.tar.gz"

    license("GPL-3.0-or-later")

    version("1.14.1", sha256="4b0a309cb6209837aaebbd691413a286dd7200ccf4b977ffed1462a65ac35dc0")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.13.0:", type=("build", "run"))
    depends_on("py-mako@1.0.1:", type=("build", "run"))
    depends_on("py-cython", type="build")
    depends_on("py-decorator@3.4.2:", type=("build", "run"))
    depends_on("py-scipy@0.16.0:", type=("build", "run"))
    depends_on("py-matplotlib@1.5.1:", type=("build", "run"))
    depends_on("pil", type=("build", "run"))
    depends_on("py-h5py@2.5:", type=("build", "run"))
    depends_on("py-jinja2", type=("build", "run"))
    depends_on("py-astropy@2.0.3:", type=("build", "run"))
    depends_on("py-mpld3@0.3:", type=("build", "run"))
    depends_on("py-lscsoft-glue@1.59.3:", type=("build", "run"))
    depends_on("py-emcee@2.2.1", type=("build", "run"))
    depends_on("py-requests@1.2.1:", type=("build", "run"))
    depends_on("py-beautifulsoup4@4.6.0:", type=("build", "run"))
    depends_on("py-six@1.10.0:", type=("build", "run"))
    depends_on("py-ligo-segments", type=("build", "run"))

    patch("for_aarch64.patch", when="@:1.14.1 target=aarch64:")
