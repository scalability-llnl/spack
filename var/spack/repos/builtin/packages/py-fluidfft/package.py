# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFluidfft(PythonPackage):
    """Efficient and easy Fast Fourier Transform (FFT) for Python."""

    pypi = "fluidfft/fluidfft-0.4.2.tar.gz"

    maintainers("paugier")

    license("CECILL-B", checked_by="paugier")

    version("0.4.2", sha256="5e35f1fb647da2fa65c116bb0d598fc9cb975cd95c41022644c27dc726c36073")
    version("0.4.1", sha256="b17e64c7b2be47c61d6ac7b713e0e8992cf900d2367381288c93a56090e6c0c1")

    variant("native", default=False, description="Compile with -march=native and -Ofast.")

    with default_args(type=("build", "run")):
        depends_on("python@3.9:")
        depends_on("py-transonic@0.6.4:")

    with default_args(type="build"):
        depends_on("py-meson-python")
        depends_on("py-pythran@0.9.7:")

    with default_args(type="run"):
        depends_on("py-fluiddyn@0.2.3:")
        depends_on("py-pyfftw@0.10.4:")
        depends_on("py-importlib_metadata", when="^python@:3.10")

    def config_settings(self, spec, prefix):
        settings = {"setup-args": {"-Dnative": spec.variants["native"].value}}
        return settings
