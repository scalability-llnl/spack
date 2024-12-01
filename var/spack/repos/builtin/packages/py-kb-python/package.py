# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyKbPython(PythonPackage):
    """Python wrapper around kallisto | bustools for scRNA-seq analysis."""

    homepage = "https://github.com/pachterlab/kb_python"
    pypi = "kb_python/kb_python-0.27.3.tar.gz"

    license("BSD-2-Clause")

    version("0.27.3", sha256="dc98f6ceb4402d666b7e0d19be17c63d33e8b710a35cdc33de7c0f457122f43f")

    depends_on("python@3.6:", type=("build", "run"))

    depends_on("py-setuptools", type="build")

    depends_on("py-anndata@0.6.22.post1:", type=("build", "run"))
    depends_on("py-h5py@2.10.0:", type=("build", "run"))
    depends_on("py-jinja2@2.10.2:", type=("build", "run"))
    depends_on("py-loompy@3.0.6:", type=("build", "run"))
    depends_on("py-nbconvert@5.6.0:", type=("build", "run"))
    depends_on("py-nbformat@4.4.0:", type=("build", "run"))
    depends_on("py-ngs-tools@1.7.3:", type=("build", "run"))
    depends_on("py-numpy@1.17.2:", type=("build", "run"))
    depends_on("py-pandas@1.0.0:", type=("build", "run"))
    depends_on("py-plotly@4.5.0:", type=("build", "run"))
    depends_on("py-requests@2.22.0:", type=("build", "run"))
    depends_on("py-scanpy@1.4.4.post1:", type=("build", "run"))
    depends_on("py-scikit-learn@0.21.3:", type=("build", "run"))
    depends_on("py-typing-extensions@3.7.4:", type=("build", "run"))
