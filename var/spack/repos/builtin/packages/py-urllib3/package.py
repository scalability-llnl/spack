# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUrllib3(PythonPackage):
    """HTTP library with thread-safe connection pooling, file post, and
    more."""

    homepage = "https://urllib3.readthedocs.io/"
    pypi = "urllib3/urllib3-1.25.6.tar.gz"
    git = "https://github.com/urllib3/urllib3.git"

    license("MIT")

    version("2.1.0", sha256="df7aa8afb0148fa78488e7899b2c59b5f4ffcfa82e6c54ccb9dd37c1d7b52d54")
    version("2.0.7", sha256="c97dfde1f7bd43a71c8d2a58e369e9b2bf692d1334ea9f9cae55add7d0dd0f84")
    version("2.0.6", sha256="b19e1a85d206b56d7df1d5e683df4a7725252a964e3993648dd0fb5a1c157564")
    version("2.0.5", sha256="13abf37382ea2ce6fb744d4dad67838eec857c9f4f57009891805e0b5e123594")
    version("1.26.20", sha256="40c2dc0c681e47eb8f90e7e27bf6ff7df2e677421fd46756da1161c39ca70d32")
    version("1.26.12", sha256="3fa96cf423e6987997fc326ae8df396db2a8b7c667747d47ddd8ecba91f4a74e")
    version("1.26.6", sha256="f57b4c16c62fa2760b7e3d97c35b255512fb6b59a259730f36ba32ce9f8e342f")
    version("1.25.11", sha256="8d7eaa5a82a1cac232164990f04874c594c9453ec55eef02eab885aa02fc17a2")
    version("1.25.9", sha256="3018294ebefce6572a474f0604c2021e33b3fd8006ecd11d62107a5d2a963527")
    version("1.25.6", sha256="9a107b99a5393caf59c7aa3c1249c16e6879447533d0887f4336dde834c7be86")
    version("1.25.3", sha256="dbe59173209418ae49d485b87d1681aefa36252ee85884c31346debd19463232")
    version("1.24.3", sha256="2393a695cd12afedd0dcb26fe5d50d0cf248e5a66f75dbd89a3d4eb333a61af4")
    version("1.21.1", sha256="b14486978518ca0901a76ba973d7821047409d7f726f22156b24e83fd71382a5")
    version("1.20", sha256="97ef2b6e2878d84c0126b9f4e608e37a951ca7848e4855a7f7f4437d5c34a72f")
    version("1.14", sha256="dd4fb13a4ce50b18338c7e4d665b21fd38632c5d4b1d9f1a1379276bd3c08d37")

    variant("brotli", default=False, when="@1.25:", description="Add Brotli support")
    variant("socks", default=False, when="@1.15:", description="SOCKS and HTTP proxy support")
    # Historical variant
    variant("secure", default=False, when="@:2.0", description="Add SSL/TLS support")

    depends_on("python@3.8:", when="@2.1:", type=("build", "run"))
    depends_on("py-hatchling@1.6:1", when="@2:", type="build")

    with when("+brotli"):
        depends_on("py-brotli@1.0.9:", when="@1.26.9:", type=("build", "run"))

        # Historical dependencies
        depends_on("py-brotlipy@0.6:", when="@:1.26.8", type=("build", "run"))

    depends_on("py-pysocks@1.5.6,1.5.8:1", when="+socks", type=("build", "run"))

    # Historical dependencies
    with when("+secure"):
        depends_on("py-pyopenssl@17.1:", when="@2:", type=("build", "run"))
        depends_on("py-pyopenssl@0.14:", when="@1", type=("build", "run"))
        depends_on("py-cryptography@1.9:", when="@2:", type=("build", "run"))
        depends_on("py-cryptography@1.3.4:", when="@1", type=("build", "run"))
        depends_on("py-idna@2:", type=("build", "run"))
        depends_on("py-certifi", type=("build", "run"))
        depends_on("py-urllib3-secure-extra", when="@1.26.12:", type=("build", "run"))

    depends_on("py-setuptools", when="@1", type="build")
    depends_on("python@3.6:3", when="@1.26.12:1", type=("build", "run"))
