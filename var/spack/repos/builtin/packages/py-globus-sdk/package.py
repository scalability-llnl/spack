# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGlobusSdk(PythonPackage):
    """
    Globus SDK for Python
    """

    homepage = "https://github.com/globus/globus-sdk-python"
    pypi = "globus_sdk/globus_sdk-3.0.2.tar.gz"

    maintainers("hategan", "climbfuji")

    license("Apache-2.0", checked_by="wdconinc")

    version("3.42.0", sha256="7f239acf26cd98c72568b07cc69d7e8d84511004881435c83129bf37c9495f43")
    version("3.41.0", sha256="a097829e7516735675c1535bd17a8d9137636678bdbf50e95b3e7af8b32638ef")
    version("3.40.0", sha256="6394f01c35b2b3275622f4f7c194eaf6750cb6c1e82cb2448dac2eb4ec394d75")
    version("3.39.0", sha256="10af5291ba261e817665d5951948206232ecebccdc2aa8adc0528f0031ab80c3")
    version("3.38.0", sha256="b83faacc103e3d3d3ac2ae33fd73a20a09d4d566cfa0cb03716b3fd8f51adcff")
    version("3.37.0", sha256="87cd4cc191bca5912138c1f992589c735e13436208db10f2de5831efbebc83a7")
    version("3.36.0", sha256="7693954a9ee3d69d09a0914c934ebcf4b4f47f016baa5c33612a03e367ee65a3")
    version("3.35.0", sha256="9da40d5f251f98d89297c2a92abd9f24bfa3c041dfd0e957579884ef0c882cf2")
    version("3.34.0", sha256="4db2ff439de9bd650bc2ba2d7c00614bd3dee34bd9b79da708951b8148236a36")
    version("3.33.0", sha256="38b048590cf7bbd01c5ac82346401c3f42c3f105c81421d61bcb771aa788f481")
    version("3.32.0", sha256="fe9df4ca2f2d16bbf40098df482e1713070946c70e2d6ec6a687c7086c1b559c")
    version("3.31.0", sha256="5f077a8e532828a137a54f2858e63695af16d02577de058278da4ec873556cc1")
    version("3.30.0", sha256="29d25f83d3b250d28a3a4bca8d046601a4bbb725330f409e6401295fa6bfb0ce")
    version("3.29.0", sha256="a5f3c2da86ac6e7165841c9364ae80893f2ae667add5af5cd2237fc3fa14a1be")
    version("3.28.0", sha256="249423dda76f162bb0d5515509135b68d6a779ad0cf2cd02a8204b2c7903e365")
    version("3.27.0", sha256="1e9afac3bcce7dd69199c6e85372b0d6cadcc0906b27129d88db7e41dc32f195")
    version("3.26.0", sha256="5a2bca267635c62e0f7c60fce10c47c7fd0fa8923c3363d44871c4abca8a68d1")
    version("3.25.0", sha256="d9be275d4ec18054db04732f75649c4227800c79b31fbcfb3f4f31eccfa5f4f7")
    version("3.10.1", sha256="c20fec55fc7e099f4d0c8224a36e194604577539445c5985cb465b23779baee8")
    version("3.10.0", sha256="7a7e7cd5cfbc40c6dc75bdb92b050c4191f992b5f7081cd08895bf119fd97bbf")
    version("3.9.0", sha256="456f707b25a8c502607134f1d699b5970ef1aa9d17877474db73fc6d87c711e9")
    version("3.8.0", sha256="492611636c190806409198cdadc9960227fa712281dce95ef3ec0d7e8f9823a9")
    version("3.7.0", sha256="81dbcb7bb7072bf9a5f730becc65e4a0f15f0fa0e2022faf2d943a99b5ce1fb5")
    version("3.0.2", sha256="765b577b37edac70c513179607f1c09de7b287baa855165c9dd68de076d67f16")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("python@3.7:", type=("build", "run"), when="@3.17:")
    depends_on("python@3.8:", type=("build", "run"), when="@3.42:")
    depends_on("py-setuptools", type="build")
    depends_on("py-requests@2.19.1:2", type=("build", "run"))
    depends_on("py-pyjwt@2.0.0:2+crypto", type=("build", "run"))
    depends_on("py-cryptography@3.3.1:3.3,3.4.1:", when="@3.7:", type=("build", "run"))
    depends_on("py-cryptography@2:3.3,3.4.1:3.6", when="@:3.0", type=("build", "run"))
    depends_on("py-typing-extensions@4:", when="@3.25: ^python@:3.9", type=("build", "run"))
    depends_on("py-importlib-resources@5.12.0:", when="@3.41: ^python@:3.8", type=("build", "run"))

    def url_for_version(self, version):
        if version <= Version("3.39"):
            return super().url_for_version(version).replace("_", "-")
        else:
            return super().url_for_version(version)
