# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyApacheBeam(PythonPackage):
    """Apache Beam is a unified programming model for Batch and Streaming."""

    homepage = "https://github.com/apache/beam"
    pypi = "apache-beam/apache-beam-2.24.0.zip"

    version("2.24.0", sha256="55c50b1a964bacc840a5e4cc3b4a42c4ef09d12192d215ba3cad65d4d22e09dd")

    depends_on("python@2.7,3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pip@7.0.0:", type="build")
    depends_on("py-cython@0.28.1:", type="build")
    depends_on("py-avro-python3@1.8.1:1.9.1,1.9.3:1.9", type=("build", "run"))
    depends_on("py-crcmod@1.7:1", type=("build", "run"))
    depends_on("py-dill@0.3.1:0.3.1", type=("build", "run"))
    depends_on("py-fastavro@0.21.4:0.23", type=("build", "run"))
    depends_on("py-future@0.18.2:0", type=("build", "run"))
    depends_on("py-grpcio@1.29:1", type=("build", "run"))
    depends_on("py-hdfs@2.1:2", type=("build", "run"))
    depends_on("py-httplib2@0.8:0.17", type=("build", "run"))
    depends_on("py-mock@1.0.1:2", type=("build", "run"))
    depends_on("py-numpy@1.14.3:1", type=("build", "run"))
    depends_on("py-pymongo@3.8:3", type=("build", "run"))
    depends_on("py-oauth2client@2.0.1:3", type=("build", "run"))
    depends_on("py-protobuf@3.12.2:3", type=("build", "run"))
    depends_on("py-pyarrow@0.15.1:0.17", type=("build", "run"))
    depends_on("py-pydot@1.2.0:1", type=("build", "run"))
    depends_on("py-python-dateutil@2.8:2", type=("build", "run"))
    depends_on("py-pytz@2018.3:", type=("build", "run"))
    depends_on("py-requests@2.24:2", type=("build", "run"))
    depends_on("py-typing-extensions@3.7.0:3.7", type=("build", "run"))
