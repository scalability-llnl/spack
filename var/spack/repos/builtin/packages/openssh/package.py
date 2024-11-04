# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import socket

from spack.package import *


class Openssh(AutotoolsPackage):
    """OpenSSH is the premier connectivity tool for remote login with the
    SSH protocol. It encrypts all traffic to eliminate
    eavesdropping, connection hijacking, and other attacks. In
    addition, OpenSSH provides a large suite of secure tunneling
    capabilities, several authentication methods, and sophisticated
    configuration options.
    """

    homepage = "https://www.openssh.com/"
    url = "https://mirrors.sonic.net/pub/OpenBSD/OpenSSH/portable/openssh-8.7p1.tar.gz"

    tags = ["core-packages"]

    license("SSH-OpenSSH")

    version("9.8p1", sha256="dd8bd002a379b5d499dfb050dd1fa9af8029e80461f4bb6c523c49973f5a39f3")
    version("9.7p1", sha256="490426f766d82a2763fcacd8d83ea3d70798750c7bd2aff2e57dc5660f773ffd")
    version("9.6p1", sha256="910211c07255a8c5ad654391b40ee59800710dd8119dd5362de09385aa7a777c")
    version("9.5p1", sha256="f026e7b79ba7fb540f75182af96dc8a8f1db395f922bbc9f6ca603672686086b")
    version("9.4p1", sha256="3608fd9088db2163ceb3e600c85ab79d0de3d221e59192ea1923e23263866a85")
    version("9.3p1", sha256="e9baba7701a76a51f3d85a62c383a3c9dcd97fa900b859bc7db114c1868af8a8")
    version("9.2p1", sha256="3f66dbf1655fb45f50e1c56da62ab01218c228807b21338d634ebcdf9d71cf46")
    version("9.1p1", sha256="19f85009c7e3e23787f0236fbb1578392ab4d4bf9f8ec5fe6bc1cd7e8bfdd288")
    version("9.0p1", sha256="03974302161e9ecce32153cfa10012f1e65c8f3750f573a73ab1befd5972a28a")
    version("8.9p1", sha256="fd497654b7ab1686dac672fb83dfb4ba4096e8b5ffcdaccd262380ae58bec5e7")
    version("8.8p1", sha256="4590890ea9bb9ace4f71ae331785a3a5823232435161960ed5fc86588f331fe9")
    version("8.7p1", sha256="7ca34b8bb24ae9e50f33792b7091b3841d7e1b440ff57bc9fabddf01e2ed1e24")
    version("8.6p1", sha256="c3e6e4da1621762c850d03b47eed1e48dff4cc9608ddeb547202a234df8ed7ae")
    version("8.5p1", sha256="f52f3f41d429aa9918e38cf200af225ccdd8e66f052da572870c89737646ec25")
    version("8.4p1", sha256="5a01d22e407eb1c05ba8a8f7c654d388a13e9f226e4ed33bd38748dafa1d2b24")
    version("8.3p1", sha256="f2befbe0472fe7eb75d23340eb17531cb6b3aac24075e2066b41f814e12387b2")
    version("8.1p1", sha256="02f5dbef3835d0753556f973cd57b4c19b6b1f6cd24c03445e23ac77ca1b93ff")
    version("7.9p1", sha256="6b4b3ba2253d84ed3771c8050728d597c91cfce898713beb7b64a305b6f11aad")
    version("7.6p1", sha256="a323caeeddfe145baaa0db16e98d784b1fbc7dd436a6bf1f479dfd5cd1d21723")
    version("7.5p1", sha256="9846e3c5fab9f0547400b4d2c017992f914222b3fd1f8eee6c7dc6bc5e59f9f0")
    version("7.4p1", sha256="1b1fc4a14e2024293181924ed24872e6f2e06293f3e8926a376b8aec481f19d1")
    version("7.3p1", sha256="3ffb989a6dcaa69594c3b550d4855a5a2e1718ccdde7f5e36387b424220fbecc")
    version("7.2p2", sha256="a72781d1a043876a224ff1b0032daa4094d87565a68528759c1c2cab5482548c")
    version("7.1p2", sha256="dd75f024dcf21e06a0d6421d582690bf987a1f6323e32ad6619392f3bfde6bbd")
    version("7.0p1", sha256="fd5932493a19f4c81153d812ee4e042b49bbd3b759ab3d9344abecc2bc1485e5")
    version("6.9p1", sha256="6e074df538f357d440be6cf93dc581a21f22d39e236f217fcd8eacbb6c896cfe")
    version("6.8p1", sha256="3ff64ce73ee124480b5bf767b9830d7d3c03bbcb6abe716b78f0192c37ce160e")
    version("6.7p1", sha256="b2f8394eae858dabbdef7dac10b99aec00c95462753e80342e530bbb6f725507")
    version("6.6p1", sha256="48c1f0664b4534875038004cc4f3555b8329c2a81c1df48db5c517800de203bb")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "gssapi", default=True, description="Enable authentication via Kerberos through GSSAPI"
    )

    depends_on("krb5+shared", when="+gssapi")
    depends_on("openssl@:1.0", when="@:7.7p1")
    depends_on("openssl@:1.1", when="@:7.9p1")
    # 8.7 and earlier don't support openssl@3.1:
    depends_on("openssl@:3.0", when="@:8.7p1")
    depends_on("openssl")
    depends_on("libedit")
    depends_on("ncurses")
    depends_on("zlib-api")
    depends_on("py-twisted", type="test")
    depends_on("libxcrypt", type="link")

    maintainers("bernhardkaindl")
    executables = [
        "^ssh$",
        "^scp$",
        "^sftp$",
        "^ssh-add$",
        "^ssh-agent$",
        "^ssh-keygen$",
        "^ssh-keyscan$",
    ]

    # Both these patches are applied by Apple.
    # https://github.com/Homebrew/homebrew-core/blob/7aabdeb30506be9b01708793ae553502c115dfc8/Formula/o/openssh.rb#L40-L45
    patch(
        "https://raw.githubusercontent.com/Homebrew/patches/1860b0a745f1fe726900974845d1b0dd3c3398d6/openssh/patch-sandbox-darwin.c-apple-sandbox-named-external.diff",
        sha256="d886b98f99fd27e3157b02b5b57f3fb49f43fd33806195970d4567f12be66e71",
        when="platform=darwin",
    )

    # https://github.com/Homebrew/homebrew-core/blob/7aabdeb30506be9b01708793ae553502c115dfc8/Formula/o/openssh.rb#L48-L52C6
    patch(
        "https://raw.githubusercontent.com/Homebrew/patches/d8b2d8c2612fd251ac6de17bf0cc5174c3aab94c/openssh/patch-sshd.c-apple-sandbox-named-external.diff",
        sha256="3505c58bf1e584c8af92d916fe5f3f1899a6b15cc64a00ddece1dc0874b2f78f",
        when="@:9.7p1 platform=darwin",
    )
    # same as above, but against sshd-session.c instead of sshd.c
    patch(
        "https://raw.githubusercontent.com/Homebrew/patches/aa6c71920318f97370d74f2303d6aea387fb68e4/openssh/patch-sshd.c-apple-sandbox-named-external.diff",
        sha256="3f06fc03bcbbf3e6ba6360ef93edd2301f73efcd8069e516245aea7c4fb21279",
        when="@9.8p1: platform=darwin",
    )

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("-V", output=str, error=str).rstrip()
        match = re.search(r"OpenSSH_([^, ]+)", output)
        return match.group(1) if match else None

    def patch(self):
        # #29938: skip set-suid (also see man ssh-key-sign: it's not enabled by default)
        filter_file(r"\$\(INSTALL\) -m 4711", "$(INSTALL) -m711", "Makefile.in")
        # #39599: fix configure to parse zlib 1.3's version number to prevent build fail
        filter_file(r"if \(n != 3 && n != 4\)", "if (n < 2)", "configure")

        # Clang-based compilers (known at least 14-17) may randomly mis-compile
        # openssh according to this thread even when -fzero-call-used-regs=used:
        # https://www.mail-archive.com/openssh-bugs@mindrot.org/msg17461.html
        # Therefore, remove -fzero-call-used-regs=all for these compilers:
        spec = self.spec
        if spec.version < Version("9.6p1") and self.compiler.name.endswith(("clang", "oneapi")):
            filter_file("-fzero-call-used-regs=all", "", "configure")

    def configure_args(self):
        # OpenSSH's privilege separation path defaults to /var/empty. At
        # least newer versions want to create the directory during the
        # install step and fail if they cannot do so.
        args = ["--with-privsep-path={0}".format(self.prefix.var.empty)]
        if self.spec.satisfies("+gssapi"):
            args.append("--with-kerberos5=" + self.spec["krb5"].prefix)

        # Somehow creating pie executables fails with nvhpc, not with gcc.
        if "%nvhpc" in self.spec:
            args.append("--without-pie")
        return args

    def install(self, spec, prefix):
        """Install generates etc/sshd_config, but it fails in parallel mode"""
        make("install", parallel=False)

    def setup_build_environment(self, env):
        """Until spack supports a real implementation of setup_test_environment()"""
        if self.run_tests:
            self.setup_test_environment(env)

        # https://github.com/Homebrew/homebrew-core/blob/7aabdeb30506be9b01708793ae553502c115dfc8/Formula/o/openssh.rb#L65C31-L65C65
        # to use the MacOS patches
        if self.spec.platform == "darwin":
            env.append_flags("CPPFLAGS", "-D__APPLE_SANDBOX_NAMED_EXTERNAL__")
        # For "@:7": Newer compilers use -fno-common by default and fail on tun_fwd_ifnames:
        if self.spec.satisfies("@:7 %gcc@10:") or self.spec.satisfies("@:7 %clang@11:"):
            env.append_flags("CFLAGS", "-fcommon")

    def setup_test_environment(self, env):
        """Configure the regression test suite like Debian's openssh-tests package"""
        p = self.prefix
        j = join_path
        env.set("TEST_SSH_SSH", p.bin.ssh)
        env.set("TEST_SSH_SCP", p.bin.scp)
        env.set("TEST_SSH_SFTP", p.bin.sftp)
        env.set("TEST_SSH_SK_HELPER", j(p.libexec, "ssh-sk-helper"))
        env.set("TEST_SSH_SFTPSERVER", j(p.libexec, "sftp-server"))
        env.set("TEST_SSH_PKCS11_HELPER", j(p.libexec, "ssh-pkcs11-helper"))
        env.set("TEST_SSH_SSHD", p.sbin.sshd)
        env.set("TEST_SSH_SSHADD", j(p.bin, "ssh-add"))
        env.set("TEST_SSH_SSHAGENT", j(p.bin, "ssh-agent"))
        env.set("TEST_SSH_SSHKEYGEN", j(p.bin, "ssh-keygen"))
        env.set("TEST_SSH_SSHKEYSCAN", j(p.bin, "ssh-keyscan"))
        env.set("TEST_SSH_UNSAFE_PERMISSIONS", "1")
        # Get a free port for the simple tests and skip the complex tests:
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.bind(("", 0))
        host, port = tcp.getsockname()
        tcp.close()
        env.set("TEST_SSH_PORT", port)
        env.set(
            "SKIP_LTESTS",
            "key-options forward-control forwarding "
            "multiplex addrmatch cfgmatch cfgmatchlisten percent",
        )

    def installcheck(self):
        make("-e", "tests", parallel=False)
