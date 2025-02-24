# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlaskCompress(PythonPackage):
    """Flask-Compress allows you to easily compress your Flask application's
    responses with gzip."""

    homepage = "https://github.com/libwilliam/flask-compress"
    pypi = "Flask-Compress/Flask-Compress-1.4.0.tar.gz"

    license("MIT")

    version("1.14", sha256="e46528f37b91857012be38e24e65db1a248662c3dc32ee7808b5986bf1d123ee")
    version("1.4.0", sha256="468693f4ddd11ac6a41bca4eb5f94b071b763256d54136f77957cfee635badb3")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@0.42:", type="build", when="@1.10:")
    depends_on("py-setuptools-scm@3.4: +toml", type="build", when="@1.10:")
    depends_on("py-flask@0.9:", type=("build", "run"))
    depends_on("py-brotli", type="run", when="@1.5:")
