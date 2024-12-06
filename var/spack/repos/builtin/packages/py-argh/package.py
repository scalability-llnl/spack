# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyArgh(PythonPackage):
    """An argparse wrapper that doesn't make you say "argh" each time
    you deal with it.

    Building a command-line interface? Found yourself uttering "argh!"
    while struggling with the API of argparse? Don't like the complexity
    but need the power? Argh is a smart wrapper for argparse. Argparse is
    a very powerful tool; Argh just makes it easy to use."""

    homepage = "https://github.com/neithere/argh/"
    pypi = "argh/argh-0.26.2.tar.gz"

    maintainers("dorton21")

    version("0.26.2", sha256="e9535b8c84dc9571a48999094fda7f33e63c3f1b74f3e5f3ac0105a58405bb65")

    depends_on("py-setuptools", type="build")
