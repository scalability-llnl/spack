# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMultiqc(PythonPackage):
    """MultiQC is a tool to aggregate bioinformatics results across many
    samples into a single report. It is written in Python and contains modules
    for a large number of common bioinformatics tools."""

    homepage = "https://multiqc.info"
    pypi = "multiqc/multiqc-1.0.tar.gz"

    license("GPL-3.0-only", checked_by="A_N_Other")
    maintainers("ewels", "vladsavelyev")

    version("1.23", sha256="4e84664000fec69a0952a0457a8d780dcc1ce9e36d14680dbdba5610b9766265")

    # dependency defintions move from setup.py to pyproject.toml as of @1.23:

    # build deps
    depends_on("py-setuptools", type="build")

    # current run deps
    depends_on("py-click", type=("build", "run"))
    depends_on("py-humanize", type=("build", "run"), when="@1.18:")
    depends_on("py-importlib-metadata", type=("build", "run"), when="@1.16:")
    depends_on("py-jinja2@3.0.0:", type=("build", "run"), when="@1.14:")
    depends_on("py-jinja2@2.9:", type=("build", "run"), when="@:1.13")
    depends_on("py-kaleido", type=("build", "run"), when="@1.20:")
    depends_on("py-markdown", type=("build", "run"), when="@1.3:")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"), when="@1.16:")
    depends_on("py-requests", type=("build", "run"), when="@1.3:")
    depends_on("py-pillow@10:", type=("build", "run"), when="@1.20:")
    depends_on("py-plotly@5.18:", type=("build", "run"), when="@1.21:")
    depends_on("py-plotly", type=("build", "run"), when="@1.20")
    depends_on("py-pyyaml@4:", type=("build", "run"), when="@1.13:")
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-pyaml-env", type=("build", "run"), when="@1.18:")
    depends_on("py-rich@10:", type=("build", "run"), when="@1.13:")
    depends_on("py-rich-click", type=("build", "run"), when="@1.13:")
    depends_on("py-coloredlogs", type=("build", "run"), when="@1.13:")
    depends_on("py-spectra@0.0.10:", type=("build", "run"), when="@1.4:")
    depends_on("py-spectra", type=("build", "run"), when="@1.18:")
    depends_on("py-typeguard", type=("build", "run"), when="@1.23:")
    depends_on("py-tqdm", type=("build", "run"), when="@1.23:")
