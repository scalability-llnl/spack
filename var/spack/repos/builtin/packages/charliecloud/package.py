# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Charliecloud(AutotoolsPackage):
    """Lightweight user-defined software stacks for HPC."""

    maintainers("j-ogas", "reidpr")
    homepage = "https://hpc.github.io/charliecloud"
    url = "https://github.com/hpc/charliecloud/releases/download/v0.18/charliecloud-0.18.tar.gz"
    git = "https://github.com/hpc/charliecloud.git"

    tags = ["e4s"]

    license("Apache-2.0")

    version("master", branch="master")
    version("0.38", sha256="1a3766d57ff4db9c65fd5c561bbaac52476c9a19fa10c1554190912a03429b7a")
    version("0.37", sha256="1fd8e7cd1dd09a001aead5e105e3234792c1a1e9e30417f495ab3f422ade7397")
    version("0.36", sha256="b6b1a085d8ff82abc6d625ab990af3925c84fa08ec837828b383f329bd0b8e72")
    version("0.35", sha256="042f5be5ed8eda95f45230b4647510780142a50adb4e748be57e8dd8926b310e")
    version(
        "0.34",
        deprecated=True,
        sha256="034080c162949f4344ae1011cda026d4bb3ecd5cdb53135ac06d236f87e3b27d",
    )
    version(
        "0.33",
        deprecated=True,
        sha256="ed2bd3589d1e5f7b33a1542c887d69856f6d7d57a6ec8ef5b8e9335eda48a045",
    )
    version(
        "0.32",
        deprecated=True,
        sha256="47826b14966c400b250c35ff28a903f8e5b5e12d9e2a2b473e0f00f4e8393c47",
    )
    version(
        "0.31",
        deprecated=True,
        sha256="7305c3d9010386c1b96fb95297feccb5c9d7ff82a3377d1d98eb8faef76bced9",
    )
    version(
        "0.30",
        deprecated=True,
        sha256="97d45b25c9f813d8bae79b16de49503a165bc94c05dd2166975154d9b6ac78e9",
    )
    version(
        "0.29",
        deprecated=True,
        sha256="c89562e9dce4c10027434ad52eaca2140e2ba8667aa1ec9eadf789b4d7c1a6db",
    )
    version(
        "0.28",
        deprecated=True,
        sha256="1ce43b012f475bddb514bb75993efeda9e58ffa93ddbdbd9b86d647f57254c3b",
    )
    version(
        "0.27",
        deprecated=True,
        sha256="1142938ce73ec8a5dfe3a19a241b1f1ffbb63b582ac63d459aebec842c3f4b72",
    )
    version(
        "0.26",
        deprecated=True,
        sha256="5e1e64e869c59905fac0cbbd6ceb82340ee54728415d28ef588fd5de5557038a",
    )
    version(
        "0.25",
        deprecated=True,
        sha256="62d6fd211e3a573f54578e1b01d5c298f9788b7eaf2db46ac94c2dcef604cc94",
    )
    version(
        "0.24",
        deprecated=True,
        sha256="63379bcbad7b90b33457251696d6720416e4acefcf2b49cd6cb495a567e511c2",
    )
    version(
        "0.23",
        deprecated=True,
        sha256="5e458b943ad0e27d1264bb089e48d4a676219179b0e96a7d761387a36c45b4d9",
    )
    version(
        "0.22",
        deprecated=True,
        sha256="f65e4111ce87e449c656032da69f3b1cfc70a5a416a5e410329c1b0b2e953907",
    )
    version(
        "0.21",
        deprecated=True,
        sha256="024884074d283c4a0387d899161610fa4ae739ac1efcc9e53d7d626ddc20359f",
    )
    version(
        "0.19",
        deprecated=True,
        sha256="99619fd86860cda18f7f7a7cf7391f702ec9ebd3193791320dea647769996447",
    )
    version(
        "0.18",
        deprecated=True,
        sha256="15ce63353afe1fc6bcc10979496a54fcd5628f997cb13c827c9fc7afb795bdc5",
    )

    depends_on("c", type="build")  # generated
    variant("docs", default=False, description="Build man pages and html docs")
    variant("squashfuse", default=True, description="Build with squashfuse support", when="@0.32:")

    # Autoconf.
    depends_on("m4", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    # pkg-config is required for 0.36 regardless of variant.
    depends_on("pkgconfig", type="build", when="@0.36")

    # Image manipulation.
    depends_on("python@3.6:", type="run")
    depends_on("py-requests", type="run")
    depends_on("git@2.28.1:", type="run", when="@0.29:")  # build cache
    depends_on("py-lark", type="run", when="@:0.24")  # 0.25+ bundles lark

    # Man page and html docs.
    depends_on("rsync", type="build", when="+docs")
    depends_on("py-sphinx", type="build", when="+docs")
    depends_on("py-sphinx-rtd-theme", type="build", when="+docs")

    # Bash automated testing harness (bats).
    depends_on("bats@0.4.0", when="@:0.32")
    depends_on("bats@1.10.0:", when="@0.33:")

    # Require pip and wheel for git checkout builds (master).
    depends_on("py-pip@21.1.2:", type="build", when="@master")
    depends_on("py-wheel", type="build", when="@master")

    # See https://github.com/spack/spack/pull/16049.
    conflicts("platform=darwin", msg="This package does not build on macOS")

    # Squashfuse support. For why this is so messy, see:
    # https://github.com/hpc/charliecloud/issues/1696
    # https://github.com/hpc/charliecloud/pull/1697
    # https://github.com/hpc/charliecloud/pull/1784
    #
    # FIXME: the current variant and dependencies reflect
    # Charliecloud's automatic mount/un-mounting requirements. A more manual
    # approach with squashfuse could implemented in a different variant.
    with when("+squashfuse"):
        depends_on("libfuse@3:", type=("build", "run", "link"), when="@0.32:")
        depends_on("pkgconfig", type="build", when="@0.37:")
        depends_on("squashfuse@0.1.105:0.2.0,0.4.0:", type="link", when="@0.36:")
        depends_on("squashfuse@0.1.105:0.2.0,0.4.0", type="link", when="@0.35")
        depends_on("squashfuse@0.1.105", type="link", when="@0.32:0.34")

    def autoreconf(self, spec, prefix):
        which("bash")("autogen.sh")

    def configure_args(self):
        args = []
        py_path = self.spec["python"].command.path
        args.append("--with-python={0}".format(py_path))

        if self.spec.satisfies("+docs"):
            sphinx_bin = "{0}".format(self.spec["py-sphinx"].prefix.bin)
            args.append("--enable-html")
            args.append("--with-sphinx-build={0}".format(sphinx_bin.join("sphinx-build")))
        else:
            args.append("--disable-html")

        if self.spec.satisfies("+squashfuse"):
            squashfuse_prefix = "{0}".format(self.spec["squashfuse"].prefix)
            args.append("--with-libsquashfuse={0}".format(squashfuse_prefix))

        return args
