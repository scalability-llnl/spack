# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyKerasApplications(PythonPackage):
    """Sample Deep Learning application in Keras.
    Keras depends on this package to run properly."""

    homepage = "https://keras.io"
    url = "https://github.com/keras-team/keras-applications/archive/1.0.4.tar.gz"

    license("MIT")

    version("1.0.8", sha256="7c37f9e9ef93efac9b4956301cb21ce46c474ce9da41fac9a46753bab6823dfc")
    version("1.0.7", sha256="8580a885c8abe4bf8429cb0e551f23e79b14eda73d99138cfa1d355968dd4b0a")
    version("1.0.6", sha256="2cb412c97153160ec267b238e958d281ac3532b139cab42045c2d7086a157c21")
    version("1.0.4", sha256="37bd2f3ba9c0e0105c193999b1162fd99562cf43e5ef06c73932950ecc46d085")
    version("1.0.3", sha256="35b663a4933ee3c826a9349d19048221c997f0dd5ea24dd598c05cf90c72879d")
    version("1.0.2", sha256="6d8923876a7f7f2d459dd7efe3b10830f316f714b707f0c136e7f00c63035338")
    version("1.0.1", sha256="05ad1a73fddd22ed73ae59065b554e7ea13d05c3d4c6755ac166702b88686db5")

    depends_on("py-setuptools", type="build")
