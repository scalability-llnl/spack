# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJinja2(PythonPackage):
    """Jinja2 is a template engine written in pure Python. It provides
    a Django inspired non-XML syntax but supports inline expressions
    and an optional sandboxed environment."""

    homepage = "https://palletsprojects.com/p/jinja/"
    url      = "https://pypi.io/packages/source/J/Jinja2/Jinja2-2.10.3.tar.gz"

    version('2.10.3', sha256='9fe95f19286cfefaa917656583d020be14e7859c6b0252588391e47db34527de')
    version('2.10.1', sha256='065c4f02ebe7f7cf559e49ee5a95fb800a9e4528727aec6f24402a5374c65013')
    version('2.10',   sha256='f84be1bb0040caca4cea721fcbbbbd61f9be9464ca236387158b0feea01914a4')
    version('2.9.6',  sha256='ddaa01a212cd6d641401cb01b605f4a4d9f37bfc93043d7f760ec70fb99ff9ff')
    version('2.8',    sha256='bc1ff2ff88dbfacefde4ddde471d1417d3b304e8df103a7a9437d47269201bf4')
    version('2.7.3',  sha256='2e24ac5d004db5714976a04ac0e80c6df6e47e98c354cb2c0d82f8879d4f8fdb')
    version('2.7.2',  sha256='310a35fbccac3af13ebf927297f871ac656b9da1d248b1fe6765affa71b53235')
    version('2.7.1',  sha256='5cc0a087a81dca1c08368482fb7a92fe2bdd8cfbb22bc0fccfe6c85affb04c8b')
    version('2.7',    sha256='474f1518d189ae7e318b139fecc1d30b943f124448cfa0f09582ca23e069fa4d')

    depends_on('py-setuptools', type='build')
    depends_on('py-markupsafe@0.23:', type=('build', 'run'))
    depends_on('py-babel@0.8:', type=('build', 'run'))  # optional, required for i18n
