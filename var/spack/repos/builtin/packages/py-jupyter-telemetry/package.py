# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJupyterTelemetry(PythonPackage):
    """Jupyter Telemetry enables Jupyter Applications to record events and transmit"""

    """ them to destinations as structured data"""

    pypi = "jupyter-telemetry/jupyter_telemetry-0.1.0.tar.gz"

    license("BSD-3-Clause")

    version("0.1.0", sha256="445c613ae3df70d255fe3de202f936bba8b77b4055c43207edf22468ac875314")
    version("0.0.5", sha256="d3eaac14be17510a4d288f3737580107ce14eef543e6133d56654d3f0e742b9b")

    depends_on("py-python-json-logger", type=("build", "run"))
    depends_on("py-jsonschema", type=("build", "run"))
    depends_on("py-ruamel-yaml", type=("build", "run"))
    depends_on("py-setuptools", type=("build"))
    depends_on("py-traitlets", type=("build", "run"))
    depends_on("python@3.5:", type=("build", "run"))
