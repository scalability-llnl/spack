# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBabel(PythonPackage):
    """Babel is an integrated collection of utilities that assist in
    internationalizing and localizing Python applications, with an
    emphasis on web-based applications."""

    homepage = "https://babel.pocoo.org/en/latest/"
    pypi = "Babel/babel-2.15.0.tar.gz"
    git = "https://github.com/python-babel/babel"

    license("BSD-3-Clause")

    version("2.15.0", sha256="8daf0e265d05768bc6c7a314cf1321e9a123afc328cc635c18622a2f30a04413")
    version("2.12.1", sha256="cc2d99999cd01d44420ae725a21c9e3711b3aadc7976d6147f622d8581963455")
    version("2.10.3", sha256="7614553711ee97490f732126dc077f8d0ae084ebc6a96e23db1482afabdb2c51")
    version("2.9.1", sha256="bc0c176f9f6a994582230df350aa6e05ba2ebe4b3ac317eab29d9be5d2768da0")
    version("2.7.0", sha256="e86135ae101e31e2c8ec20a4e0c5220f4eed12487d5cf3f78be7e98d3a57fc28")
    version("2.6.0", sha256="8cba50f48c529ca3fa18cf81fa9403be176d374ac4d60738b839122dfaaa3d23")
    version("2.4.0", sha256="8c98f5e5f8f5f088571f2c6bd88d530e331cbbcb95a7311a0db69d3dca7ec563")
    version("2.3.4", sha256="c535c4403802f6eb38173cd4863e419e2274921a01a8aad8a5b497c131c62875")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-pytz@2015.7:", when="@2.12: ^python@:3.8", type=("build", "run"))
    depends_on("py-pytz@2015.7:", when="@:2.10", type=("build", "run"))

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/source/B/Babel/{}-{}.tar.gz"
        name = "Babel"
        if version >= Version("2.15"):
            name = name.lower()
        return url.format(name, version)
