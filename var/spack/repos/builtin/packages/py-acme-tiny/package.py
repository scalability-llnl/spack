# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAcmeTiny(PythonPackage):
    """A tiny script to issue and renew TLS certs from Let's Encrypt."""

    homepage = "https://github.com/diafygi/acme-tiny"
    git = "https://github.com/diafygi/acme-tiny.git"

    license("MIT")

    version("master", branch="master")
    version("4.0.4", commit="5350420d35177eda733d85096433a24e55f8d00e")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-setuptools-scm", type="build")
