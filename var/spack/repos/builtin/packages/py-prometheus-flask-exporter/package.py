# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPrometheusFlaskExporter(PythonPackage):
    """Prometheus metrics exporter for Flask."""

    homepage = "https://pypi.org/project/prometheus-flask-exporter/"
    pypi = "prometheus-flask-exporter/prometheus_flask_exporter-0.21.0.tar.gz"

    license("MIT")

    version("0.21.0", sha256="ebbc016c1e3d16e7cd39fe651a6c52ac68779858b2d5d1be6ddbc9e66f7fc29f")
    version("0.18.2", sha256="fc487e385d95cb5efd045d6a315c4ecf68c42661e7bfde0526af75ed3c4f8c1b")

    depends_on("py-setuptools", type="build")
    depends_on("py-prometheus-client", type=("build", "run"))
    depends_on("py-flask", type=("build", "run"))
