# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import platform

from spack.package import *


class Latex2html(AutotoolsPackage):
    """LaTeX2HTML is a utility that converts LaTeX documents to web pages in HTML."""

    homepage = "https://www.latex2html.org/"
    url = "https://github.com/latex2html/latex2html/archive/refs/tags/v2024.tar.gz"
    git = "https://github.com/latex2html/latex2html.git"

    maintainers("cessenat")

    license("GPL-2.0-only")

    version("master", branch="master")
    version("2024", sha256="554a51f83431683521b9e47a19edf07c90960feb040048a08ad8301bdca2c6fa")
    version("2023.2", sha256="2a3f50621a71c9c0c425fb6709ae69bb2cf4df4bfe72ac661c2ea302e5aba185")
    version("2022.2", sha256="b1d5bba7bab7d0369d1241f2d8294137a52b7cb7df11239bfa15ec0a2546c093")
    version("2021", sha256="872fe7a53f91ababaafc964847639e3644f2b9fab3282ea059788e4e18cbba47")
    version("2017", sha256="28a5d4b8f14b1f95928da281b6332559bcd83349ba439b2fa43655b2e21c83ab")

    variant("svg", default=True, description="Enable SVG images")
    variant("png", default=True, description="Enable PNG images")
    variant("gif", default=True, description="Enable GIF images")

    depends_on("ghostscript", type=("build", "run"))
    depends_on("perl", type=("build", "run"))
    # Provides pdfcrop scheme=full
    depends_on("texlive", type=("build", "run"))

    depends_on("netpbm", type=("build", "run"))
    # Provides pdftocairo
    depends_on("poppler+glib", type=("build", "run"), when="+svg")

    def url_for_version(self, version):
        return f"https://github.com/latex2html/latex2html/archive/refs/tags/v{version}.tar.gz"

    # A copy of texlive function as long as it does not provide the
    # bin env to dependent package:
    def tex_arch(self):
        tex_arch = "{0}-{1}".format(platform.machine(), platform.system().lower())
        return tex_arch

    def configure_args(self):
        spec = self.spec
        args = ["--with-perl={0}".format(spec["perl"].command.path)]
        args.extend(self.enable_or_disable("png"))
        args.extend(self.enable_or_disable("gif"))
        args.extend(self.enable_or_disable("svg"))

        # Since packages do not always provide a proper dependent_build_environment,
        # one needs to guess where the bins are since latex2html configure wants to
        # hard set the bins location once for all:
        for p in ["gs", "ps2pdf"]:
            exe = join_path(spec["ghostscript"].prefix.bin, p)
            if os.path.exists(exe):
                args.append("--with-{0}={1}".format(p, exe))
        pnms = [
            "pnmcrop",
            "pnmflip",
            "ppmquant",
            "pnmfile",
            "pnmcat",
            "pbmmake",
            "ppmtogif",
            "pnmtopng",
            "ppmtojpeg",
            "pnmcut",
            "pnmpad",
            "pnmrotate",
            "pnmscale",
            "giftopnm",
            "jpegtopnm",
            "pngtopnm",
            "tifftopnm",
            "anytopnm",
            "bmptoppm",
            "pcxtoppm",
            "sgitopnm",
            "xbmtopbm",
            "xwdtopnm",
        ]
        for p in pnms:
            exe = join_path(spec["netpbm"].prefix.bin, p)
            if os.path.exists(exe):
                args.append("--with-{0}={1}".format(p, exe))

        # PR #24102 at https://github.com/spack/spack/pull/24102
        # should make this useless ; but at least it lets us know which are the
        # texlive bins that latex2html may use.
        lats = [
            "pdfcrop",
            "tex",
            "initex",
            "latex",
            "dvips",
            "dvipng",
            "pdflatex",
            "lualatex",
            "dvilualatex",
            "kpsewhich",
            "mktexlsr",
        ]
        for p in lats:
            exe = join_path(spec["texlive"].prefix.bin, self.tex_arch(), p)
            if os.path.exists(exe):
                args.append("--with-{0}={1}".format(p, exe))
            else:
                # This should be the only needed code if texlive where
                # to set its proper dependent_build_environment
                exe = which(p)
                if exe:
                    args.append("--with-{0}={1}".format(p, str(exe)))
        if spec.satisfies("+svg"):
            p = "pdftocairo"
            exe = join_path(spec["poppler"].prefix.bin, p)
            if os.path.exists(exe):
                args.append("--with-{0}={1}".format(p, exe))
            else:
                exe = which(p)
                if exe:
                    args.append("--with-{0}={1}".format(p, str(exe)))

        return args
