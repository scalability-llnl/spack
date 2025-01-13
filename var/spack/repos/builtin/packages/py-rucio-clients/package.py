# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRucioClients(PythonPackage):
    """Rucio Client Lite Package"""

    homepage = "https://rucio.cern.ch/"
    pypi = "rucio_clients/rucio_clients-35.4.0.tar.gz"

    maintainers("wdconinc")

    license("Apache-2.0", checked_by="wdconinc")

    version(
        "36.0.0.post2", sha256="48ac2e3217aac9aaa70133cbfff991560bbeb162165bcf3dd3425967c8a2f816"
    )
    version(
        "36.0.0.post1", sha256="141aafdde66080d36708dedc9f06a72c55918ee1d138b8cd2f5d2fe43cbc504f"
    )
    version("36.0.0", sha256="80fbf3b2ec63c13ac1ce430d769fcc526a5f742ba3960ecc64560e0d4cd465b5")
    version("35.6.0", sha256="3c77dea0ce95b7649211da08cee7e93fa9ecb1a6c91bbe750b76b4c576a8b0dd")
    version("35.5.0", sha256="bc79602193e271f66c3fdb43e7abda7903026795d6f3c5d71afb5e52250f8d92")
    version("35.4.1", sha256="d87405785776d7522100cda2ebc16892f94cda94d3c257896ee4817c4e03c06b")
    version("35.4.0", sha256="f8771ee39d0d496109586ddbb4000ce006a193fd33cdac8a654661ae0b7346c0")

    variant("ssh", default=False, description="Enable SSH2 protocol library")
    variant("kerberos", default=False, description="Enable kerberos authentication")
    variant("swift", default=False, description="Enable support for swift service")
    variant("argcomplete", default=False, description="Enable bash tab completion for argparse")
    variant("dumper", default=False, description="Enable file type identification using libmagic")

    # requirements/requirements.client.txt
    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-requests@2.32.2:", type=("build", "run"))
    depends_on("py-urllib3@1.26.18:", type=("build", "run"))
    depends_on("py-dogpile-cache@1.2.2:", type=("build", "run"))
    depends_on("py-tabulate@0.9.0:", type=("build", "run"))
    depends_on("py-jsonschema@4.20.0:", type=("build", "run"))
    depends_on("py-packaging@24.1:", type=("build", "run"), when="@36:")
    depends_on("py-rich@13.7.1:", type=("build", "run"), when="@36:")
    depends_on("py-typing-extensions@4.12.2:", type=("build", "run"), when="@36:")

    with when("+ssh"):
        depends_on("py-paramiko@3.4.0:")
    with when("+kerberos"):
        depends_on("py-kerberos@1.3.1:")
        depends_on("py-pykerberos@1.2.4:")
        depends_on("py-requests-kerberos@0.14.0:")
    with when("+swift"):
        depends_on("py-python-swiftclient@4.4.0:")
    with when("+argcomplete"):
        depends_on("py-argcomplete@3.1.6:")
    with when("+dumper"):
        depends_on("py-python-magic@0.4.27:")
