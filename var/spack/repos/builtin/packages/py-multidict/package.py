# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMultidict(PythonPackage):
    """Multidict is dict-like collection of key-value pairs where key
    might be occurred more than once in the container."""

    homepage = "https://github.com/aio-libs/multidict"
    pypi = "multidict/multidict-6.0.2.tar.gz"

    license("Apache-2.0")

    version("6.0.4", sha256="3666906492efb76453c0e7b97f2cf459b0682e7402c0489a95484965dbc1da49")
    version("6.0.2", sha256="5ff3bd75f38e4c43f1f470f2df7a4d430b821c4ce22be384e1459cb57d6bb013")
    version("5.2.0", sha256="0dd1c93edb444b33ba2274b66f63def8a327d607c6c790772f448a53b6ea59ce")
    version("5.1.0", sha256="25b4e5f22d3a37ddf3effc0710ba692cfc792c2b9edfb9c05aefe823256e84d5")
    version("4.7.6", sha256="fbb77a75e529021e7c4a8d4e823d88ef4d23674a202be4f5addffc72cbb91430")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools@40:", type="build")

    # Historical dependencies
    depends_on("py-pip@18:", when="@:4", type="build")
