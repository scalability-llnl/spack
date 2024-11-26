# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAzureIdentity(PythonPackage):
    """Microsoft Azure Identity Library for Python."""

    homepage = (
        "https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/identity/azure-identity"
    )
    pypi = "azure-identity/azure-identity-1.15.0.tar.gz"

    # 'azure.identity.aio' import doesn't work for some reason, leave out of
    # 'import_modules' list to ensure that tests still pass for other imports.
    import_modules = ["azure.identity", "azure.identity._internal", "azure.identity._credentials"]

    license("MIT")

    version("1.17.1", sha256="32ecc67cc73f4bd0595e4f64b1ca65cd05186f4fe6f98ed2ae9f1aa32646efea")
    version("1.15.0", sha256="4c28fc246b7f9265610eb5261d65931183d019a23d4b0e99357facb2e6c227c8")
    version("1.14.1", sha256="48e2a9dbdc59b4f095f841d867d9a8cbe4c1cdbbad8251e055561afd47b4a9b8")
    version("1.13.0", sha256="c931c27301ffa86b07b4dcf574e29da73e3deba9ab5d1fe4f445bb6a3117e260")
    version("1.12.0", sha256="7f9b1ae7d97ea7af3f38dd09305e19ab81a1e16ab66ea186b6579d85c1ca2347")
    version("1.3.1", sha256="5a59c36b4b05bdaec455c390feda71b6495fc828246593404351b9a41c2e877a")
    version("1.2.0", sha256="b32acd1cdb6202bfe10d9a0858dc463d8960295da70ae18097eb3b85ab12cb91")

    # https://github.com/Azure/azure-sdk-for-python/blob/azure-identity_1.17.1/sdk/identity/azure-identity/setup.py

    depends_on("python@3.8:", type=("build", "run"), when="@1.16:")
    depends_on("py-setuptools", type="build")
    depends_on("py-azure-core@1.23:", type=("build", "run"), when="@1.16:")
    depends_on("py-azure-core@1.23:1", type=("build", "run"), when="@1.15")
    depends_on("py-azure-core@1.11:1", type=("build", "run"), when="@1.12:1.14")
    depends_on("py-azure-core@1", type=("build", "run"), when="@:1.15")
    depends_on("py-cryptography@2.5:", type=("build", "run"), when="@1.12:")
    depends_on("py-cryptography@2.1.4:", type=("build", "run"))
    depends_on("py-msal@1.24:", type=("build", "run"), when="@1.16:")
    depends_on("py-msal@1.24:1", type=("build", "run"), when="@1.15")
    depends_on("py-msal@1.20:1", type=("build", "run"), when="@1.13:1.14")
    depends_on("py-msal@1.12:1", type=("build", "run"), when="@1.12")
    depends_on("py-msal@1", type=("build", "run"), when="@:1.15")
    depends_on("py-msal-extensions@0.3:", type=("build", "run"), when="@1.16:")
    depends_on("py-msal-extensions@0.3:1", type=("build", "run"), when="@1.12:1.15")
    depends_on("py-msal-extensions@0.1.3:0.1", type=("build", "run"), when="@:1.11")
    depends_on("py-typing-extensions@4:", type=("build", "run"), when="@1.17:")

    depends_on("py-six@1.12:", type=("build", "run"), when="@1.12")
    depends_on("py-six@1.6:", type=("build", "run"), when="@:1.11")

    def url_for_version(self, version):
        if version < Version("1.15"):
            return (
                "https://pypi.io/packages/source/a/azure-identity/azure-identity-{0}.zip".format(
                    version
                )
            )

        return super().url_for_version(version)
