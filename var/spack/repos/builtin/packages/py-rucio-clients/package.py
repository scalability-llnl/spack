# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRucioClients(PythonPackage):
    """Rucio Client Lite Package"""

    homepage = "https://rucio.cern.ch/"
    pypi = "rucio_clients/rucio_clients-35.4.0.tar.gz"

    maintainers("wdconinc")

    license("Apache-2.0", checked_by="wdconinc")

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
