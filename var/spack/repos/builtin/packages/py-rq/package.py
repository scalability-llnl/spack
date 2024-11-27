# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRq(PythonPackage):
    """RQ (Redis Queue) is a simple Python library for queueing
    jobs and processing them in the background with workers."""

    homepage = "https://github.com/rq/rq"
    url = "https://github.com/rq/rq/archive/v1.5.2.tar.gz"

    license("BSD-2-Clause-FreeBSD")

    version("1.5.2", sha256="e8e7b6ffc4a962837eaff8eb0137514346e629633bf08550a1649771cdc4ace6")
    version("1.5.1", sha256="36ca5cd2762b5b15bb176943f77da933fac6c2f4e5b5d47a0475f918c167fd4c")
    version("1.5.0", sha256="97443acd8aab1c273710f74db197838f68a0678f9cabb64c3598dfb816d35e13")
    version("1.4.3", sha256="a971aa16d346d1c145442af3bfb171ea620f375d240fbade3c42c2246d3d698a")
    version("1.4.2", sha256="478bd19ac4f66d3066459f5e8253cf5f477bfe128f69ed952f7565cb530ac6a4")
    version("1.4.1", sha256="fe158e3d9d4efe533f5698738f14e975656e396cd280c6acfd45952dc5ddfc66")
    version("1.4.0", sha256="03cd39392d31d00205bd1d84930e9b7aefc5d3ac9770c59092bdd8a94fc8a47d")
    version("1.3.0", sha256="ce94d07125b96313e8c4512b30c62da290ae6f5eeff60b8c3e2a0a08055f5608")
    version("1.2.2", sha256="ea71f805d4e3b972b4df5545529044df4bc0fbae30814a48bc28d8d0a39c0068")
    version("1.2.1", sha256="0b38344cda68710e572df9c70b733e95f1cdf13ce727a970f68307cedc98376a")

    depends_on("python@3.5:3.8", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-redis@3.5.0:", type=("build", "run"))
    depends_on("py-click@5.0.0:", type=("build", "run"))
