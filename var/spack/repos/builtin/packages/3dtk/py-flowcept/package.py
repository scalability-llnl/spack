# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyFlowcept(PythonPackage):
    """Capture and query workflow provenance data using data observability."""

    homepage = "https://github.com/ORNL/flowcept"
    pypi = "flowcept/flowcept-0.6.11.tar.gz"

    maintainers("renan-souza", "mdorier")

    license("MIT", checked_by="mdorier")

    version("0.6.11", sha256="3a87c5f6835410a34b158efc9ab21ba686af26b609cff8beebc53bfb2a20c3dc")

    variant("kafka", default=False, description="Replace Redis with Kafka")
    variant("dask", default=False, description="Enable Dask support")

    depends_on("py-hatchling", type="build")
    with default_args(type=("build", "run")):
        depends_on("py-flask-restful")
        depends_on("py-msgpack")
        depends_on("py-omegaconf")
        depends_on("py-pandas")
        depends_on("py-psutil")
        depends_on("py-py-cpuinfo")
        depends_on("py-pymongo")
        depends_on("py-redis")
        depends_on("py-requests")
        depends_on("py-confluent-kafka", when="+kafka")
        depends_on("py-tomli", when="+dask")
        depends_on("py-dask@:2024.10.0+distributed", when="+dask")
