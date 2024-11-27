# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMsrest(PythonPackage):
    """AutoRest swagger generator Python client runtime."""

    homepage = "https://github.com/Azure/msrest-for-python"
    pypi = "msrest/msrest-0.7.1.zip"

    def url_for_version(self, version):
        if Version("0.4.8") < version < Version("0.7"):
            return "https://pypi.io/packages/source/m/msrest/msrest-{0}.tar.gz".format(version)

        return super().url_for_version(version)

    version("0.7.1", sha256="6e7661f46f3afd88b75667b7187a92829924446c7ea1d169be8c4bb7eeb788b9")
    version("0.6.21", sha256="72661bc7bedc2dc2040e8f170b6e9ef226ee6d3892e01affd4d26b06474d68d8")
    version("0.6.16", sha256="214c5be98954cb45feb6a6a858a7ae6d41a664e80294b65db225bbaa33d9ca3c")

    depends_on("py-setuptools", type="build")
    depends_on("py-requests@2.16:2", type=("build", "run"))
    depends_on("py-requests-oauthlib@0.5.0:", type=("build", "run"))
    depends_on("py-isodate@0.6.0:", type=("build", "run"))
    depends_on("py-certifi@2017.4.17:", type=("build", "run"))
    depends_on("py-azure-core@1.24:", type=("build", "run"), when="@0.7.1:")
