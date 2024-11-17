# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gh(GoPackage):
    """GitHub's official command line tool."""

    homepage = "https://github.com/cli/cli"
    url = "https://github.com/cli/cli/archive/refs/tags/v2.0.0.tar.gz"

    maintainers("lcnzg")

    license("MIT")

    version("2.58.0", sha256="90894536c797147586db775d06ec2040c45cd7eef941f7ccbea46f4e5997c81c")
    version("2.50.0", sha256="683d0dee90e1d24a6673d13680e0d41963ddc6dd88580ab5119acec790d1b4d7")
    version("2.49.2", sha256="e839ea302ad99b70ce3efcb903f938ecbbb919798e49bc2f2034ad506ae0b0f5")
    version("2.43.1", sha256="1ea3f451fb7002c1fb95a7fab21e9ab16591058492628fe264c5878e79ec7c90")
    version("2.32.1", sha256="1d569dc82eb6520e6a8959568c2db84fea3bbaab2604c8dd5901849d320e1eae")
    version("2.28.0", sha256="cf3c0fb7f601d717d8b5177707a197c49fd426f5dc3c9aa52a932e96ba7166af")
    version("2.25.1", sha256="d3b28da03f49600697d2e80c2393425bd382e340040c34641bf3569593c7fbe8")
    version("2.25.0", sha256="b445dbb863643d30cc7991b134c694ea14492e7fac363a9e2648f245f67184f7")
    version("2.24.3", sha256="f5c8a273d3adabee9d4a07d38e738df589f1e9dcdae03f9c7b8e3d8aa4b58cf4")
    version("2.23.0", sha256="1e9f92a47caa92efedc06b22cfe9c951c5163c4a9bc60a45d477fd5d9b592e54")
    version("2.5.1", sha256="89aac9c35ad875f1b17144bf9fcbfa7231554d4abce187d9277fcc83da846e4a")
    version("2.5.0", sha256="4e9d1cbcdd2346cab5b7fc176cd57c07ed3628a0241fad8a48fe4df6a354b120")
    version("2.4.0", sha256="3c87db4d9825a342fc55bd7f27461099dd46291aea4a4a29bb95d3c896403f94")
    version("2.3.0", sha256="56bcf353adc17c386377ffcdfc980cbaff36123a1c1132ba09c3c51a7d1c9b82")
    version("2.2.0", sha256="597c6c1cde4484164e9320af0481e33cfad2330a02315b4c841bdc5b7543caec")
    version("2.1.0", sha256="4b353b121a0f3ddf5046f0a1ae719a0539e0cddef27cc78a1b33ad7d1d22c007")
    version("2.0.0", sha256="5d93535395a6684dee1d9d1d3cde859addd76f56581e0111d95a9c685d582426")
    version("1.14.0", sha256="1a99050644b4821477aabc7642bbcae8a19b3191e9227cd8078016d78cdd83ac")
    version("1.13.1", sha256="1a19ab2bfdf265b5e2dcba53c3bd0b5a88f36eff4864dcc38865e33388b600c5")

    conflicts("platform=darwin", when="@2.28.0")

    depends_on("go@1.16:", type="build")
    depends_on("go@1.18:", type="build", when="@2.10.0:")
    depends_on("go@1.19:", type="build", when="@2.21.0:")
    depends_on("go@1.21:", type="build", when="@2.33.0:")
    depends_on("go@1.22:", type="build", when="@2.47.0:")

    @property
    def build_args(self):
        args = super().build_args
        args.extend(["-trimpath", "./cmd/gh"])
        return args

    @run_after("install")
    def install_completions(self):
        gh = Executable(self.prefix.bin.gh)

        mkdirp(bash_completion_path(self.prefix))
        with open(bash_completion_path(self.prefix) / "gh", "w") as file:
            gh("completion", "-s", "bash", output=file)

        mkdirp(fish_completion_path(self.prefix))
        with open(fish_completion_path(self.prefix) / "gh.fish", "w") as file:
            gh("completion", "-s", "fish", output=file)

        mkdirp(zsh_completion_path(self.prefix))
        with open(zsh_completion_path(self.prefix) / "_gh", "w") as file:
            gh("completion", "-s", "zsh", output=file)
