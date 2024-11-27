# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySlurmPipeline(PythonPackage):
    """A Python class for scheduling SLURM jobs"""

    homepage = "https://github.com/acorg/slurm-pipeline"
    pypi = "slurm-pipeline/slurm-pipeline-1.1.13.tar.gz"

    license("MIT")

    version("4.0.4", sha256="5496e46edb890ef745231b4d05b8dfd194374b3fe2c6b33da43cda9685f145c8")
    version("3.0.2", sha256="28e07eb93e846b395a16e6778fd3fc8344a82d115a6a8420276ec68f67f7131c")
    version("2.0.9", sha256="2360e43965ecfa3701f287b7d597c99b4accd4dc8faf9d55cfdcc2228c4054cc")
    version("1.1.13", sha256="6d6ca2e96a16780fd9520957166afd06272c57abd962e76bfe74c4d394b38da1")

    depends_on("py-setuptools", type="build")
    # listed in install_requires:
    depends_on("py-pytest@6.2.2:", type="build")
    # Before 4.0.0, slurm_pipeline/base.py has: from six import string_types
    depends_on("py-six@1.10.0:", type=("build", "run"), when="@:3")
