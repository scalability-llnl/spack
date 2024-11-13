# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack.package import *
from spack.util.environment import is_system_path


class Git(AutotoolsPackage):
    """Git is a free and open source distributed version control
    system designed to handle everything from small to very large
    projects with speed and efficiency.
    """

    homepage = "https://git-scm.com"
    url = "https://mirrors.edge.kernel.org/pub/software/scm/git/git-2.12.0.tar.gz"
    maintainers("jennfshr")

    tags = ["build-tools"]

    executables = ["^git$"]

    license("GPL-2.0-only")

    # Every new git release comes with a corresponding manpage resource:
    # https://www.kernel.org/pub/software/scm/git/git-manpages-{version}.tar.gz
    # https://mirrors.edge.kernel.org/pub/software/scm/git/sha256sums.asc
    version("2.45.2", sha256="98b26090ed667099a3691b93698d1e213e1ded73d36a2fde7e9125fce28ba234")
    version("2.44.2", sha256="f0655e81c5ecfeef7440aa4fcffa1c1a77eaccf764d6fe29579e9a06eac2cd04")
    version("2.43.5", sha256="324c3b85d668e6afe571b3502035848e4b349dead35188e2b8ab1b96c0cd45ff")
    version("2.42.3", sha256="f42a8e8f6c0add4516f9e4607554c8ad698161b7d721b82073fe315a59621961")
    version("2.41.2", sha256="481aa0a15aa37802880a6245b96c1570d7337c44700d5d888344cd6d43d85306")
    version("2.40.3", sha256="b3dc96b20edcdbe6bea7736ea55bb80babf683d126cc7f353ed4e3bc304cd7da")
    version("2.39.5", sha256="ca0ec03fb2696f552f37135a56a0242fa062bd350cb243dc4a15c86f1cafbc99")

    # Deprecated versions (https://groups.google.com/g/git-packagers/c/x6-nKLV20aE)
    version(
        "2.45.1",
        sha256="10acb581993061e616be9c5674469335922025a666318e0748cb8306079fef24",
        deprecated=True,
    )
    version(
        "2.44.1",
        sha256="118214bb8d7ba971a62741416e757562b8f5451cefc087a407e91857897c92cc",
        deprecated=True,
    )
    version(
        "2.43.4",
        sha256="bfd717dc31922f718232a25a929d199e26146df5e876fdf0ff90a7cc95fa06e2",
        deprecated=True,
    )
    version(
        "2.42.2",
        sha256="3b24b712fa6e9a3da5b7d3e68b1854466905aadb93a43088a38816bcc3b9d043",
        deprecated=True,
    )
    version(
        "2.41.1",
        sha256="06d2a681aa7f1bdb6e7f7101631407e7412faa534e1fa0eb6fdcb9975d867d31",
        deprecated=True,
    )
    version(
        "2.40.2",
        sha256="1dcdfbb4eeb3ef2c2d9154f888d4a6f0cf19f19acad76f0d32e725e7bc147753",
        deprecated=True,
    )
    version(
        "2.39.4",
        sha256="b895ed2b5d98fd3dcfde5807f16d5fb17c4f83044e7d08e597ae13de222f0d26",
        deprecated=True,
    )

    # Deprecated versions (see https://github.blog/2024-05-14-securing-git-addressing-5-new-vulnerabilities/).
    version(
        "2.42.0",
        sha256="34aedd54210d7216a55d642bbb4cfb22695b7610719a106bf0ddef4c82a8beed",
        deprecated=True,
    )
    version(
        "2.41.0",
        sha256="c4a6a3dd1827895a80cbd824e14d94811796ae54037549e0da93f7b84cb45b9f",
        deprecated=True,
    )
    version(
        "2.40.1",
        sha256="55511f10f3b1cdf5db4e0e3dea61819dfb67661b0507a5a2b061c70e4f87e14c",
        deprecated=True,
    )
    version(
        "2.39.3",
        sha256="2f9aa93c548941cc5aff641cedc24add15b912ad8c9b36ff5a41b1a9dcad783e",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated

    for _version, _sha256_manpage in {
        "2.45.2": "48c1e2e3ecbb2ce9faa020a19fcdbc6ce64ea25692111b5930686bc0bb4f0e7f",
        "2.45.1": "d9098fd93a3c0ef242814fc856a99886ce31dae2ba457afc416ba4e92af8f8f5",
        "2.44.2": "ee6a7238d5ede18fe21c0cc2131c7fbff1f871c25e2848892ee864d40baf7218",
        "2.44.1": "8d80359e44cbcce256c1eb1389cb8e15ccfcd267fbb8df567d5ce19ce006eb42",
        "2.43.5": "df3c3d0f0834959aa33005e6f8134c1e56ab01f34d1497ceb34b2dd8ec7d4de4",
        "2.43.4": "99d3a0394a6093237123237fd6c0d3de1041d5ceaedc3bfc016807914275d3e2",
        "2.42.3": "3c8c55dcbc3f59560c63e6ced400f7251e9a00d876d365cb4fe9be6b3c3e3713",
        "2.42.2": "2ddfa2187fdaf9ab2b27c0ab043e46793127c26c82a824ffe980f006be049286",
        "2.42.0": "51643c53d70ce15dde83b6da2bad76ba0c7bbcd4f944d7c378f03a15b9f2e1de",
        "2.41.2": "a758988c81478a942e1593ecf11568b962506bff1119061bad04bd4149b40c2c",
        "2.41.1": "7093ef7dacfa8cdb3c4689d8bc1f06186d9b2420bec49087a3a6a4dee26ddcec",
        "2.41.0": "7b77c646b36d33c5c0f62677a147142011093270d6fd628ca38c42d5301f3888",
        "2.40.3": "fa9b837e1e161ebdbbbfde27a883a90fe5f603ce1618086a384bccda59c47de5",
        "2.40.2": "2c71f3f3e4801176f97708f2093756bce672ef260c6d95c255046e6727b3a031",
        "2.40.1": "6bbde434121bd0bf8aa574c60fd9a162388383679bd5ddd99921505149ffd4c2",
        "2.39.5": "16aac22749bd55d845c422068702781a9c89e6cdde7de1c3aa1dd0fb41aeae39",
        "2.39.4": "fedd01dd22a15b84bcbcad68c1b37113ba2c64381c19b6c9f3aa9b2818e126dc",
        "2.39.3": "c8377b5a3ff497d7e6377363c270931496e982509ff27a1e46956d6637671642",
    }.items():
        resource(
            name="git-manpages",
            url=f"https://www.kernel.org/pub/software/scm/git/git-manpages-{_version}.tar.gz",
            sha256=_sha256_manpage,
            placement="git-manpages",
            when=f"@{_version} +man",
        )

    variant("tcltk", default=False, description="Gitk: provide Tcl/Tk in the run environment")
    variant("svn", default=False, description="Provide SVN Perl dependency in run environment")
    variant("perl", default=True, description="Do not use Perl scripts or libraries at all")
    variant("nls", default=True, description="Enable native language support")
    variant("man", default=True, description="Install manual pages")
    variant("subtree", default=True, description="Add git-subtree command and capability")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("curl")
    depends_on("expat")
    depends_on("gettext", when="+nls")
    depends_on("iconv")
    depends_on("libidn2")
    depends_on("openssl")
    depends_on("pcre2")
    depends_on("perl", when="+perl")
    depends_on("zlib-api")
    depends_on("openssh", type="run")
    depends_on("perl-alien-svn", type="run", when="+svn")
    depends_on("tk", type=("build", "link"), when="+tcltk")

    conflicts("+svn", when="~perl")

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(spack.fetch_strategy.GitFetchStrategy.git_version_re, output)
        return match.group(1) if match else None

    @classmethod
    def determine_variants(cls, exes, version_str):
        prefix = os.path.dirname(exes[0])
        variants = ""
        if "gitk" in os.listdir(prefix):
            variants += "+tcltk"
        else:
            variants += "~tcltk"
        return variants

    # See the comment in setup_build_environment re EXTLIBS.
    def patch(self):
        filter_file(r"^EXTLIBS =$", "#EXTLIBS =", "Makefile")

    def setup_build_environment(self, env):
        # We use EXTLIBS rather than LDFLAGS so that git's Makefile
        # inserts the information into the proper place in the link commands
        # (alongside the # other libraries/paths that configure discovers).
        # LDFLAGS is inserted *before* libgit.a, which requires libintl.
        # EXTFLAGS is inserted *after* libgit.a.
        # This depends on the patch method above, which keeps the Makefile
        # from stepping on the value that we pass in via the environment.
        #
        # The test avoids failures when git is an external package.
        # In that case the node in the DAG gets truncated and git DOES NOT
        # have a gettext dependency.
        spec = self.spec
        if spec.satisfies("+nls"):
            if "intl" in spec["gettext"].libs.names:
                extlib_bits = []
                if not is_system_path(spec["gettext"].prefix):
                    extlib_bits.append(spec["gettext"].libs.search_flags)
                extlib_bits.append("-lintl")
                env.append_flags("EXTLIBS", " ".join(extlib_bits))

        if not self.spec["curl"].satisfies("libs=shared"):
            curlconfig = which(os.path.join(self.spec["curl"].prefix.bin, "curl-config"))
            # For configure step:
            env.append_flags("LIBS", curlconfig("--static-libs", output=str).strip())
            # For build step:
            env.append_flags("EXTLIBS", curlconfig("--static-libs", output=str).strip())

        if self.spec.satisfies("~perl"):
            env.append_flags("NO_PERL", "1")

    def configure_args(self):
        spec = self.spec

        configure_args = [
            "--with-curl={0}".format(spec["curl"].prefix),
            "--with-expat={0}".format(spec["expat"].prefix),
            "--with-openssl={0}".format(spec["openssl"].prefix),
            "--with-zlib={0}".format(spec["zlib-api"].prefix),
        ]

        if self.spec["iconv"].name == "libiconv":
            configure_args.append(f"--with-iconv={self.spec['iconv'].prefix}")

        if self.spec.satisfies("+perl"):
            configure_args.append("--with-perl={0}".format(spec["perl"].command.path))

        if self.spec.satisfies("^pcre"):
            configure_args.append("--with-libpcre={0}".format(spec["pcre"].prefix))
        if self.spec.satisfies("^pcre2"):
            configure_args.append("--with-libpcre2={0}".format(spec["pcre2"].prefix))
        if self.spec.satisfies("+tcltk"):
            configure_args.append("--with-tcltk={0}".format(self.spec["tk"].prefix.bin.wish))
        else:
            configure_args.append("--without-tcltk")

        return configure_args

    @run_after("configure")
    def filter_rt(self):
        if self.spec.satisfies("platform=darwin"):
            # Don't link with -lrt; the system has no (and needs no) librt
            filter_file(r" -lrt$", "", "Makefile")

    def check(self):
        make("test")

    def build(self, spec, prefix):
        args = []
        if self.spec.satisfies("~nls"):
            args.append("NO_GETTEXT=1")
        make(*args)

        if spec.satisfies("platform=darwin"):
            with working_dir("contrib/credential/osxkeychain"):
                make()

    def install(self, spec, prefix):
        args = ["install"]
        if self.spec.satisfies("~nls"):
            args.append("NO_GETTEXT=1")
        make(*args)

        if spec.satisfies("platform=darwin"):
            install(
                "contrib/credential/osxkeychain/git-credential-osxkeychain",
                join_path(prefix, "libexec", "git-core"),
            )

    @run_after("install")
    def install_completions(self):
        mkdirp(bash_completion_path(self.prefix))
        install(
            "contrib/completion/git-completion.bash",
            join_path(bash_completion_path(self.prefix), "git"),
        )

        mkdirp(zsh_completion_path(self.prefix))
        filter_file(
            r"\$bash_completion\/git",
            join_path(bash_completion_path(self.prefix), "git"),
            "contrib/completion/git-completion.zsh",
        )
        install(
            "contrib/completion/git-completion.zsh",
            join_path(zsh_completion_path(self.prefix), "_git"),
        )

    @run_after("install")
    def install_manpages(self):
        if self.spec.satisfies("~man"):
            return

        prefix = self.prefix

        with working_dir("git-manpages"):
            install_tree("man1", prefix.share.man.man1)
            install_tree("man5", prefix.share.man.man5)
            install_tree("man7", prefix.share.man.man7)

    @run_after("install")
    def install_subtree(self):
        if self.spec.satisfies("+subtree"):
            with working_dir("contrib/subtree"):
                make_args = ["V=1", "prefix={}".format(self.prefix.bin)]
                make(" ".join(make_args))
                install_args = ["V=1", "prefix={}".format(self.prefix.bin), "install"]
                make(" ".join(install_args))
                install("git-subtree", self.prefix.bin)

    def setup_run_environment(self, env):
        # Setup run environment if using SVN extension
        # Libs from perl-alien-svn and apr-util are required in
        # LD_LIBRARY_PATH
        # TODO: extend to other platforms
        if self.spec.satisfies("+svn platform=linux"):
            perl_svn = self.spec["perl-alien-svn"]
            env.prepend_path(
                "LD_LIBRARY_PATH",
                join_path(
                    perl_svn.prefix, "lib", "perl5", "x86_64-linux-thread-multi", "Alien", "SVN"
                ),
            )
