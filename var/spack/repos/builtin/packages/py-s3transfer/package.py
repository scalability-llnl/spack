# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyS3transfer(PythonPackage):
    """S3transfer is a Python library for managing Amazon S3 transfers."""

    homepage = "https://github.com/boto/s3transfer"
    pypi = "s3transfer/s3transfer-0.2.1.tar.gz"

    license("Apache-2.0")

    version("0.10.0", sha256="d0c8bbf672d5eebbe4e57945e23b972d963f07d82f661cabf678a5c88831595b")
    version("0.9.0", sha256="9e1b186ec8bb5907a1e82b51237091889a9973a2bb799a924bcd9f301ff79d3d")
    version("0.8.2", sha256="368ac6876a9e9ed91f6bc86581e319be08188dc60d50e0d56308ed5765446283")
    version("0.7.0", sha256="fd3889a66f5fe17299fe75b82eae6cf722554edca744ca5d5fe308b104883d2e")
    version("0.6.2", sha256="cab66d3380cca3e70939ef2255d01cd8aece6a4907a9528740f668c4b0611861")
    version("0.6.0", sha256="2ed07d3866f523cc561bf4a00fc5535827981b117dd7876f036b0c1aca42c947")
    version("0.5.0", sha256="50ed823e1dc5868ad40c8dc92072f757aa0e653a192845c94a3b676f4a62da4c")
    version("0.4.2", sha256="cb022f4b16551edebbb31a377d3f09600dbada7363d8c5db7976e7f47732e1b2")
    version("0.3.4", sha256="7fdddb4f22275cf1d32129e21f056337fd2a80b6ccef1664528145b72c49e6d2")
    version("0.2.1", sha256="6efc926738a3cd576c2a79725fed9afde92378aa5c6a957e3af010cb019fac9d")

    depends_on("py-setuptools", type="build")

    depends_on("py-botocore@1.33.2:1", type=("build", "run"), when="@0.8.1:")
    depends_on("py-botocore@1.32.7:1", type=("build", "run"), when="@0.8.0:")
    depends_on("py-botocore@1.12.36:1", type=("build", "run"))
