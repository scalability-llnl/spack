# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *


class HdfEos2(AutotoolsPackage):
    """HDF-EOS (Hierarchical Data Format - Earth Observing System) is a
    self-describing file format based upon HDF for standard data products
    that are derived from EOS missions.  HDF-EOS2 is based upon HDF4.
    """

    homepage = "https://hdfeos.org"
    # Starting with @3, download requires authentication.  So reverting
    # to a manual download
    url = "file://{0}/hdf-eos2-3.0-src.tar.gz".format(os.getcwd())
    manual_download = True

    # The download URLs for @2 versions are messing, and include sha256 checksum.
    # Templates for url_for_version. 0 is sha256 checksum, 1 is filename
    # This is just a template.  See version_list and url_for_version below
    v2url = "https://git.earthdata.nasa.gov/rest/git-lfs/storage/DAS/hdfeos/{0}?response-content-disposition=attachment%3B%20filename%3D%22{1}%22%3B%20filename*%3Dutf-8%27%27{1}"

    maintainers("climbfuji")

    # Crazy URL scheme, differing with each version, and including the
    # sha256 checksum in the URL.  Yuck
    # The data in version_list is used to generate versions and urls
    # In basename expansions, 0 is raw version,
    # 1 is for version with dots => underscores
    version_list = [
        {
            "version": "3.0",
            "basename": "hdf-eos2-{0}-src.tar.gz",
            "sha256": "3a5564b4d69b541139ff7dfdad948696cf31d9d1a6ea8af290c91a4c0ee37188",
            "can_auto_download": False,
        },
        {
            "version": "2.20v1.00",
            "sha256": "cb0f900d2732ab01e51284d6c9e90d0e852d61bba9bce3b43af0430ab5414903",
            "basename": "HDF-EOS{0}.tar.Z",
            "can_auto_download": True,
        },
        {
            "version": "2.19b",
            "sha256": "a69993508dbf5fa6120bac3c906ab26f1ad277348dfc2c891305023cfdf5dc9d",
            "basename": "hdfeos{1}.zip",
            "can_auto_download": True,
        },
    ]

    for vrec in version_list:
        ver = vrec["version"]
        sha256 = vrec["sha256"]
        version(ver, sha256=sha256)

    variant(
        "shared", default=True, description="Build shared libraries (can be used with +static)"
    )
    variant(
        "static", default=True, description="Build static libraries (can be used with +shared)"
    )

    conflicts("~static", when="~shared", msg="At least one of +static or +shared must be set")

    # Build dependencies
    depends_on("hdf")
    # Because hdf always depends on zlib and jpeg in spack, the tests below in configure_args
    # (if self.spec.satisfies("^jpeg"):) always returns true and hdf-eos2 wants zlib and jpeg, too.
    depends_on("zlib-api")
    depends_on("jpeg")
    depends_on("szip", when="^hdf +szip")

    # Fix some problematic logic in stock configure script
    # test succeeds, but then script aborts due to env variable not being set
    patch("hdf-eos2.configure.patch", when="@2:3.0")

    # The standard Makefile.am, etc. add a --single_module flag to LDFLAGS
    # to pass to the linker.
    # That appears to be only recognized by the Darwin linker, remove it
    # if we are not running on darwin/
    if sys.platform != "darwin":
        patch("hdf-eos2.nondarwin-no-single_module.patch", when="@2")

    def url_for_version(self, version):
        vrec = [x for x in self.version_list if x["version"] == version.dotted.string]
        if vrec:
            fname = vrec[0]["basename"].format(version.dotted, version.underscored)
            sha256 = vrec[0]["sha256"]
            can_auto_download = vrec[0].get("can_auto_download", False)
            if can_auto_download:
                myurl = self.v2url.format(sha256, fname)
            else:
                myurl = self.url
            return myurl
        else:
            sys.exit(
                "ERROR: cannot generate URL for version {0};"
                "version/checksum not found in version_list".format(version)
            )

    @run_before("configure")
    def fix_configure(self):
        # spack patches the configure file unless autoconf is run,
        # and this fails because configure has the wrong permissions (644)
        if not self.force_autoreconf:
            os.chmod(join_path(self.stage.source_path, "configure"), 0o755)

        # The configure script as written really wants you to use h4cc.
        # This causes problems because h4cc differs when HDF is built with
        # autotools vs cmake, and we lose all the nice flags from the
        # Spack wrappers.  These filter operations allow us to use the
        # Spack wrappers again
        filter_file("\\$CC -show &> /dev/null", "true", "configure")
        filter_file("CC=./\\$SZIP_CC", "", "configure")

    def flag_handler(self, name, flags):
        if name == "cflags":
            flags.append(self.compiler.cc_pic_flag)
            if self.spec.compiler.name in ["apple-clang", "oneapi"]:
                flags.append("-Wno-error=implicit-function-declaration")
                flags.append("-Wno-error=implicit-int")

        return flags, None, None

    def setup_build_environment(self, env):
        # Add flags to LDFLAGS for any dependencies that need it
        extra_ldflags = []
        # hdf might have link dependency on rpc, if so need to add flags
        if self.spec.satisfies("^libtirpc"):
            tmp = self.spec["libtirpc"].libs.ld_flags
            extra_ldflags.append(tmp)
        # Set LDFLAGS
        env.set("LDFLAGS", " ".join(extra_ldflags))

    def configure_args(self):
        extra_args = []

        # We always build PIC code
        extra_args.append("--with-pic")
        extra_args.append("--enable-install_include")

        # Set shared/static appropriately
        extra_args.extend(self.enable_or_disable("shared"))
        extra_args.extend(self.enable_or_disable("static"))

        # Provide config args for dependencies
        extra_args.append("--with-hdf4={0}".format(self.spec["hdf"].prefix))
        if self.spec.satisfies("^jpeg"):
            # Allow handling whatever provider of jpeg are using
            tmp = self.spec["jpeg"].libs.directories
            if tmp:
                tmp = tmp[0]
                extra_args.append("--with-jpeg={0}".format(tmp))
        if self.spec.satisfies("^szip"):
            extra_args.append("--with-szlib={0}".format(self.spec["szip"].prefix))
        if self.spec.satisfies("^zlib"):
            extra_args.append("--with-zlib={0}".format(self.spec["zlib-api"].prefix))

        return extra_args
