# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAvroJsonSerializer(PythonPackage):
    """Serializes data into a JSON format using AVRO schema."""

    homepage = "https://github.com/linkedin/python-avro-json-serializer"
    pypi = "avro_json_serializer/avro_json_serializer-0.4.tar.gz"

    license("Apache-2.0")

    version("0.4", sha256="f9dac2dac92036c5dd5aba8c716545fc0a0630cc365a51ab15bc2ac47eac28f1")

    depends_on("py-setuptools", type="build")
    depends_on("py-simplejson", type=("build", "run"))
    depends_on("py-avro", type=("build", "run"))
