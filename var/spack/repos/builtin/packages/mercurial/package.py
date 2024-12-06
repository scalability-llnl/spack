# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from llnl.util import tty

from spack.package import *


class Mercurial(PythonPackage):
    """Mercurial is a free, distributed source control management tool."""

    homepage = "https://www.mercurial-scm.org"
    url = "https://www.mercurial-scm.org/release/mercurial-5.3.tar.gz"

    license("GPL-2.0-or-later")

    version("6.7.3", sha256="00196944ea92738809317dc7a8ed7cb21287ca0a00a85246e66170955dcd9031")
    version("6.6.3", sha256="f75d6a4a75823a1b7d713a4967eca2f596f466e58fc6bc06d72642932fd7e307")
    version("6.4.5", sha256="b0b4b00b8b2639c8be387394796f0425beb339314df7e72937f8ddd2a41b1b8a")
    version("6.3.3", sha256="13c97ff589c7605e80a488f336852ce1d538c5d4143cfb33be69bdaddd9157bd")
    version("6.2.3", sha256="98d1ae002f68adf53d65c5947fe8b7a379f98cf05d9b8ea1f4077d2ca5dce9db")
    version("6.1.4", sha256="f361f9802b36e357ac019ceb712ca11de8332b07deadeed8dfa904f05bf7ca78")
    version("6.0.3", sha256="67f13647a46517a2b567cdcb73c98721d75d36a0432debb15022b77f9c138333")
    version("5.8", sha256="fc5d6a8f6478d88ef83cdd0ab6d86ad68ee722bbdf4964e6a0b47c3c6ba5309f")
    version("5.7.1", sha256="cb5139144ccb2ef648f36963c8606d47dea1cb0e22aa2c055d6f860ce3fde7b0")
    version("5.7", sha256="609c3e7c9276dd75b03b713eccc10f5e0553001f35ae21600bcea1509699c601")
    version("5.6.1", sha256="e55c254f4904c45226a106780e57f4279aee03368f6ff6a981d5d2a38243ffad")
    version("5.3", sha256="e57ff61d6b67695149dd451922b40aa455ab02e01711806a131a1e95c544f9b9")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("python+bz2+ssl+zlib", type=("build", "run"))
    depends_on("python@3.5:", when="@5.2:", type=("build", "run"))
    depends_on("python@3.6:", when="@6.2:", type=("build", "run"))
    # Upperbounds because of forward compat issues.
    depends_on("python@:3.9", when="@:6.0.0", type=("build", "run"))
    depends_on("python@:3.10", when="@:6.3.0", type=("build", "run"))

    depends_on("py-setuptools", type="build")
    depends_on("py-docutils", type="build")
    depends_on("py-pygments", type=("build", "run"))
    depends_on("py-certifi", type=("build", "run"))

    def setup_build_environment(self, env):
        # Python 3 support is still experimental, explicitly allow
        env.set("HGALLOWPYTHON3", True)
        env.set("HGPYTHON3", True)
        # Setuptools is still opt-in, explicitly enable
        env.set("FORCE_SETUPTOOLS", True)

    @run_after("install")
    def post_install(self):
        prefix = self.prefix

        # Install man pages
        mkdirp(prefix.man.man1)
        mkdirp(prefix.man.man5)
        mkdirp(prefix.man.man8)
        with working_dir("doc"):
            install("hg.1", prefix.man.man1)
            install("hgignore.5", prefix.man.man5)
            install("hgrc.5", prefix.man.man5)
            install("hg-ssh.8", prefix.man.man8)

        # Install completion scripts
        contrib = prefix.contrib
        mkdir(contrib)
        with working_dir("contrib"):
            install("bash_completion", contrib.bash_completion)
            install("zsh_completion", contrib.zsh_completion)

    @run_after("install")
    def configure_certificates(self):
        """Configuration of HTTPS certificate authorities
        https://www.mercurial-scm.org/wiki/CACertificates"""

        etc_dir = self.prefix.etc.mercurial
        mkdirp(etc_dir)

        hgrc_filename = etc_dir.hgrc

        # Use certifi to find the location of the CA certificate
        certificate = python("-c", "import certifi; print(certifi.where())", output=str)

        if not certificate:
            tty.warn(
                "CA certificate not found. You may not be able to "
                "connect to an HTTPS server. If your CA certificate "
                "is in a non-standard location, you should add it to "
                "{0}.".format(hgrc_filename)
            )
        else:
            # Write the global mercurial configuration file
            with open(hgrc_filename, "w") as hgrc:
                hgrc.write(f"[web]\ncacerts = {certificate}")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_install(self):
        """Sanity-check setup."""

        hg = Executable(self.prefix.bin.hg)

        hg("debuginstall")
        hg("version")
