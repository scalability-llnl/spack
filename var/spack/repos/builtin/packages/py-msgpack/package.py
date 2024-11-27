# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMsgpack(PythonPackage):
    """MessagePack (de)serializer."""

    homepage = "https://msgpack.org/"
    pypi = "msgpack/msgpack-1.0.0.tar.gz"
    git = "https://github.com/msgpack/msgpack-python"

    license("Apache-2.0")

    version("1.0.5", sha256="c075544284eadc5cddc70f4757331d99dcbc16b2bbd4849d15f8aae4cf36d31c")
    version("1.0.4", sha256="f5d869c18f030202eb412f08b28d2afeea553d6613aee89e200d7aca7ef01f5f")
    version("1.0.3", sha256="51fdc7fb93615286428ee7758cecc2f374d5ff363bdd884c7ea622a7a327a81e")
    version("1.0.2", sha256="fae04496f5bc150eefad4e9571d1a76c55d021325dcd484ce45065ebbdd00984")
    version("1.0.1", sha256="7033215267a0e9f60f4a5e4fb2228a932c404f237817caff8dc3115d9e7cd975")
    version("1.0.0", sha256="9534d5cc480d4aff720233411a1f765be90885750b07df772380b34c10ecb5c0")
    version("0.6.2", sha256="ea3c2f859346fcd55fc46e96885301d9c2f7a36d453f5d8f2967840efa1e1830")
    version("0.6.1", sha256="734e1abc6f14671f28acd5266de336ae6d8de522fe1c8d0b7146365ad1fe6b0f")
    version("0.6.0", sha256="4478a5f68142414084cd43af8f21cef9619ad08bb3c242ea505330dade6ca9ea")

    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@35.0.2:", when="@1.0.4:", type="build")
    depends_on("py-cython@0.29.30:0.29", when="@1.0.4:", type="build")
