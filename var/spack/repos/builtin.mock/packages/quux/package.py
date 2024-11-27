# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import sys

from spack.package import *


class Quux(Package):
    """Toy package for testing dependencies"""

    homepage = "https://www.example.com"
    has_code = False
    version("3.0.0")

    depends_on("garply")

    def install(self, spec, prefix):
        quux_cc = """#include "quux.h"
#include "garply/garply.h"
#include "quux_version.h"
#include <iostream>
#include <stdexcept>

const int Quux::version_major = quux_version_major;
const int Quux::version_minor = quux_version_minor;

Quux::Quux() {}

int
Quux::get_version() const
{
    return 10 * version_major + version_minor;
}

int
Quux::quuxify() const
{
    int quux_version = get_version();
    std::cout << "Quux::quuxify version " << quux_version
              << " invoked" <<std::endl;
    std::cout << "Quux config directory is %s" <<std::endl;
    Garply garply;
    int garply_version = garply.garplinate();

    if (garply_version != quux_version) {
        throw std::runtime_error(
            "Quux found an incompatible version of Garply.");
    }

    return quux_version;
}
"""
        quux_h = """#ifndef QUUX_H_

class Quux
{
private:
    static const int version_major;
    static const int version_minor;

public:
    Quux();
    int get_version() const;
    int quuxify() const;
};

#endif // QUUX_H_
"""
        quuxifier_cc = """
#include "quux.h"
#include <iostream>

int
main()
{
    Quux quux;
    quux.quuxify();

    return 0;
}
"""
        quux_version_h = """const int quux_version_major = %s;
const int quux_version_minor = %s;
"""
        mkdirp("%s/quux" % prefix.include)
        mkdirp("%s/quux" % self.stage.source_path)
        with open("%s/quux_version.h" % self.stage.source_path, "w") as f:
            f.write(quux_version_h % (self.version[0], self.version[1:]))
        with open("%s/quux/quux.cc" % self.stage.source_path, "w") as f:
            f.write(quux_cc % (prefix.config))
        with open("%s/quux/quux.h" % self.stage.source_path, "w") as f:
            f.write(quux_h)
        with open("%s/quux/quuxifier.cc" % self.stage.source_path, "w") as f:
            f.write(quuxifier_cc)
        gpp = which(
            "g++",
            path=":".join(
                [s for s in os.environ["PATH"].split(os.pathsep) if "lib/spack/env" not in s]
            ),
        )
        if sys.platform == "darwin":
            gpp = which("/usr/bin/clang++")
        gpp(
            "-Dquux_EXPORTS",
            "-I%s" % self.stage.source_path,
            "-I%s" % spec["garply"].prefix.include,
            "-O2",
            "-g",
            "-DNDEBUG",
            "-fPIC",
            "-o",
            "quux.cc.o",
            "-c",
            "quux/quux.cc",
        )
        gpp(
            "-Dquux_EXPORTS",
            "-I%s" % self.stage.source_path,
            "-I%s" % spec["garply"].prefix.include,
            "-O2",
            "-g",
            "-DNDEBUG",
            "-fPIC",
            "-o",
            "quuxifier.cc.o",
            "-c",
            "quux/quuxifier.cc",
        )
        if sys.platform == "darwin":
            gpp(
                "-fPIC",
                "-O2",
                "-g",
                "-DNDEBUG",
                "-dynamiclib",
                "-Wl,-headerpad_max_install_names",
                "-o",
                "libquux.dylib",
                "-install_name",
                "@rpath/libquux.dylib",
                "quux.cc.o",
                "-Wl,-rpath,%s" % prefix.lib64,
                "-Wl,-rpath,%s" % spec["garply"].prefix.lib64,
                "%s/libgarply.dylib" % spec["garply"].prefix.lib64,
            )
            gpp(
                "-O2",
                "-g",
                "-DNDEBUG",
                "quuxifier.cc.o",
                "-o",
                "quuxifier",
                "-Wl,-rpath,%s" % prefix.lib64,
                "-Wl,-rpath,%s" % spec["garply"].prefix.lib64,
                "libquux.dylib",
                "%s/libgarply.dylib" % spec["garply"].prefix.lib64,
            )
            mkdirp(prefix.lib64)
            copy("libquux.dylib", "%s/libquux.dylib" % prefix.lib64)
            os.link("%s/libquux.dylib" % prefix.lib64, "%s/libquux.dylib.3.0" % prefix.lib64)
        else:
            gpp(
                "-fPIC",
                "-O2",
                "-g",
                "-DNDEBUG",
                "-shared",
                "-Wl,-soname,libquux.so",
                "-o",
                "libquux.so",
                "quux.cc.o",
                "-Wl,-rpath,%s:%s::::" % (prefix.lib64, spec["garply"].prefix.lib64),
                "%s/libgarply.so" % spec["garply"].prefix.lib64,
            )
            gpp(
                "-O2",
                "-g",
                "-DNDEBUG",
                "-rdynamic",
                "quuxifier.cc.o",
                "-o",
                "quuxifier",
                "-Wl,-rpath,%s:%s::::" % (prefix.lib64, spec["garply"].prefix.lib64),
                "libquux.so",
                "%s/libgarply.so" % spec["garply"].prefix.lib64,
            )
            mkdirp(prefix.lib64)
            copy("libquux.so", "%s/libquux.so" % prefix.lib64)
            os.link("%s/libquux.so" % prefix.lib64, "%s/libquux.so.3.0" % prefix.lib64)
        copy("quuxifier", "%s/quuxifier" % prefix.lib64)
        copy("%s/quux/quux.h" % self.stage.source_path, "%s/quux/quux.h" % prefix.include)
        mkdirp(prefix.bin)
        copy("quux_version.h", "%s/quux_version.h" % prefix.bin)
        os.symlink("%s/quuxifier" % prefix.lib64, "%s/quuxifier" % prefix.bin)
        os.symlink("%s/garplinator" % spec["garply"].prefix.lib64, "%s/garplinator" % prefix.bin)
