# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOsloSerialization(PythonPackage):
    """
    The oslo.serialization library provides support for representing objects in
    transmittable and storable formats, such as Base64, JSON and MessagePack.
    """

    homepage = "https://docs.openstack.org/oslo.serialization/"
    pypi = "oslo.serialization/oslo.serialization-4.1.0.tar.gz"

    maintainers("haampie")

    version("4.1.0", sha256="cecc7794df806c85cb70dbd6c2b3af19bc68047ad29e3c6442be90a0a4de5379")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pbr@2.0.0:2.0,2.1.1:", type="build")

    depends_on("py-msgpack@0.5.2:", type=("build", "run"))
    depends_on("py-oslo-utils@3.33.0:", type=("build", "run"))
    depends_on("py-pytz@2013.6:", type=("build", "run"))
