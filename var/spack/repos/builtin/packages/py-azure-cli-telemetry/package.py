# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureCliTelemetry(PythonPackage):
    """Microsoft Azure CLI Telemetry Package."""

    homepage = "https://github.com/Azure/azure-cli"
    pypi = "azure-cli-telemetry/azure-cli-telemetry-1.0.4.tar.gz"

    license("MIT")

    version("1.0.4", sha256="1f239d544d309c29e827982cc20113eb57037dba16db6cdd2e0283e437e0e577")

    depends_on("py-setuptools", type="build")
    depends_on("py-applicationinsights@0.11.1:0.11", type=("build", "run"))
    depends_on("py-portalocker@1.2:1", type=("build", "run"))
