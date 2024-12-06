# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyConfigargparse(PythonPackage):
    """Applications with more than a handful of user-settable
    options are best configured through a combination of
    command line args, config files, hard-coded defaults, and
    in some cases, environment variables.

    Python's command line parsing modules such as argparse have
    very limited support for config files and environment
    variables, so this module extends argparse to add these
    features."""

    homepage = "https://github.com/bw2/ConfigArgParse"
    url = "https://github.com/bw2/ConfigArgParse/archive/1.7.tar.gz"

    license("MIT")

    version("1.7", sha256="4549d105790386d01f71beebc3aa457d4177315680b75415f05bc22e1e28183a")
    version("1.5.7", sha256="2156f15ef4ccce4377427046789ce93e0b09ac425c7297f1c9572655bf11bdfe")
    version("1.5.5", sha256="5b8316f11985aa169e51126086d3d6d24d7ba976585266311491015ddffbd717")
    version("1.2.3", sha256="0f1144a204e3b896d6ac900e151c1d13bde3103d6b7d541e3bb57514a94083bf")

    depends_on("py-setuptools", type="build")
