# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyMsgpack(PythonPackage):
    """MessagePack is an efficient binary serialization format."""

    homepage = "https://msgpack.org/"
    pypi = "msgpack/msgpack-1.0.0.tar.gz"

    version('1.0.0', sha256='9534d5cc480d4aff720233411a1f765be90885750b07df772380b34c10ecb5c0')
    version('0.6.2', sha256='ea3c2f859346fcd55fc46e96885301d9c2f7a36d453f5d8f2967840efa1e1830')
    version('0.6.1', sha256='734e1abc6f14671f28acd5266de336ae6d8de522fe1c8d0b7146365ad1fe6b0f')
    version('0.6.0', sha256='4478a5f68142414084cd43af8f21cef9619ad08bb3c242ea505330dade6ca9ea')
    depends_on('py-setuptools', type='build')
