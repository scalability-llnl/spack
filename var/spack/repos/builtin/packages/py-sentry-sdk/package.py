# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySentrySdk(PythonPackage):
    """The new Python SDK for Sentry.io"""

    homepage = "https://github.com/getsentry/sentry-python"
    pypi = "sentry-sdk/sentry-sdk-0.17.6.tar.gz"

    license("MIT")

    version("1.5.5", sha256="98fd155fa5d5fec1dbabed32a1a4ae2705f1edaa5dae4e7f7b62a384ba30e759")
    version("0.17.6", sha256="1a086486ff9da15791f294f6e9915eb3747d161ef64dee2d038a4d0b4a369b24")

    variant("flask", default=False, description="Builts with flask")
    variant("quart", default=False, when="@1.5.5:", description="Builts with quart")
    variant("bottle", default=False, description="Builts with bottle")
    variant("falcon", default=False, description="Builts with falcon")
    variant("django", default=False, description="Builts with django")
    variant("sanic", default=False, description="Builts with sanic")
    variant("celery", default=False, description="Builts with celery")
    variant("beam", default=False, description="Builts with beam")
    variant("rq", default=False, description="Builts with rq")
    variant("aiohttp", default=False, description="Builts with aiohttp")
    variant("tornado", default=False, description="Builts with tornado")
    variant("sqlalchemy", default=False, description="Builts with sqlalchemy")
    variant("pyspark", default=False, description="Builts with pyspark")
    variant("pure_eval", default=False, description="Builts with pure_eval")
    variant("chalice", default=False, description="Builts with chalice")
    variant("httpx", default=False, when="@1.5.5:", description="Builts with httpx")

    depends_on("python@2.7,3.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-urllib3@1.10.0:", type=("build", "run"))
    depends_on("py-certifi", type=("build", "run"))

    depends_on("py-flask@0.11:", type=("build", "run"), when="+flask")
    depends_on("py-blinker@1.1:", type=("build", "run"), when="+flask")
    depends_on("py-quart@0.16.1:", type=("build", "run"), when="+quart")
    depends_on("py-blinker@1.1:", type=("build", "run"), when="+quart")
    depends_on("py-bottle@0.12.13:", type=("build", "run"), when="+bottle")
    depends_on("py-falcon@1.4:", type=("build", "run"), when="+falcon")
    depends_on("py-django@1.8:", type=("build", "run"), when="+django")
    depends_on("py-sanic@0.8:", type=("build", "run"), when="+sanic")
    depends_on("py-celery@3:", type=("build", "run"), when="+celery")
    depends_on("py-apache-beam@2.12:", type=("build", "run"), when="+beam")
    depends_on("py-rq@0.6:", type=("build", "run"), when="+rq")
    depends_on("py-aiohttp@3.5:", type=("build", "run"), when="+aiohttp")
    depends_on("py-tornado@5:", type=("build", "run"), when="+tornado")
    depends_on("py-sqlalchemy@1.2:", type=("build", "run"), when="+sqlalchemy")
    depends_on("py-pyspark@2.4.4:", type=("build", "run"), when="+pyspark")
    depends_on("py-pure-eval", type=("build", "run"), when="+pure_eval")
    depends_on("py-executing", type=("build", "run"), when="+pure_eval")
    depends_on("py-asttokens", type=("build", "run"), when="+pure_eval")
    depends_on("py-chalice@1.16.0:", type=("build", "run"), when="+chalice")
    depends_on("py-httpx@0.16.0:", type=("build", "run"), when="+httpx")
