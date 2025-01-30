# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlaskCors(PythonPackage):
    """A Flask extension for handling Cross Origin Resource Sharing (CORS),
    making cross-origin AJAX possible.
    """

    homepage = "https://flask-cors.corydolphin.com/en/latest/index.html"
    pypi = "Flask-Cors/Flask-Cors-3.0.10.tar.gz"

    license("MIT")

    version("4.0.0", sha256="f268522fcb2f73e2ecdde1ef45e2fd5c71cc48fe03cffb4b441c6d1b40684eb0")
    version("3.0.10", sha256="b60839393f3b84a0f3746f6cdca56c1ad7426aa738b70d6c61375857823181de")

    depends_on("py-setuptools", type="build")
    depends_on("py-flask@0.9:", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
