# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJupyterEvents(PythonPackage):
    """Jupyter Event System library."""

    homepage = "https://github.com/jupyter/jupyter_events"
    pypi = "jupyter_events/jupyter_events-0.6.3.tar.gz"

    version("0.10.0", sha256="670b8229d3cc882ec782144ed22e0d29e1c2d639263f92ca8383e66682845e22")
    version("0.6.3", sha256="9a6e9995f75d1b7146b436ea24d696ce3a35bfa8bfe45e0c33c334c79464d0b3")

    depends_on("py-hatchling@1.5:", type="build")

    depends_on("py-referencing", type=("build", "run"), when="@0.7:")
    depends_on("py-jsonschema+format-nongpl@4.18:", type=("build", "run"), when="@0.7:")
    depends_on("py-jsonschema+format-nongpl@3.2:", type=("build", "run"))
    depends_on("py-python-json-logger@2.0.4:", type=("build", "run"))
    depends_on("py-pyyaml@5.3:", type=("build", "run"))
    depends_on("py-traitlets@5.3:", type=("build", "run"))
    depends_on("py-rfc3339-validator", type=("build", "run"))
    depends_on("py-rfc3986-validator@0.1.1:", type=("build", "run"))
