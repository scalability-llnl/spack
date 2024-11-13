# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Check(AutotoolsPackage):
    """Check is a unit testing framework for C. It features a simple interface
    for defining unit tests, putting little in the way of the developer. Tests
    are run in a separate address space, so both assertion failures and code
    errors that cause segmentation faults or other signals can be caught. Test
    results are reportable in the following: Subunit, TAP, XML, and a generic
    logging format."""

    homepage = "https://libcheck.github.io/check/index.html"
    url = "https://github.com/libcheck/check/releases/download/0.12.0/check-0.12.0.tar.gz"

    license("LGPL-2.1-or-later")

    version("0.15.2", sha256="a8de4e0bacfb4d76dd1c618ded263523b53b85d92a146d8835eb1a52932fa20a")
    version("0.12.0", sha256="464201098bee00e90f5c4bdfa94a5d3ead8d641f9025b560a27755a83b824234")
    version("0.11.0", sha256="24f7a48aae6b74755bcbe964ce8bc7240f6ced2141f8d9cf480bc3b3de0d5616")
    version("0.10.0", sha256="f5f50766aa6f8fe5a2df752666ca01a950add45079aa06416b83765b1cf71052")

    depends_on("c", type="build")  # generated
