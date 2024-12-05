# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCertifi(PythonPackage):
    """Certifi: A carefully curated collection of Root Certificates for validating
    the trustworthiness of SSL certificates while verifying the identity of TLS
    hosts."""

    homepage = "https://github.com/certifi/python-certifi"
    pypi = "certifi/certifi-2020.6.20.tar.gz"

    license("MPL-2.0")

    version("2023.7.22", sha256="539cc1d13202e33ca466e88b2807e29f4c13049d6d87031a3c110744495cb082")
    version("2023.5.7", sha256="0f0d56dc5a6ad56fd4ba36484d6cc34451e1c6548c61daad8c320169f91eddc7")
    version("2022.12.7", sha256="35824b4c3a97115964b408844d64aa14db1cc518f6562e8d7261699d1350a9e3")
    version("2022.9.14", sha256="36973885b9542e6bd01dea287b2b4b3b21236307c56324fcc3f1160f2d655ed5")
    version("2021.10.8", sha256="78884e7c1d4b00ce3cea67b44566851c4343c120abd683433ce934a68ea58872")
    version("2020.6.20", sha256="5930595817496dd21bb8dc35dad090f1c2cd0adfaf21204bf6732ca5d8ee34d3")
    version(
        "2020.4.5.1", sha256="51fcb31174be6e6664c5f69e3e1691a2d72a1a12e90f872cbdb1567eb47b6519"
    )
    version("2019.9.11", sha256="e4f3620cfea4f83eedc95b24abd9cd56f3c4b146dd0177e83a21b4eb49e21e50")
    version("2019.6.16", sha256="945e3ba63a0b9f577b1395204e13c3a231f9bc0223888be653286534e5873695")
    version("2019.3.9", sha256="b26104d6835d1f5e49452a26eb2ff87fe7090b89dfcaee5ea2212697e1e1d7ae")
    version("2017.4.17", sha256="f7527ebf7461582ce95f7a9e03dd141ce810d40590834f4ec20cddd54234c10a")
    version("2017.1.23", sha256="81877fb7ac126e9215dfb15bfef7115fdc30e798e0013065158eed0707fd99ce")

    depends_on("py-setuptools", type="build")
