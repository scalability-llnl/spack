# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from os.path import split

from spack.package import *
from spack.util.environment import EnvironmentModifications


class Miniconda2(Package):
    """The minimalist bootstrap toolset for conda and Python2."""

    homepage = "https://conda.io/miniconda.html"
    url = "https://repo.continuum.io/miniconda/Miniconda2-4.6.14-Linux-x86_64.sh"

    version(
        "4.7.12.1",
        sha256="383fe7b6c2574e425eee3c65533a5101e68a2d525e66356844a80aa02a556695",
        expand=False,
        deprecated=True,
    )
    version(
        "4.6.14",
        sha256="3e20425afa1a2a4c45ee30bd168b90ca30a3fdf8598b61cb68432886aadc6f4d",
        expand=False,
        deprecated=True,
    )
    version(
        "4.5.11",
        sha256="0e23e8d0a1a14445f78960a66b363b464b889ee3b0e3f275b7ffb836df1cb0c6",
        expand=False,
        deprecated=True,
    )
    version(
        "4.5.4",
        sha256="77d95c99996495b9e44db3c3b7d7981143d32d5e9a58709c51d35bf695fda67d",
        expand=False,
        deprecated=True,
    )
    version(
        "4.3.30",
        sha256="0891000ca28359e63aa77e613c01f7a88855dedfc0ddc8be31829f3139318cf3",
        expand=False,
        deprecated=True,
    )
    version(
        "4.3.14",
        sha256="2dc629843be954fc747f08ffbcb973b5473f6818464b82a00260c38f687e02f1",
        expand=False,
        deprecated=True,
    )
    version(
        "4.3.11",
        sha256="fbc77646cc62e39f4aa5dd1dda1c94cc4e0bc3be580b10aa2ca2ae0013456a87",
        expand=False,
        deprecated=True,
    )

    def install(self, spec, prefix):
        # peel the name of the script out of the pathname of the
        # downloaded file
        dir, script = split(self.stage.archive_file)
        bash = which("bash")
        bash(script, "-b", "-f", "-p", self.prefix)

    def setup_run_environment(self, env):
        filename = self.prefix.etc.join("profile.d").join("conda.sh")
        env.extend(EnvironmentModifications.from_sourcing_file(filename))
