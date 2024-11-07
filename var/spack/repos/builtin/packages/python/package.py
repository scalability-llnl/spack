# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import json
import os
import platform
import re
import subprocess
import sys
from shutil import copy
from typing import Dict, List

import llnl.util.tty as tty
from llnl.util.lang import dedupe

from spack.build_environment import dso_suffix, stat_suffix
from spack.package import *
from spack.util.prefix import Prefix


def make_pyvenv_cfg(python_spec: "spack.spec.Spec", venv_prefix: str) -> str:
    """Make a pyvenv_cfg file for a given (real) python command and venv prefix."""
    python_cmd = python_spec.command.path
    lines = [
        # directory containing python command
        f"home = {os.path.dirname(python_cmd)}",
        # venv should not allow site packages from the real python to be loaded
        "include-system-site-packages = false",
        # version of the python command
        f"version = {python_spec.version}",
        # the path to the python command
        f"executable = {python_cmd}",
        # command "used" to create the pyvenv.cfg
        f"command = {python_cmd} -m venv --without-pip {venv_prefix}",
    ]

    return "\n".join(lines) + "\n"


class Python(Package):
    """The Python programming language."""

    homepage = "https://www.python.org/"
    url = "https://www.python.org/ftp/python/3.8.0/Python-3.8.0.tgz"
    list_url = "https://www.python.org/ftp/python/"
    list_depth = 1
    tags = ["windows"]

    maintainers("skosukhin", "scheibelp")

    phases = ["configure", "build", "install"]

    #: phase
    install_targets = ["install"]
    build_targets: List[str] = []

    license("0BSD")

    version("3.13.0", sha256="12445c7b3db3126c41190bfdc1c8239c39c719404e844babbd015a1bc3fafcd4")
    version("3.12.5", sha256="38dc4e2c261d49c661196066edbfb70fdb16be4a79cc8220c224dfeb5636d405")
    version("3.12.4", sha256="01b3c1c082196f3b33168d344a9c85fb07bfe0e7ecfe77fee4443420d1ce2ad9")
    version("3.12.3", sha256="a6b9459f45a6ebbbc1af44f5762623fa355a0c87208ed417628b379d762dddb0")
    version("3.12.2", sha256="a7c4f6a9dc423d8c328003254ab0c9338b83037bd787d680826a5bf84308116e")
    version("3.12.1", sha256="d01ec6a33bc10009b09c17da95cc2759af5a580a7316b3a446eb4190e13f97b2")
    version("3.12.0", sha256="51412956d24a1ef7c97f1cb5f70e185c13e3de1f50d131c0aac6338080687afb")
    version("3.11.9", sha256="e7de3240a8bc2b1e1ba5c81bf943f06861ff494b69fda990ce2722a504c6153d")
    version("3.11.8", sha256="d3019a613b9e8761d260d9ebe3bd4df63976de30464e5c0189566e1ae3f61889")
    version("3.11.7", sha256="068c05f82262e57641bd93458dfa883128858f5f4997aad7a36fd25b13b29209")
    version("3.11.6", sha256="c049bf317e877cbf9fce8c3af902436774ecef5249a29d10984ca3a37f7f4736")
    version("3.11.5", sha256="a12a0a013a30b846c786c010f2c19dd36b7298d888f7c4bd1581d90ce18b5e58")
    version("3.11.4", sha256="85c37a265e5c9dd9f75b35f954e31fbfc10383162417285e30ad25cc073a0d63")
    version("3.11.3", sha256="1a79f3df32265d9e6625f1a0b31c28eb1594df911403d11f3320ee1da1b3e048")
    version("3.11.2", sha256="2411c74bda5bbcfcddaf4531f66d1adc73f247f529aee981b029513aefdbf849")
    version("3.11.1", sha256="baed518e26b337d4d8105679caf68c5c32630d702614fc174e98cb95c46bdfa4")
    version("3.11.0", sha256="64424e96e2457abbac899b90f9530985b51eef2905951febd935f0e73414caeb")
    version("3.10.14", sha256="cefea32d3be89c02436711c95a45c7f8e880105514b78680c14fe76f5709a0f6")
    version("3.10.13", sha256="698ec55234c1363bd813b460ed53b0f108877c7a133d48bde9a50a1eb57b7e65")
    version("3.10.12", sha256="a43cd383f3999a6f4a7db2062b2fc9594fefa73e175b3aedafa295a51a7bb65c")
    version("3.10.11", sha256="f3db31b668efa983508bd67b5712898aa4247899a346f2eb745734699ccd3859")
    version("3.10.10", sha256="fba64559dde21ebdc953e4565e731573bb61159de8e4d4cedee70fb1196f610d")
    version("3.10.9", sha256="4ccd7e46c8898f4c7862910a1703aa0e63525913a519abb2f55e26220a914d88")
    version("3.10.8", sha256="f400c3fb394b8bef1292f6dc1292c5fadc3533039a5bc0c3e885f3e16738029a")
    version("3.10.7", sha256="1b2e4e2df697c52d36731666979e648beeda5941d0f95740aafbf4163e5cc126")
    version("3.10.6", sha256="848cb06a5caa85da5c45bd7a9221bb821e33fc2bdcba088c127c58fad44e6343")
    version("3.10.5", sha256="18f57182a2de3b0be76dfc39fdcfd28156bb6dd23e5f08696f7492e9e3d0bf2d")
    version("3.10.4", sha256="f3bcc65b1d5f1dc78675c746c98fcee823c038168fc629c5935b044d0911ad28")
    version("3.10.3", sha256="5a3b029bad70ba2a019ebff08a65060a8b9b542ffc1a83c697f1449ecca9813b")
    version("3.10.2", sha256="3c0ede893011319f9b0a56b44953a3d52c7abf9657c23fb4bc9ced93b86e9c97")
    version("3.10.1", sha256="b76117670e7c5064344b9c138e141a377e686b9063f3a8a620ff674fa8ec90d3")
    version("3.10.0", sha256="c4e0cbad57c90690cb813fb4663ef670b4d0f587d8171e2c42bd4c9245bd2758")
    version("3.9.19", sha256="f5f9ec8088abca9e399c3b62fd8ef31dbd2e1472c0ccb35070d4d136821aaf71")
    version("3.9.18", sha256="504ce8cfd59addc04c22f590377c6be454ae7406cb1ebf6f5a350149225a9354")
    version("3.9.17", sha256="8ead58f669f7e19d777c3556b62fae29a81d7f06a7122ff9bc57f7dd82d7e014")
    version("3.9.16", sha256="1ad539e9dbd2b42df714b69726e0693bc6b9d2d2c8e91c2e43204026605140c5")
    version("3.9.15", sha256="48d1ccb29d5fbaf1fb8f912271d09f7450e426d4dfe95978ef6aaada70ece4d8")
    version("3.9.14", sha256="9201836e2c16361b2b7408680502393737d44f227333fe2e5729c7d5f6041675")
    version("3.9.13", sha256="829b0d26072a44689a6b0810f5b4a3933ee2a0b8a4bfc99d7c5893ffd4f97c44")
    version("3.9.12", sha256="70e08462ebf265012bd2be88a63d2149d880c73e53f1712b7bbbe93750560ae8")
    version("3.9.11", sha256="3442400072f582ac2f0df30895558f08883b416c8c7877ea55d40d00d8a93112")
    version("3.9.10", sha256="1aa9c0702edbae8f6a2c95f70a49da8420aaa76b7889d3419c186bfc8c0e571e")
    version("3.9.9", sha256="2cc7b67c1f3f66c571acc42479cdf691d8ed6b47bee12c9b68430413a17a44ea")
    version("3.9.8", sha256="7447fb8bb270942d620dd24faa7814b1383b61fa99029a240025fd81c1db8283")
    version("3.9.7", sha256="a838d3f9360d157040142b715db34f0218e535333696a5569dc6f854604eb9d1")
    version("3.9.6", sha256="d0a35182e19e416fc8eae25a3dcd4d02d4997333e4ad1f2eee6010aadc3fe866")
    version("3.9.5", sha256="e0fbd5b6e1ee242524430dee3c91baf4cbbaba4a72dd1674b90fda87b713c7ab")
    version("3.9.4", sha256="66c4de16daa74a825cf9da9ddae1fe020b72c3854b73b1762011cc33f9e4592f")
    version("3.9.3", sha256="3afeb61a45b5a2e6f1c0f621bd8cf925a4ff406099fdb3d8c97b993a5f43d048")
    version("3.9.2", sha256="7899e8a6f7946748830d66739f2d8f2b30214dad956e56b9ba216b3de5581519")
    version("3.9.1", sha256="29cb91ba038346da0bd9ab84a0a55a845d872c341a4da6879f462e94c741f117")
    version("3.9.0", sha256="df796b2dc8ef085edae2597a41c1c0a63625ebd92487adaef2fed22b567873e8")
    version("3.8.19", sha256="c7fa55a36e5c7a19ec37d8f90f60a2197548908c9ac8b31e7c0dbffdd470eeac")
    version("3.8.18", sha256="7c5df68bab1be81a52dea0cc2e2705ea00553b67107a301188383d7b57320b16")
    version("3.8.17", sha256="def428fa6cf61b66bcde72e3d9f7d07d33b2e4226f04f9d6fce8384c055113ae")
    version("3.8.16", sha256="71ca9d935637ed2feb59e90a368361dc91eca472a90acb1d344a2e8178ccaf10")
    version("3.8.15", sha256="924d46999df82aa2eaa1de5ca51d6800ffb56b4bf52486a28f40634e3362abc4")
    version("3.8.14", sha256="41f959c480c59211feb55d5a28851a56c7e22d02ef91035606ebb21011723c31")
    version("3.8.13", sha256="903b92d76354366b1d9c4434d0c81643345cef87c1600adfa36095d7b00eede4")
    version("3.8.12", sha256="316aa33f3b7707d041e73f246efedb297a70898c4b91f127f66dc8d80c596f1a")
    version("3.8.11", sha256="b77464ea80cec14581b86aeb7fb2ff02830e0abc7bcdc752b7b4bdfcd8f3e393")
    version("3.8.10", sha256="b37ac74d2cbad2590e7cd0dd2b3826c29afe89a734090a87bf8c03c45066cb65")
    version("3.8.9", sha256="9779ec1df000bf86914cdd40860b88da56c1e61db59d37784beca14a259ac9e9")
    version("3.8.8", sha256="76c0763f048e4f9b861d24da76b7dd5c7a3ba7ec086f40caedeea359263276f7")
    version("3.8.7", sha256="20e5a04262f0af2eb9c19240d7ec368f385788bba2d8dfba7e74b20bab4d2bac")
    version("3.8.6", sha256="313562ee9986dc369cd678011bdfd9800ef62fbf7b1496228a18f86b36428c21")
    version("3.8.5", sha256="015115023c382eb6ab83d512762fe3c5502fa0c6c52ffebc4831c4e1a06ffc49")
    version("3.8.4", sha256="32c4d9817ef11793da4d0d95b3191c4db81d2e45544614e8449255ca9ae3cc18")
    version("3.8.3", sha256="6af6d4d2e010f9655518d0fc6738c7ff7069f10a4d2fbd55509e467f092a8b90")
    version("3.8.2", sha256="e634a7a74776c2b89516b2e013dda1728c89c8149b9863b8cea21946daf9d561")
    version("3.8.1", sha256="c7cfa39a43b994621b245e029769e9126caa2a93571cee2e743b213cceac35fb")
    version("3.8.0", sha256="f1069ad3cae8e7ec467aa98a6565a62a48ef196cb8f1455a245a08db5e1792df")
    version(
        "3.7.17",
        sha256="fd50161bc2a04f4c22a0971ff0f3856d98b4bf294f89740a9f06b520aae63b49",
        deprecated=True,
    )
    version(
        "3.7.16",
        sha256="0cf2da07fa464636755215415909e22eb1d058817af4824bc15af8390d05fb38",
        deprecated=True,
    )
    version(
        "3.7.15",
        sha256="cf2993798ae8430f3af3a00d96d9fdf320719f4042f039380dca79967c25e436",
        deprecated=True,
    )
    version(
        "3.7.14",
        sha256="82b2abf8978caa61a9011d166eede831b32de9cbebc0db8162900fa23437b709",
        deprecated=True,
    )
    version(
        "3.7.13",
        sha256="e405417f50984bc5870c7e7a9f9aeb93e9d270f5ac67f667a0cd3a09439682b5",
        deprecated=True,
    )
    version(
        "3.7.12",
        sha256="33b4daaf831be19219659466d12645f87ecec6eb21d4d9f9711018a7b66cce46",
        deprecated=True,
    )
    version(
        "3.7.11",
        sha256="b4fba32182e16485d0a6022ba83c9251e6a1c14676ec243a9a07d3722cd4661a",
        deprecated=True,
    )
    version(
        "3.7.10",
        sha256="c9649ad84dc3a434c8637df6963100b2e5608697f9ba56d82e3809e4148e0975",
        deprecated=True,
    )
    version(
        "3.7.9",
        sha256="39b018bc7d8a165e59aa827d9ae45c45901739b0bbb13721e4f973f3521c166a",
        deprecated=True,
    )
    version(
        "3.7.8",
        sha256="0e25835614dc221e3ecea5831b38fa90788b5389b99b675a751414c858789ab0",
        deprecated=True,
    )
    version(
        "3.7.7",
        sha256="8c8be91cd2648a1a0c251f04ea0bb4c2a5570feb9c45eaaa2241c785585b475a",
        deprecated=True,
    )
    version(
        "3.7.6",
        sha256="aeee681c235ad336af116f08ab6563361a0c81c537072c1b309d6e4050aa2114",
        deprecated=True,
    )
    version(
        "3.7.5",
        sha256="8ecc681ea0600bbfb366f2b173f727b205bb825d93d2f0b286bc4e58d37693da",
        deprecated=True,
    )
    version(
        "3.7.4",
        sha256="d63e63e14e6d29e17490abbe6f7d17afb3db182dbd801229f14e55f4157c4ba3",
        deprecated=True,
    )
    version(
        "3.7.3",
        sha256="d62e3015f2f89c970ac52343976b406694931742fbde2fed8d1ce8ebb4e1f8ff",
        deprecated=True,
    )
    version(
        "3.7.2",
        sha256="f09d83c773b9cc72421abba2c317e4e6e05d919f9bcf34468e192b6a6c8e328d",
        deprecated=True,
    )
    version(
        "3.7.1",
        sha256="36c1b81ac29d0f8341f727ef40864d99d8206897be96be73dc34d4739c9c9f06",
        deprecated=True,
    )
    version(
        "3.7.0",
        sha256="85bb9feb6863e04fb1700b018d9d42d1caac178559ffa453d7e6a436e259fd0d",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    extendable = True

    # Variants to avoid cyclical dependencies for concretizer
    variant("libxml2", default=True, description="Use a gettext library build with libxml2")

    variant(
        "debug", default=False, description="debug build with extra checks (this is high overhead)"
    )

    variant("shared", default=True, description="Enable shared libraries")
    variant("pic", default=True, description="Produce position-independent code (for shared libs)")
    variant(
        "optimizations",
        default=False,
        description="Enable expensive build-time optimizations, if available",
    )
    # See https://legacy.python.org/dev/peps/pep-0394/
    variant(
        "pythoncmd",
        default=sys.platform != "win32",
        description="Symlink 'python3' executable to 'python' (not PEP 394 compliant)",
    )

    # Optional Python modules
    variant("readline", default=sys.platform != "win32", description="Build readline module")
    variant("ssl", default=True, description="Build ssl module")
    variant("sqlite3", default=True, description="Build sqlite3 module")
    variant("dbm", default=True, description="Build dbm module")
    variant("nis", default=False, description="Build nis module")
    variant("zlib", default=True, description="Build zlib module")
    variant("bz2", default=True, description="Build bz2 module")
    variant("lzma", default=True, description="Build lzma module")
    variant("pyexpat", default=True, description="Build pyexpat module")
    variant("ctypes", default=True, description="Build ctypes module")
    variant("tkinter", default=False, description="Build tkinter module")
    variant("uuid", default=True, description="Build uuid module")
    variant("tix", default=False, description="Build Tix module", when="+tkinter")
    variant("crypt", default=True, description="Build crypt module", when="@:3.12 platform=linux")
    variant("crypt", default=True, description="Build crypt module", when="@:3.12 platform=darwin")

    if sys.platform != "win32":
        depends_on("gmake", type="build")
        depends_on("pkgconfig@0.9.0:", type="build")
        depends_on("gettext +libxml2", when="+libxml2")
        depends_on("gettext ~libxml2", when="~libxml2")

        # Optional dependencies
        # See detect_modules() in setup.py for details
        depends_on("readline", when="+readline")
        depends_on("ncurses", when="+readline")
        depends_on("openssl", when="+ssl")
        # https://docs.python.org/3/whatsnew/3.7.html#build-changes
        depends_on("openssl@1.0.2:", when="+ssl")
        # https://docs.python.org/3.10/whatsnew/3.10.html#build-changes
        depends_on("openssl@1.1.1:", when="@3.10:+ssl")
        depends_on("sqlite@3.0.8:", when="@:3.9+sqlite3")
        # https://docs.python.org/3.10/whatsnew/3.10.html#build-changes
        depends_on("sqlite@3.7.15:", when="@3.10:+sqlite3")
        depends_on("gdbm", when="+dbm")  # alternatively ndbm or berkeley-db
        depends_on("libnsl", when="+nis")
        depends_on("zlib-api", when="+zlib")
        depends_on("bzip2", when="+bz2")
        depends_on("xz libs=shared", when="+lzma")
        depends_on("expat", when="+pyexpat")
        depends_on("libffi", when="+ctypes")
        # https://docs.python.org/3/whatsnew/3.11.html#build-changes
        depends_on("tk@8.5.12:", when="@3.11: +tkinter")
        depends_on("tk", when="+tkinter")
        depends_on("tcl@8.5.12:", when="@3.11: +tkinter")
        depends_on("tcl", when="+tkinter")
        depends_on("uuid", when="+uuid")
        depends_on("tix", when="+tix")
        depends_on("libxcrypt", when="+crypt")

    # Python needs to be patched to build extensions w/ mixed C/C++ code:
    # https://github.com/NixOS/nixpkgs/pull/19585/files
    # https://bugs.python.org/issue1222585
    #
    # NOTE: This patch puts Spack's default Python installation out of
    # sync with standard Python installs. If you're using such an
    # installation as an external and encountering build issues with mixed
    # C/C++ modules, consider installing a Spack-managed Python with
    # this patch instead. For more information, see:
    # https://github.com/spack/spack/pull/16856
    patch("python-3.7.2-distutils-C++.patch", when="@3.7.2")
    patch("python-3.7.3-distutils-C++.patch", when="@3.7.3")
    patch("python-3.7.4+-distutils-C++.patch", when="@3.7.4:3.10")
    patch("python-3.7.4+-distutils-C++-testsuite.patch", when="@3.7.4:3.11")
    patch("python-3.11-distutils-C++.patch", when="@3.11.0:3.11")
    patch("cpython-windows-externals.patch", when="@:3.9.6 platform=windows")
    patch("tkinter-3.7.patch", when="@3.7 platform=darwin")
    # Patch the setup script to deny that tcl/x11 exists rather than allowing
    # autodetection of (possibly broken) system components
    patch("tkinter-3.8.patch", when="@3.8:3.9 ~tkinter")
    patch("tkinter-3.10.patch", when="@3.10.0:3.10 ~tkinter")
    patch("tkinter-3.11.patch", when="@3.11.0:3.11 ~tkinter")

    # Ensure that distutils chooses correct compiler option for RPATH:
    patch("rpath-non-gcc.patch", when="@:3.11")

    # Ensure that distutils chooses correct compiler option for RPATH on fj:
    patch("fj-rpath-3.1.patch", when="@:3.9.7,3.10.0 %fj")
    patch("fj-rpath-3.9.patch", when="@3.9.8:3.9,3.10.1:3.11 %fj")

    # Fixes build with the Intel compilers
    # https://github.com/python/cpython/pull/16717
    patch("intel-3.7.patch", when="@3.7.1:3.7.5 %intel")

    # CPython tries to build an Objective-C file with GCC's C frontend
    # https://github.com/spack/spack/pull/16222
    # https://github.com/python/cpython/pull/13306
    conflicts(
        "%gcc platform=darwin",
        msg="CPython does not compile with GCC on macOS yet, use clang. "
        "See: https://github.com/python/cpython/pull/13306",
    )
    conflicts("%nvhpc")

    # https://bugs.python.org/issue45405
    conflicts("@:3.7.12,3.8.0:3.8.12,3.9.0:3.9.7,3.10.0", when="%apple-clang@13:")

    # See https://github.com/python/cpython/issues/106424
    # datetime.now(timezone.utc) segfaults
    conflicts("@3.9:", when="%oneapi@2022.2.1:2023")

    # Used to cache various attributes that are expensive to compute
    _config_vars: Dict[str, Dict[str, str]] = {}

    # An in-source build with --enable-optimizations fails for python@3.X
    build_directory = "spack-build"

    executables = [r"^python\d?$"]

    @classmethod
    def determine_version(cls, exe):
        # Newer versions of Python support `--version`,
        # but older versions only support `-V`
        # Output looks like:
        #   Python 3.7.7
        # On pre-production Ubuntu, this is also possible:
        #   Python 3.10.2+
        output = Executable(exe)("-V", output=str, error=str)
        match = re.search(r"Python\s+([A-Za-z0-9_.-]+)", output)
        return match.group(1) if match else None

    @classmethod
    def determine_variants(cls, exes, version_str):
        python = Executable(exes[0])

        variants = ""
        for exe in exes:
            if os.path.basename(exe) == "python":
                variants += "+pythoncmd"
                break
        else:
            variants += "~pythoncmd"

        for module in [
            "readline",
            "sqlite3",
            "dbm",
            "nis",
            "zlib",
            "bz2",
            "lzma",
            "ctypes",
            "tkinter",
            "uuid",
        ]:
            try:
                python("-c", "import " + module, error=os.devnull)
                variants += "+" + module
            except ProcessError:
                variants += "~" + module

        # Some variants enable multiple modules
        try:
            python("-c", "import ssl", error=os.devnull)
            python("-c", "import hashlib", error=os.devnull)
            variants += "+ssl"
        except ProcessError:
            variants += "~ssl"

        try:
            python("-c", "import xml.parsers.expat", error=os.devnull)
            python("-c", "import xml.etree.ElementTree", error=os.devnull)
            variants += "+pyexpat"
        except ProcessError:
            variants += "~pyexpat"

        # Some variant names do not match module names
        if "+tkinter" in variants:
            try:
                python("-c", "import tkinter.tix", error=os.devnull)
                variants += "+tix"
            except ProcessError:
                variants += "~tix"

        # Some modules are platform-dependent
        if sys.platform != "win32":
            try:
                python("-c", "import crypt", error=os.devnull)
                variants += "+crypt"
            except ProcessError:
                variants += "~crypt"

        return variants

    def url_for_version(self, version):
        url = "https://www.python.org/ftp/python/{0}/Python-{1}.tgz"
        return url.format(re.split("[a-z]", str(version))[0], version)

    def patch(self):
        # NOTE: Python's default installation procedure makes it possible for a
        # user's local configurations to change the Spack installation.  In
        # order to prevent this behavior for a full installation, we must
        # modify the installation script so that it ignores user files.
        ff = FileFilter("Makefile.pre.in")
        ff.filter(
            r"^(.*)setup\.py(.*)((build)|(install))(.*)$", r"\1setup.py\2 --no-user-cfg \3\6"
        )

    def setup_build_environment(self, env):
        spec = self.spec

        # TODO: Python has incomplete support for Python modules with mixed
        # C/C++ source, and patches are required to enable building for these
        # modules. All Python versions without a viable patch are installed
        # with a warning message about this potentially erroneous behavior.
        if not spec.satisfies("@3.7.2:"):
            tty.warn(
                (
                    'Python v{0} does not have the C++ "distutils" patch; '
                    "errors may occur when installing Python modules w/ "
                    "mixed C/C++ source files."
                ).format(self.version)
            )

        env.unset("PYTHONPATH")
        env.unset("PYTHONHOME")

        # avoid build error on fugaku
        if spec.satisfies("@3.10.0 arch=linux-rhel8-a64fx"):
            if spec.satisfies("%gcc") or spec.satisfies("%fj"):
                env.unset("LC_ALL")

        # https://github.com/python/cpython/issues/87275
        if spec.satisfies("@:3.9.5 +optimizations %apple-clang"):
            xcrun = Executable("/usr/bin/xcrun")
            env.set("LLVM_AR", xcrun("-find", "ar", output=str).strip())

    def flag_handler(self, name, flags):
        # python 3.8 requires -fwrapv when compiled with intel
        if self.spec.satisfies("@3.8: %intel"):
            if name == "cflags":
                flags.append("-fwrapv")

        # Fix for following issues for python with aocc%3.2.0:
        # https://github.com/spack/spack/issues/29115
        # https://github.com/spack/spack/pull/28708
        if self.spec.satisfies("%aocc@3.2.0"):
            if name == "cflags":
                flags.extend(["-mllvm", "-disable-indvar-simplify=true"])

        # allow flags to be passed through compiler wrapper
        return (flags, None, None)

    @property
    def plat_arch(self):
        """
        String referencing platform architecture
        filtered through Python's Windows build file
        architecture support map

        Note: This function really only makes
        sense to use on Windows, could be overridden to
        cross compile however.
        """

        arch_map = {"AMD64": "x64", "x86": "Win32", "IA64": "Win32", "EM64T": "Win32"}
        arch = platform.machine()
        if arch in arch_map:
            arch = arch_map[arch]
        return arch

    @property
    def win_build_params(self):
        """
        Arguments must be passed to the Python build batch script
        in order to configure it to spec and system.
        A number of these toggle optional MSBuild Projects
        directly corresponding to the python support of the same
        name.
        """
        args = []
        args.append("-p %s" % self.plat_arch)
        if self.spec.satisfies("+debug"):
            args.append("-d")
        if self.spec.satisfies("~ctypes"):
            args.append("--no-ctypes")
        if self.spec.satisfies("~ssl"):
            args.append("--no-ssl")
        if self.spec.satisfies("~tkinter"):
            args.append("--no-tkinter")
        return args

    def win_installer(self, prefix):
        """
        Python on Windows does not export an install target
        so we must handcraft one here. This structure
        directly mimics the install tree of the Python
        Installer on Windows.

        Parameters:
            prefix (str): Install prefix for package
        """
        proj_root = self.stage.source_path
        pcbuild_root = os.path.join(proj_root, "PCbuild")
        build_root = os.path.join(pcbuild_root, platform.machine().lower())
        include_dir = os.path.join(proj_root, "Include")
        copy_tree(include_dir, prefix.include)
        doc_dir = os.path.join(proj_root, "Doc")
        copy_tree(doc_dir, prefix.Doc)
        tools_dir = os.path.join(proj_root, "Tools")
        copy_tree(tools_dir, prefix.Tools)
        lib_dir = os.path.join(proj_root, "Lib")
        copy_tree(lib_dir, prefix.Lib)
        pyconfig = os.path.join(proj_root, "PC", "pyconfig.h")
        copy(pyconfig, prefix.include)
        shared_libraries = []
        shared_libraries.extend(glob.glob("%s\\*.exe" % build_root))
        shared_libraries.extend(glob.glob("%s\\*.dll" % build_root))
        shared_libraries.extend(glob.glob("%s\\*.pyd" % build_root))
        os.makedirs(prefix.DLLs)
        for lib in shared_libraries:
            file_name = os.path.basename(lib)
            if (
                file_name.endswith(".exe")
                or (file_name.endswith(".dll") and "python" in file_name)
                or "vcruntime" in file_name
            ):
                copy(lib, prefix)
            else:
                copy(lib, prefix.DLLs)
        static_libraries = glob.glob("%s\\*.lib" % build_root)
        os.makedirs(prefix.libs, exist_ok=True)
        for lib in static_libraries:
            copy(lib, prefix.libs)

    def configure_args(self):
        spec = self.spec
        config_args = []
        cflags = []

        # setup.py needs to be able to read the CPPFLAGS and LDFLAGS
        # as it scans for the library and headers to build
        link_deps = spec.dependencies(deptype="link")

        if link_deps:
            # Header files are often included assuming they reside in a
            # subdirectory of prefix.include, e.g. #include <openssl/ssl.h>,
            # which is why we don't use HeaderList here. The header files of
            # libffi reside in prefix.lib but the configure script of Python
            # finds them using pkg-config.
            cppflags = " ".join("-I" + spec[dep.name].prefix.include for dep in link_deps)

            # Currently, the only way to get SpecBuildInterface wrappers of the
            # dependencies (which we need to get their 'libs') is to get them
            # using spec.__getitem__.
            ldflags = " ".join(spec[dep.name].libs.search_flags for dep in link_deps)

            config_args.extend(["CPPFLAGS=" + cppflags, "LDFLAGS=" + ldflags])

        if "+optimizations" in spec:
            config_args.append("--enable-optimizations")
            # Prefer thin LTO for faster compilation times.
            if "@3.11.0: %clang@3.9:" in spec or "@3.11.0: %apple-clang@8:" in spec:
                config_args.append("--with-lto=thin")
            else:
                config_args.append("--with-lto")
            config_args.append("--with-computed-gotos")

        if spec.satisfies("@3.7 %intel"):
            config_args.append("--with-icc={0}".format(spack_cc))

        if "+debug" in spec:
            config_args.append("--with-pydebug")
        else:
            config_args.append("--without-pydebug")

        if "+shared" in spec:
            config_args.append("--enable-shared")
        else:
            config_args.append("--disable-shared")

        config_args.append("--without-ensurepip")

        if "+pic" in spec:
            cflags.append(self.compiler.cc_pic_flag)

        if "+ssl" in spec:
            config_args.append("--with-openssl={0}".format(spec["openssl"].prefix))

        if "+dbm" in spec:
            # Default order is ndbm:gdbm:bdb
            config_args.append("--with-dbmliborder=gdbm")
        else:
            config_args.append("--with-dbmliborder=")

        if "+pyexpat" in spec:
            config_args.append("--with-system-expat")
        else:
            config_args.append("--without-system-expat")

        if self.version < Version("3.12.0"):
            if "+ctypes" in spec:
                config_args.append("--with-system-ffi")
            else:
                config_args.append("--without-system-ffi")

        if "+tkinter" in spec:
            config_args.extend(
                [
                    "--with-tcltk-includes=-I{0} -I{1}".format(
                        spec["tcl"].prefix.include, spec["tk"].prefix.include
                    ),
                    "--with-tcltk-libs={0} {1}".format(
                        spec["tcl"].libs.ld_flags, spec["tk"].libs.ld_flags
                    ),
                ]
            )

        # https://docs.python.org/3.8/library/sqlite3.html#f1
        if spec.satisfies("+sqlite3 ^sqlite+dynamic_extensions"):
            config_args.append("--enable-loadable-sqlite-extensions")

        if spec.satisfies("%oneapi"):
            cflags.append("-fp-model=strict")

        if cflags:
            config_args.append("CFLAGS={0}".format(" ".join(cflags)))

        if self.version >= Version("3.12.0") and sys.platform == "darwin":
            config_args.append("CURSES_LIBS={0}".format(spec["ncurses"].libs.link_flags))

        return config_args

    def configure(self, spec, prefix):
        """Runs configure with the arguments specified in
        :meth:`~spack.build_systems.autotools.AutotoolsPackage.configure_args`
        and an appropriately set prefix.
        """
        with working_dir(self.stage.source_path, create=True):
            if sys.platform == "win32":
                pass
            else:
                options = getattr(self, "configure_flag_args", [])
                options += ["--prefix={0}".format(prefix)]
                options += self.configure_args()
                configure(*options)

    def build(self, spec, prefix):
        """Makes the build targets specified by
        :py:attr:``~.AutotoolsPackage.build_targets``
        """
        # Windows builds use a batch script to drive
        # configure and build in one step
        with working_dir(self.stage.source_path):
            if sys.platform == "win32":
                pcbuild_root = os.path.join(self.stage.source_path, "PCbuild")
                builder_cmd = os.path.join(pcbuild_root, "build.bat")
                try:
                    subprocess.check_output(  # novermin
                        " ".join([builder_cmd] + self.win_build_params), stderr=subprocess.STDOUT
                    )
                except subprocess.CalledProcessError as e:
                    raise ProcessError(
                        "Process exited with status %d" % e.returncode,
                        long_message=e.output.decode("utf-8"),
                    )
            else:
                # See https://autotools.io/automake/silent.html
                params = ["V=1"]
                params += self.build_targets
                make(*params)

    def install(self, spec, prefix):
        """Makes the install targets specified by
        :py:attr:``~.AutotoolsPackage.install_targets``
        """
        with working_dir(self.stage.source_path):
            if sys.platform == "win32":
                self.win_installer(prefix)
            else:
                # See https://github.com/python/cpython/issues/102007
                make(*self.install_targets, parallel=False)

    @run_after("install")
    def filter_compilers(self):
        """Run after install to tell the configuration files and Makefiles
        to use the compilers that Spack built the package with.

        If this isn't done, they'll have CC and CXX set to Spack's generic
        cc and c++. We want them to be bound to whatever compiler
        they were built with."""
        if sys.platform == "win32":
            return
        kwargs = {"ignore_absent": True, "backup": False, "string": True}

        filenames = [self.get_sysconfigdata_name(), self.config_vars["makefile_filename"]]

        filter_file(spack_cc, self.compiler.cc, *filenames, **kwargs)
        if spack_cxx and self.compiler.cxx:
            filter_file(spack_cxx, self.compiler.cxx, *filenames, **kwargs)

    @run_after("install")
    def symlink(self):
        if sys.platform == "win32":
            return
        spec = self.spec
        prefix = self.prefix

        if spec.satisfies("+pythoncmd"):
            os.symlink(os.path.join(prefix.bin, "python3"), os.path.join(prefix.bin, "python"))
            os.symlink(
                os.path.join(prefix.bin, "python3-config"),
                os.path.join(prefix.bin, "python-config"),
            )

    @run_after("install")
    def install_python_gdb(self):
        # https://devguide.python.org/gdb/
        src = os.path.join("Tools", "gdb", "libpython.py")
        if os.path.exists(src):
            install(src, self.command.path + "-gdb.py")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def import_tests(self):
        """Test that basic Python functionality works."""

        spec = self.spec

        with working_dir("spack-test", create=True):
            # Ensure that readline module works
            if "+readline" in spec:
                self.command("-c", "import readline")

            # Ensure that ssl module works
            if "+ssl" in spec:
                self.command("-c", "import ssl")
                self.command("-c", "import hashlib")

            # Ensure that sqlite3 module works
            if "+sqlite3" in spec:
                self.command("-c", "import sqlite3")

            # Ensure that dbm module works
            if "+dbm" in spec:
                self.command("-c", "import dbm")

            # Ensure that nis module works
            if "+nis" in spec:
                self.command("-c", "import nis")

            # Ensure that zlib module works
            if "+zlib" in spec:
                self.command("-c", "import zlib")

            # Ensure that bz2 module works
            if "+bz2" in spec:
                self.command("-c", "import bz2")

            # Ensure that lzma module works
            if "+lzma" in spec:
                self.command("-c", "import lzma")

            # Ensure that pyexpat module works
            if "+pyexpat" in spec:
                self.command("-c", "import xml.parsers.expat")
                self.command("-c", "import xml.etree.ElementTree")

            # Ensure that ctypes module works
            if "+ctypes" in spec:
                self.command("-c", "import ctypes")

            # Ensure that tkinter module works
            # https://wiki.python.org/moin/TkInter
            if "+tkinter" in spec:
                # Only works if ForwardX11Trusted is enabled, i.e. `ssh -Y`
                if "DISPLAY" in env:
                    self.command("-c", "import tkinter; tkinter._test()")
                else:
                    self.command("-c", "import tkinter")

            # Ensure that uuid module works
            if "+uuid" in spec:
                self.command("-c", "import uuid")

            # Ensure that tix module works
            if "+tix" in spec:
                self.command("-c", "import tkinter.tix")

            # Ensure that crypt module works
            if "+crypt" in spec:
                self.command("-c", "import crypt")

    # ========================================================================
    # Set up environment to make install easy for python extensions.
    # ========================================================================

    @property
    def command(self):
        """Returns the Python command, which may vary depending
        on the version of Python and how it was installed.

        In general, Python 3 only comes with a ``python3`` command. However, some
        package managers will symlink ``python`` to ``python3``, while others
        may contain ``python3.11``, ``python3.10``, and ``python3.9`` in the
        same directory.

        Returns:
            Executable: the Python command
        """
        # We need to be careful here. If the user is using an externally
        # installed python, several different commands could be located
        # in the same directory. Be as specific as possible. Search for:
        #
        # * python3.11
        # * python3
        # * python
        #
        # in that order if using python@3.11.0, for example.
        suffixes = [self.spec.version.up_to(2), self.spec.version.up_to(1), ""]
        file_extension = "" if sys.platform != "win32" else ".exe"
        patterns = [f"python{ver}{file_extension}" for ver in suffixes]
        root = self.prefix.bin if sys.platform != "win32" else self.prefix
        path = find_first(root, files=patterns)

        if path is not None:
            return Executable(path)

        else:
            # Give a last try at rhel8 platform python
            if self.spec.external and self.prefix == "/usr" and self.spec.satisfies("os=rhel8"):
                path = os.path.join(self.prefix, "libexec", "platform-python")
                if os.path.exists(path):
                    return Executable(path)

        raise RuntimeError(
            f"cannot to locate the '{self.name}' command in {root} or its subdirectories"
        )

    @property
    def config_vars(self):
        """Return a set of variable definitions associated with a Python installation.

        Wrapper around various ``sysconfig`` functions. To see these variables on the
        command line, run:

        .. code-block:: console

           $ python -m sysconfig

        Returns:
            dict: variable definitions
        """
        cmd = """
import json
from sysconfig import (
    get_config_vars,
    get_config_h_filename,
    get_makefile_filename,
    get_paths,
)

config = get_config_vars()
config['config_h_filename'] = get_config_h_filename()
config['makefile_filename'] = get_makefile_filename()
config.update(get_paths())

print(json.dumps(config))
"""

        dag_hash = self.spec.dag_hash()
        lib_prefix = "lib" if sys.platform != "win32" else ""
        if dag_hash not in self._config_vars:
            # Default config vars
            version = self.version.up_to(2)
            if sys.platform == "win32":
                version = str(version).split(".")[0]
            config = {
                # get_config_vars
                "BINDIR": self.prefix.bin,
                "CC": "cc",
                "CONFINCLUDEPY": self.prefix.include.join("python{}").format(version),
                "CXX": "c++",
                "INCLUDEPY": self.prefix.include.join("python{}").format(version),
                "LIBDEST": self.prefix.lib.join("python{}").format(version),
                "LIBDIR": self.prefix.lib,
                "LIBPL": self.prefix.lib.join("python{0}")
                .join("config-{0}-{1}")
                .format(version, sys.platform),
                "LDLIBRARY": "{}python{}.{}".format(lib_prefix, version, dso_suffix),
                "LIBRARY": "{}python{}.{}".format(lib_prefix, version, stat_suffix),
                "LDSHARED": "cc",
                "LDCXXSHARED": "c++",
                "PYTHONFRAMEWORKPREFIX": "/System/Library/Frameworks",
                "base": self.prefix,
                "installed_base": self.prefix,
                "installed_platbase": self.prefix,
                "platbase": self.prefix,
                "prefix": self.prefix,
                # get_config_h_filename
                "config_h_filename": self.prefix.include.join("python{}")
                .join("pyconfig.h")
                .format(version),
                # get_makefile_filename
                "makefile_filename": self.prefix.lib.join("python{0}")
                .join("config-{0}-{1}")
                .Makefile.format(version, sys.platform),
                # get_paths
                "data": self.prefix,
                "include": self.prefix.include.join("python{}".format(version)),
                "platinclude": self.prefix.include64.join("python{}".format(version)),
                "platlib": self.prefix.lib64.join("python{}".format(version)).join(
                    "site-packages"
                ),
                "platstdlib": self.prefix.lib64.join("python{}".format(version)),
                "purelib": self.prefix.lib.join("python{}".format(version)).join("site-packages"),
                "scripts": self.prefix.bin,
                "stdlib": self.prefix.lib.join("python{}".format(version)),
            }

            try:
                config.update(json.loads(self.command("-c", cmd, output=str)))
            except (ProcessError, RuntimeError):
                pass
            self._config_vars[dag_hash] = config
        return self._config_vars[dag_hash]

    def get_sysconfigdata_name(self):
        """Return the full path name of the sysconfigdata file."""

        libdest = self.config_vars["LIBDEST"]

        cmd = "from sysconfig import _get_sysconfigdata_name; "
        cmd += "print(_get_sysconfigdata_name())"
        filename = self.command("-c", cmd, output=str).strip()
        filename += ".py"

        return join_path(libdest, filename)

    @property
    def home(self):
        """Most of the time, ``PYTHONHOME`` is simply
        ``spec['python'].prefix``. However, if the user is using an
        externally installed python, it may be symlinked. For example,
        Homebrew installs python in ``/usr/local/Cellar/python/2.7.12_2``
        and symlinks it to ``/usr/local``. Users may not know the actual
        installation directory and add ``/usr/local`` to their
        ``packages.yaml`` unknowingly. Query the python executable to
        determine exactly where it is installed.
        """
        return Prefix(self.config_vars["base"])

    def find_library(self, library):
        # Spack installs libraries into lib, except on openSUSE where it installs them
        # into lib64. If the user is using an externally installed package, it may be
        # in either lib or lib64, so we need to ask Python where its LIBDIR is.
        libdir = self.config_vars["LIBDIR"]

        # Debian and derivatives use a triplet subdir under /usr/lib, LIBPL can be used
        # to get the Python library directory
        libpldir = self.config_vars["LIBPL"]

        # The system Python installation on macOS and Homebrew installations
        # install libraries into a Frameworks directory
        frameworkprefix = self.config_vars["PYTHONFRAMEWORKPREFIX"]

        # Get the active Xcode environment's Framework location.
        macos_developerdir = os.environ.get("DEVELOPER_DIR")
        if macos_developerdir and os.path.exists(macos_developerdir):
            macos_developerdir = os.path.join(macos_developerdir, "Library", "Frameworks")
        else:
            macos_developerdir = ""

        # Windows libraries are installed directly to BINDIR
        win_bin_dir = self.config_vars["BINDIR"]
        win_root_dir = self.config_vars["prefix"]

        directories = [
            libdir,
            libpldir,
            frameworkprefix,
            macos_developerdir,
            win_bin_dir,
            win_root_dir,
        ]

        if self.spec.satisfies("platform=windows"):
            lib_dirs = ["libs"]
        else:
            # The Python shipped with Xcode command line tools isn't in any of these locations
            lib_dirs = ["lib", "lib64"]

        for subdir in lib_dirs:
            directories.append(os.path.join(self.config_vars["base"], subdir))

        directories = dedupe(directories)
        for directory in directories:
            path = os.path.join(directory, library)
            if os.path.exists(path):
                return LibraryList(path)

    @property
    def libs(self):
        py_version = self.version.up_to(2)
        if sys.platform == "win32":
            py_version = str(py_version).replace(".", "")
        lib_prefix = "lib" if sys.platform != "win32" else ""
        # The values of LDLIBRARY and LIBRARY aren't reliable. Intel Python uses a
        # static binary but installs shared libraries, so sysconfig reports
        # libpythonX.Y.a but only libpythonX.Y.so exists. So we add our own paths, too.

        # With framework python on macOS, self.config_vars["LDLIBRARY"] can point
        # to a library that is not linkable because it does not have the required
        # suffix of a shared library (it is called "Python" without extention).
        # The linker then falls back to libPython.tbd in the default macOS
        # software tree, which security settings prohibit to link against
        # (your binary is not an allowed client of /path/to/libPython.tbd).
        # To avoid this, we replace the entry in config_vars with a default value.
        file_extension_shared = os.path.splitext(self.config_vars["LDLIBRARY"])[-1]
        if file_extension_shared == "":
            shared_libs = []
        else:
            shared_libs = [self.config_vars["LDLIBRARY"]]
        shared_libs += ["{}python{}.{}".format(lib_prefix, py_version, dso_suffix)]
        # Like LDLIBRARY for Python on Mac OS, LIBRARY may refer to an un-linkable object
        file_extension_static = os.path.splitext(self.config_vars["LIBRARY"])[-1]
        if file_extension_static == "":
            static_libs = []
        else:
            static_libs = [self.config_vars["LIBRARY"]]
        static_libs += ["{}python{}.{}".format(lib_prefix, py_version, stat_suffix)]

        # The +shared variant isn't reliable, as `spack external find` currently can't
        # detect it. If +shared, prefer the shared libraries, but check for static if
        # those aren't found. Vice versa for ~shared.
        if self.spec.satisfies("platform=windows"):
            # Since we are searching for link libraries, on Windows search only for
            # ".Lib" extensions by default as those represent import libraries for implict links.
            candidates = static_libs
        elif self.spec.satisfies("+shared"):
            candidates = shared_libs + static_libs
        else:
            candidates = static_libs + shared_libs

        for candidate in dedupe(candidates):
            lib = self.find_library(candidate)
            if lib:
                return lib

        raise spack.error.NoLibrariesError(
            "Unable to find {} libraries with the following names:\n\n* ".format(self.name)
            + "\n* ".join(candidates)
        )

    @property
    def headers(self):
        # Locations where pyconfig.h could be
        # This varies by system, especially on macOS where the command line tools are
        # installed in a very different directory from the system python interpreter.
        py_version = str(self.version.up_to(2))
        candidates = [
            os.path.dirname(self.config_vars["config_h_filename"]),
            self.config_vars["INCLUDEPY"],
            self.config_vars["CONFINCLUDEPY"],
            os.path.join(self.config_vars["base"], "include", py_version),
            os.path.join(self.config_vars["base"], "Headers"),
        ]
        candidates = list(dedupe(candidates))

        for directory in candidates:
            headers = find_headers("pyconfig", directory)
            if headers:
                config_h = headers[0]
                break
        else:
            raise spack.error.NoHeadersError(
                "Unable to locate {} headers in any of these locations:\n\n* ".format(self.name)
                + "\n* ".join(candidates)
            )

        headers.directories = [os.path.dirname(config_h)]
        return headers

    # https://docs.python.org/3/library/sysconfig.html#installation-paths
    # https://discuss.python.org/t/understanding-site-packages-directories/12959
    # https://github.com/pypa/pip/blob/22.1/src/pip/_internal/locations/__init__.py
    # https://github.com/pypa/installer/pull/103

    # NOTE: XCode Python's sysconfing module was incorrectly patched, and hard-codes
    # everything to be installed in /Library/Python. Therefore, we need to use a
    # fallback in the following methods. For more information, see:
    # https://github.com/pypa/pip/blob/22.1/src/pip/_internal/locations/__init__.py#L486

    @property
    def platlib(self):
        """Directory for site-specific, platform-specific files.

        Exact directory depends on platform/OS/Python version. Examples include:

        * ``lib/pythonX.Y/site-packages`` on most POSIX systems
        * ``lib64/pythonX.Y/site-packages`` on RHEL/CentOS/Fedora with system Python
        * ``lib/pythonX/dist-packages`` on Debian/Ubuntu with system Python
        * ``lib/python/site-packages`` on macOS with framework Python
        * ``Lib/site-packages`` on Windows

        Returns:
            str: platform-specific site-packages directory
        """
        prefix = self.config_vars["platbase"] + os.sep
        path = self.config_vars["platlib"]
        if path.startswith(prefix):
            return path.replace(prefix, "")
        return os.path.join("lib64", f"python{self.version.up_to(2)}", "site-packages")

    @property
    def purelib(self):
        """Directory for site-specific, non-platform-specific files.

        Exact directory depends on platform/OS/Python version. Examples include:

        * ``lib/pythonX.Y/site-packages`` on most POSIX systems
        * ``lib/pythonX/dist-packages`` on Debian/Ubuntu with system Python
        * ``lib/python/site-packages`` on macOS with framework Python
        * ``Lib/site-packages`` on Windows

        Returns:
            str: platform-independent site-packages directory
        """
        prefix = self.config_vars["base"] + os.sep
        path = self.config_vars["purelib"]
        if path.startswith(prefix):
            return path.replace(prefix, "")
        return os.path.join("lib", f"python{self.version.up_to(2)}", "site-packages")

    @property
    def include(self):
        """Directory for non-platform-specific header files.

        Exact directory depends on platform/Python version/ABI flags. Examples include:

        * ``include/pythonX.Y`` on most POSIX systems
        * ``include/pythonX.Yd`` for debug builds
        * ``include/pythonX.Ym`` for malloc builds
        * ``include/pythonX.Yu`` for wide unicode builds
        * ``include`` on macOS with framework Python
        * ``Include`` on Windows

        Returns:
            str: platform-independent header file directory
        """
        prefix = self.config_vars["installed_base"] + os.sep
        path = self.config_vars["include"]
        if path.startswith(prefix):
            return path.replace(prefix, "")
        return os.path.join("include", "python{}".format(self.version.up_to(2)))

    def setup_dependent_build_environment(self, env, dependent_spec):
        """Set PYTHONPATH to include the site-packages directory for the
        extension and any other python extensions it depends on.
        """
        # We need to make sure that the extensions are compiled and linked with
        # the Spack wrapper. Paths to the executables that are used for these
        # operations are normally taken from the sysconfigdata file, which we
        # modify after the installation (see method filter compilers). The
        # modified file contains paths to the real compilers, not the wrappers.
        # The values in the file, however, can be overridden with environment
        # variables. The first variable, CC (CXX), which is used for
        # compilation, is set by Spack for the dependent package by default.
        # That is not 100% correct because the value for CC (CXX) in the
        # sysconfigdata file often contains additional compiler flags (e.g.
        # -pthread), which we lose by simply setting CC (CXX) to the path to the
        # Spack wrapper. Moreover, the user might try to build an extension with
        # a compiler that is different from the one that was used to build
        # Python itself, which might have unexpected side effects. However, the
        # experience shows that none of the above is a real issue and we will
        # not try to change the default behaviour. Given that, we will simply
        # try to modify LDSHARED (LDCXXSHARED), the second variable, which is
        # used for linking, in a consistent manner.

        for compile_var, link_var in [("CC", "LDSHARED"), ("CXX", "LDCXXSHARED")]:
            # First, we get the values from the sysconfigdata:
            config_compile = self.config_vars[compile_var]
            config_link = self.config_vars[link_var]

            # The dependent environment will have the compilation command set to
            # the following:
            new_compile = join_path(
                spack.paths.build_env_path,
                dependent_spec.package.compiler.link_paths[compile_var.lower()],
            )

            # Normally, the link command starts with the compilation command:
            if config_link.startswith(config_compile):
                new_link = new_compile + config_link[len(config_compile) :]
            else:
                # Otherwise, we try to replace the compiler command if it
                # appears "in the middle" of the link command; to avoid
                # mistaking some substring of a path for the compiler (e.g. to
                # avoid replacing "gcc" in "-L/path/to/gcc/"), we require that
                # the compiler command be surrounded by spaces. Note this may
                # leave "config_link" unchanged if the compilation command does
                # not appear in the link command at all, for example if "ld" is
                # invoked directly (no change would be required in that case
                # because Spack arranges for the Spack ld wrapper to be the
                # first instance of "ld" in PATH).
                new_link = config_link.replace(f" {config_compile} ", f" {new_compile} ")

            # There is logic in the sysconfig module that is sensitive to the
            # fact that LDSHARED is set in the environment, therefore we export
            # the variable only if the new value is different from what we got
            # from the sysconfigdata file:
            if config_link != new_link and sys.platform != "win32":
                env.set(link_var, new_link)

    def setup_dependent_run_environment(self, env, dependent_spec):
        """Set PYTHONPATH to include the site-packages directory for the
        extension and any other python extensions it depends on.
        """
        if not dependent_spec.package.extends(self.spec) or dependent_spec.dependencies(
            "python-venv"
        ):
            return

        # Packages may be installed in platform-specific or platform-independent site-packages
        # directories
        for directory in {self.platlib, self.purelib}:
            env.prepend_path("PYTHONPATH", os.path.join(dependent_spec.prefix, directory))

    def setup_dependent_package(self, module, dependent_spec):
        """Called before python modules' install() methods."""
        module.python = self.command
        module.python_include = join_path(dependent_spec.prefix, self.include)
        module.python_platlib = join_path(dependent_spec.prefix, self.platlib)
        module.python_purelib = join_path(dependent_spec.prefix, self.purelib)

    def add_files_to_view(self, view, merge_map, skip_if_exists=True):
        """Make the view a virtual environment if it isn't one already.

        If `python-venv` is linked into the view, it will already be a virtual
        environment. If not, then this is an older python that doesn't use the
        python-venv support, or we may be using python packages that
        use ``depends_on("python")`` but not ``extends("python")``.

        We used to copy the python interpreter in, but we can get the same effect in a
        simpler way by adding a ``pyvenv.cfg`` to the environment.

        """
        super().add_files_to_view(view, merge_map, skip_if_exists=skip_if_exists)

        # location of python inside the view, where we will put the venv config
        projection = view.get_projection_for_spec(self.spec)
        pyvenv_cfg = os.path.join(projection, "pyvenv.cfg")
        if os.path.lexists(pyvenv_cfg):
            return

        # don't put a pyvenv.cfg in a copy view
        if view.link_type == "copy":
            return

        with open(pyvenv_cfg, "w") as cfg_file:
            cfg_file.write(make_pyvenv_cfg(self.spec["python"], projection))

    def test_hello_world(self):
        """run simple hello world program"""
        # do not use self.command because we are also testing the run env
        python = self.spec["python"].command

        msg = "hello world!"
        out = python("-c", f'print("{msg}")', output=str.split, error=str.split)
        assert msg in out

    def test_import_executable(self):
        """ensure import of installed executable works"""
        python = self.spec["python"].command

        out = python("-c", "import sys; print(sys.executable)", output=str.split, error=str.split)
        assert self.spec.prefix in out
