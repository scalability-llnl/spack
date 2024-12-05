# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Jansi(MavenPackage):
    """Jansi is a small java library that allows you to use
    ANSI escape codes to format your console output which
    works even on Windows."""

    homepage = "https://fusesource.github.io/jansi/"
    url = "https://github.com/fusesource/jansi/archive/jansi-project-1.18.tar.gz"

    license("Apache-2.0")

    version("1.18", sha256="73cd47ecf370a33c6e76afb5d9a8abf99489361d7bd191781dbd9b7efd082aa5")
    version("1.17.1", sha256="3d7280eb14edc82e480d66b225470ed6a1da5c5afa4faeab7804a1f15e53b2cd")
    version("1.17", sha256="aa30765df4912d8bc1a00b1cb9e50b3534c060dec84f35f1d0c6fbf40ad71b67")
    version("1.16", sha256="5f600cfa151367e029baa9ce33491059575945791ff9db82b8df8d4848187086")
    version("1.15", sha256="620c59deea17408eeddbe398d3638d7c9971de1807e494eb33fdf8c994b95104")

    depends_on("java@8", type=("build", "run"))
