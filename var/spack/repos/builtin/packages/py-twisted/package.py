# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTwisted(PythonPackage):
    """An asynchronous networking framework written in Python"""

    homepage = "https://twistedmatrix.com/"
    pypi = "Twisted/twisted-21.7.0.tar.gz"

    license("Unlicense")

    version("24.7.0", sha256="5a60147f044187a127ec7da96d170d49bcce50c6fd36f594e60f4587eff4d394")
    version("22.10.0", sha256="32acbd40a94f5f46e7b42c109bfae2b302250945561783a8b7a059048f2d4d31")
    with default_args(deprecated=True):
        # https://nvd.nist.gov/vuln/detail/CVE-2022-24801
        version(
            "21.7.0", sha256="2cd652542463277378b0d349f47c62f20d9306e57d1247baabd6d1d38a109006"
        )
        version(
            "15.4.0", sha256="78862662fa9ae29654bc2b9d349c3f1d887e6b2ed978512c4442d53ea861f05c"
        )
        version(
            "15.3.0", sha256="025729751cf898842262375a40f70ae1d246daea88369eab9f6bb96e528bf285"
        )

    depends_on("python@3.6.7:", type=("build", "run"), when="@21.7.0:")
    depends_on("python@3.7.1:", type=("build", "run"), when="@22.8.0:")

    with when("@:22.10"):
        depends_on("py-setuptools", type="build")
        depends_on("py-setuptools@35.0.2:", type="build", when="@21.7.0:")
    with when("@23.8.0:"):
        depends_on("py-hatchling@1.10.0:", type="build")
        depends_on("py-hatch-fancy-pypi-readme@22.5.0:", type="build")
        depends_on("py-incremental@22.10.0:", type="build")

    depends_on("py-zope-interface@4.0.2:", type=("build", "run"))
    depends_on("py-zope-interface@4.4.2:", type=("build", "run"), when="@21.7.0:")
    depends_on("py-zope-interface@5:", type=("build", "run"), when="@23.8.0:")

    depends_on("py-incremental@21.3.0:", type=("build", "run"), when="@21.7.0:")
    depends_on("py-incremental@22.10.0:", type=("build", "run"), when="@23.8.0:")
    depends_on("py-constantly@15.1:", type=("build", "run"), when="@21.7.0:")
    depends_on("py-automat@0.8.0:", type=("build", "run"), when="@21.7.0:")
    depends_on("py-hyperlink@17.1.1:", type=("build", "run"), when="@21.7.0:")
    depends_on("py-attrs@19.2.0:", type=("build", "run"), when="@21.7.0:")
    depends_on("py-attrs@21.3.0:", type=("build", "run"), when="@23.8.0:")
    depends_on("py-typing-extensions@3.6.5:", type=("build", "run"), when="@21.7.0:")
    depends_on("py-typing-extensions@3.10.0:", type=("build", "run"), when="@23.8.0:")

    def url_for_version(self, version):
        url = "https://pypi.io/packages/source/T/Twisted/"

        if version <= Version("20.3.0"):
            url += "Twisted-{0}.tar.bz2"
        elif version <= Version("22.10.0"):
            url += "Twisted-{0}.tar.gz"
        else:
            url += "twisted-{0}.tar.gz"

        url = url.format(version)
        return url

    @property
    def import_modules(self):
        modules = [
            "twisted",
            "twisted.positioning",
            "twisted.positioning.test",
            "twisted.protocols",
            "twisted.protocols.test",
            "twisted.protocols.haproxy",
            "twisted.protocols.haproxy.test",
            "twisted.web",
            "twisted.web._auth",
            "twisted.web.test",
            "twisted.scripts",
            "twisted.scripts.test",
            "twisted.runner",
            "twisted.runner.test",
            "twisted.cred",
            "twisted.cred.test",
            "twisted.plugins",
            "twisted.enterprise",
            "twisted.logger",
            "twisted.logger.test",
            "twisted.persisted",
            "twisted.persisted.test",
            "twisted.names",
            "twisted.names.test",
            "twisted.pair",
            "twisted.pair.test",
            "twisted.test",
            "twisted.tap",
            "twisted.python",
            "twisted.python.test",
            "twisted.trial",
            "twisted.trial._dist",
            "twisted.trial._dist.test",
            "twisted.trial.test",
            "twisted.words",
            "twisted.words.protocols",
            "twisted.words.protocols.jabber",
            "twisted.words.im",
            "twisted.words.test",
            "twisted.words.xish",
            "twisted.spread",
            "twisted.spread.test",
            "twisted.conch",
            "twisted.conch.scripts",
            "twisted.conch.ui",
            "twisted.conch.client",
            "twisted.conch.openssh_compat",
            "twisted.conch.test",
            "twisted.conch.insults",
            "twisted.conch.ssh",
            "twisted.internet",
            "twisted.internet.test",
        ]

        return modules
