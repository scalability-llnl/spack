# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCython(PythonPackage):
    """The Cython compiler for writing C extensions for the Python language."""

    homepage = "https://github.com/cython/cython"
    pypi = "cython/Cython-0.29.21.tar.gz"
    tags = ["build-tools"]

    license("Apache-2.0")

    version(
        "3.0.11",
        sha256="7146dd2af8682b4ca61331851e6aebce9fe5158e75300343f80c07ca80b1faff",
        url="https://files.pythonhosted.org/packages/source/cython/cython-3.0.11.tar.gz",
    )
    version("3.0.10", sha256="dcc96739331fb854dcf503f94607576cfe8488066c61ca50dfd55836f132de99")
    version("3.0.8", sha256="8333423d8fd5765e7cceea3a9985dd1e0a5dfeb2734629e1a2ed2d6233d39de6")
    version("3.0.7", sha256="fb299acf3a578573c190c858d49e0cf9d75f4bc49c3f24c5a63804997ef09213")
    version("3.0.6", sha256="399d185672c667b26eabbdca420c98564583798af3bc47670a8a09e9f19dd660")
    version("3.0.5", sha256="39318348db488a2f24e7c84e08bdc82f2624853c0fea8b475ea0b70b27176492")
    version("3.0.4", sha256="2e379b491ee985d31e5faaf050f79f4a8f59f482835906efe4477b33b4fbe9ff")
    version("3.0.0", sha256="350b18f9673e63101dbbfcf774ee2f57c20ac4636d255741d76ca79016b1bd82")
    version("0.29.36", sha256="41c0cfd2d754e383c9eeb95effc9aa4ab847d0c9747077ddd7c0dcb68c3bc01f")
    version("0.29.35", sha256="6e381fa0bf08b3c26ec2f616b19ae852c06f5750f4290118bf986b6f85c8c527")
    version("0.29.34", sha256="1909688f5d7b521a60c396d20bba9e47a1b2d2784bfb085401e1e1e7d29a29a8")
    version("0.29.33", sha256="5040764c4a4d2ce964a395da24f0d1ae58144995dab92c6b96f44c3f4d72286a")
    version("0.29.32", sha256="8733cf4758b79304f2a4e39ebfac5e92341bce47bcceb26c1254398b2f8c1af7")
    version("0.29.30", sha256="2235b62da8fe6fa8b99422c8e583f2fb95e143867d337b5c75e4b9a1a865f9e3")
    version("0.29.24", sha256="cdf04d07c3600860e8c2ebaad4e8f52ac3feb212453c1764a49ac08c827e8443")
    version("0.29.23", sha256="6a0d31452f0245daacb14c979c77e093eb1a546c760816b5eed0047686baad8e")
    version("0.29.22", sha256="df6b83c7a6d1d967ea89a2903e4a931377634a297459652e4551734c48195406")
    version("0.29.21", sha256="e57acb89bd55943c8d8bf813763d20b9099cc7165c0f16b707631a7654be9cad")
    version("0.29.20", sha256="22d91af5fc2253f717a1b80b8bb45acb655f643611983fd6f782b9423f8171c7")
    version("0.29.16", sha256="232755284f942cbb3b43a06cd85974ef3c970a021aef19b5243c03ee2b08fa05")
    version("0.29.15", sha256="60d859e1efa5cc80436d58aecd3718ff2e74b987db0518376046adedba97ac30")
    version("0.29.14", sha256="e4d6bb8703d0319eb04b7319b12ea41580df44fd84d83ccda13ea463c6801414")
    version("0.29.13", sha256="c29d069a4a30f472482343c866f7486731ad638ef9af92bfe5fca9c7323d638e")
    version("0.29.10", sha256="26229570d6787ff3caa932fe9d802960f51a89239b990d275ae845405ce43857")
    version("0.29.7", sha256="55d081162191b7c11c7bfcb7c68e913827dfd5de6ecdbab1b99dab190586c1e8")
    version("0.29.5", sha256="9d5290d749099a8e446422adfb0aa2142c711284800fb1eb70f595101e32cbf1")
    version("0.29", sha256="94916d1ede67682638d3cc0feb10648ff14dc51fb7a7f147f4fedce78eaaea97")
    version("0.28.6", sha256="68aa3c00ef1deccf4dd50f0201d47c268462978c12c42943bc33dc9dc816ac1b")
    version("0.28.3", sha256="1aae6d6e9858888144cea147eb5e677830f45faaff3d305d77378c3cba55f526")
    version("0.28.1", sha256="152ee5f345012ca3bb7cc71da2d3736ee20f52cd8476e4d49e5e25c5a4102b12")
    version("0.25.2", sha256="f141d1f9c27a07b5a93f7dc5339472067e2d7140d1c5a9e20112a5665ca60306")
    version("0.23.5", sha256="0ae5a5451a190e03ee36922c4189ca2c88d1df40a89b4f224bc842d388a0d1b6")
    version("0.23.4", sha256="fec42fecee35d6cc02887f1eef4e4952c97402ed2800bfe41bbd9ed1a0730d8e")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # https://github.com/cython/cython/issues/5751 (distutils not yet dropped)
    depends_on("python@:3.11", type=("build", "link", "run"))

    # https://github.com/cython/cython/commit/1cd24026e9cf6d63d539b359f8ba5155fd48ae21
    # collections.Iterable was removed in Python 3.10
    depends_on("python@:3.9", when="@:0.29.14", type=("build", "link", "run"))

    # https://github.com/cython/cython/commit/430e2ca220c8fed49604daf578df98aadb33a87d
    depends_on("python@:3.8", when="@:0.29.13", type=("build", "link", "run"))

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("gdb@7.2:", type="test")

    # Backports CYTHON_FORCE_REGEN environment variable
    patch("5307.patch", when="@0.29:0.29.33")
    patch("5712.patch", when="@0.29")

    @property
    def command(self):
        """Returns the Cython command"""
        return Executable(self.prefix.bin.cython)

    def setup_dependent_build_environment(self, env, dependent_spec):
        # If cython is used as a dep, ensure it's used even when pre-generated
        # C files are distributed in the tarball. Cython is a small build dep, and
        # the time generating C-files is typically less than compiling them. So it's
        # fine. It solves an issue where distributed C-sources were generated with
        # an old, buggy Cython. In particular Cython regularly depends on cpython
        # internals, which can change even in Python patch releases. It looks like
        # the Cython folks are coming back from their recommendation to *include*
        # pre-generated C-sources in tarballs, see also
        # https://github.com/cython/cython/issues/5089

        # Support for this was backported to 0.29.34, but we patch any 0.29 release
        if self.spec.version >= Version("0.29"):
            env.set("CYTHON_FORCE_REGEN", "1")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def build_test(self):
        # Warning: full suite of unit tests takes a very long time
        python("runtests.py", "-j", str(make_jobs))
