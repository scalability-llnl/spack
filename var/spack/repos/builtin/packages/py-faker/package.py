# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFaker(PythonPackage):
    """Faker is a Python package that generates fake data for
    you. Whether you need to bootstrap your database, create
    good-looking XML documents, fill-in your persistence to
    stress test it, or anonymize data taken from a production
    service, Faker is for you."""

    homepage = "https://github.com/joke2k/faker"
    pypi = "Faker/Faker-9.8.2.tar.gz"

    license("MIT")

    version("9.8.2", sha256="393bd1b5becf3ccbc04a4f0f13da7e437914b24cafd1a4d8b71b5fecff54fb34")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-python-dateutil@2.4:", type=("build", "run"))
    depends_on("py-text-unidecode@1.3", type=("build", "run"))
    depends_on("py-typing-extensions@3.10.0.2:", type=("build", "run"), when="^python@:3.8")
