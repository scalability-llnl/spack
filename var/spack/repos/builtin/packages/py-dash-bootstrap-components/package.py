# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDashBootstrapComponents(PythonPackage):
    """Bootstrap themed components for use in Plotly Dash"""

    homepage = "https://dash-bootstrap-components.opensource.faculty.ai/"
    pypi = "dash_bootstrap_components/dash_bootstrap_components-1.6.0.tar.gz"
    git = "https://github.com/facultyai/dash-bootstrap-components/"

    license("Apache-2.0")

    version("1.6.0", sha256="960a1ec9397574792f49a8241024fa3cecde0f5930c971a3fc81f016cbeb1095")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
