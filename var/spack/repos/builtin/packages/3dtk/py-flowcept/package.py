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
    depends_on("py-flask-restful", type=("build", "run"))
    depends_on("py-msgpack", type=("build", "run"))
    depends_on("py-omegaconf", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
    depends_on("py-py-cpuinfo", type=("build", "run"))
    depends_on("py-pymongo", type=("build", "run"))
    depends_on("py-redis", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-confluent-kafka", type=("build", "run"), when="+kafka")
    depends_on("py-tomli", type=("build", "run"), when="+dask")
    depends_on("py-dask@:2024.10.0+distributed", type=("build", "run"), when="+dask")
