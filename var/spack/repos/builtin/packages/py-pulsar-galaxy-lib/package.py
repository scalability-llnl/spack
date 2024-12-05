# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPulsarGalaxyLib(PythonPackage):
    """Distributed job execution application built for Galaxy (http://galaxyproject.org/)."""

    homepage = "https://github.com/galaxyproject/pulsar"
    pypi = "pulsar-galaxy-lib/pulsar-galaxy-lib-0.14.16.tar.gz"

    license("Apache-2.0")

    version("0.14.16", sha256="f3330350d2e85c7228cebf83f74fc4c0cc5e8e7557bb6e5ae55f5556d7e6fbff")

    depends_on("py-setuptools", type="build")

    depends_on("py-galaxy-job-metrics@19.9.0:", type=("build", "run"))
    depends_on("py-galaxy-objectstore@19.9.0:", type=("build", "run"))
    depends_on("py-galaxy-tool-util@19.9.0:", type=("build", "run"))
    depends_on("py-galaxy-util@19.9.0:", type=("build", "run"))
    depends_on("py-webob", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
    depends_on("py-pastedeploy", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-paramiko", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"))
