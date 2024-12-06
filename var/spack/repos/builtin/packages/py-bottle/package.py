# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBottle(PythonPackage):
    """Bottle is a fast, simple and lightweight WSGI
    micro web-framework for Python."""

    homepage = "https://github.com/bottlepy/bottle"
    url = "https://github.com/bottlepy/bottle/archive/0.12.18.tar.gz"

    license("MIT")

    version("0.12.23", sha256="f38c26395736ae4653cbeb94087d3bd1d2e1ad0c29b1d3e5384f5db20b63bc98")
    version("0.12.19", sha256="b97277f8e87d452a0aa5fbcd16cd604a189e2cc17fdb2d4eaf6baa732f8d111b")
    version("0.12.18", sha256="176721f1e26082c66fd4df76f31800933e4bb36de6814b0fda3851cb409a95e6")
    version("0.12.17", sha256="7df26ca1789aa0693277c4a86d564524bff03e5d3132d9405946c58739190928")
    version("0.12.16", sha256="76143230ff034c1f47ada4b33674984220d070c557c10e22729ebd9764bc7960")
    version("0.12.15", sha256="18499bc1ec4a1af71d1df26f96b9a6f3f1d36ee45aa8420531b939ac402f3513")
    version("0.12.14", sha256="3d37cb8ebc6ab03986543280774c8b0aa028616123b9d4e2615b242fc8a291f9")
    version("0.12.13", sha256="c89ce532b1c180905d03a4815fea2d7b9b444f5e13407f43a9c7eae5777aa613")
    version("0.12.12", sha256="0d3ab0ef82ad697ac98978c246d073da4b19e446c06d2621865ca84a4a6e5e94")
    version("0.12.11", sha256="c815cfd1bd0757f4bc9e3d71973477373efba531bb63a8abc320e5550d8403b8")
    version("0.12.10", sha256="f57fb6594feac80fd92a573ab8ca7ce98491471211d99f1c97855e34f5d13677")
    version("0.12.9", sha256="45285ad084ca054d821ceef8bd95462efd38e13ecbef13a82c22b6472a6f4b2d")

    depends_on("python@2.5:2,3.2:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
