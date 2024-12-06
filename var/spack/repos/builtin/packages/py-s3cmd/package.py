# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyS3cmd(PythonPackage):
    """
    S3cmd (s3cmd) is a free command line tool and client for uploading,
    retrieving and managing data in Amazon S3 and other cloud storage
    service providers that use the S3 protocol, such as Google Cloud
    Storage or DreamHost DreamObjects. It is best suited for power
    users who are familiar with command line programs.
    """

    homepage = "https://github.com/s3tools/s3cmd"
    url = "https://github.com/s3tools/s3cmd/releases/download/v2.0.2/s3cmd-2.0.2.tar.gz"

    version("2.3.0", sha256="15330776e7ff993d8ae0ac213bf896f210719e9b91445f5f7626a8fa7e74e30b")
    version("2.2.0", sha256="2a7d2afe09ce5aa9f2ce925b68c6e0c1903dd8d4e4a591cd7047da8e983a99c3")
    version("2.1.0", sha256="966b0a494a916fc3b4324de38f089c86c70ee90e8e1cae6d59102103a4c0cc03")
    version("2.0.2", sha256="9f244c0c10d58d0ccacbba3aa977463e32491bdd9d95109e27b67e4d46c5bd52")
    version("2.0.1", sha256="caf09f1473301c442fba6431c983c361c9af8bde503dac0953f0d2f8f2c53c8f")
    version("2.0.0", sha256="bf2a50802f1031cba83e99be488965803899d8ab0228c800c833b55c7269cd48")
    version("1.6.1", sha256="4675794f84d8744ee3d35873d180f41c7b2116895ccbe2738a9bc552e1cf214e")
    version("1.6.0", sha256="04279ee26c661d4b740449460ed93a74ffec91616f685474beea97e930fdfa5c")
    version("1.5.2", sha256="ff8a6764e8bdd7ed48a93e51b08222bea33469d248a90b8d25315b023717b42d")

    depends_on("py-setuptools", type="build")
    depends_on("python@2.6:+pyexpat", type=("build", "run"))
    depends_on("py-python-dateutil", type=("build", "run"))
    depends_on("py-python-magic", type=("build", "run"))
