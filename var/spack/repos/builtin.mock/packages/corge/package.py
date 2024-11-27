# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import sys

from spack.package import *


class Corge(Package):
    """A toy package to test dependencies"""

    homepage = "https://www.example.com"
    has_code = False
    version("3.0.0")

    depends_on("quux")

    def install(self, spec, prefix):
        corge_cc = """#include <iostream>
#include <stdexcept>
#include "corge.h"
#include "corge_version.h"
#include "quux/quux.h"

const int Corge::version_major = corge_version_major;
const int Corge::version_minor = corge_version_minor;

Corge::Corge()
{
}

int
Corge::get_version() const
{
    return 10 * version_major + version_minor;
}

int
Corge::corgegate() const
{
    int corge_version = get_version();
    std::cout << "Corge::corgegate version " << corge_version
              << " invoked" << std::endl;
    std::cout << "Corge config directory = %s" <<std::endl;
    Quux quux;
    int quux_version = quux.quuxify();

    if(quux_version != corge_version) {
        throw std::runtime_error(
              "Corge found an incompatible version of Garply.");
    }

    return corge_version;
}
"""
        corge_h = """#ifndef CORGE_H_

class Corge
{
private:
    static const int version_major;
    static const int version_minor;

public:
    Corge();
    int get_version() const;
    int corgegate() const;
};

#endif // CORGE_H_
"""
        corge_version_h = """
const int corge_version_major = %s;
const int corge_version_minor = %s;
"""
        corgegator_cc = """
#include <iostream>
#include "corge.h"

int
main(int argc, char* argv[])
{
    std::cout << "corgerator called with ";
    if (argc == 0) {
        std::cout << "no command-line arguments" << std::endl;
    } else {
        std::cout << "command-line arguments:";
        for (int i = 0; i < argc; ++i) {
            std::cout << " \"" << argv[i] << "\"";
        }
        std::cout << std::endl;
    }
    std::cout << "corgegating.."<<std::endl;
    Corge corge;
    corge.corgegate();
    std::cout << "done."<<std::endl;
    return 0;
}
"""
        mkdirp("%s/corge" % prefix.include)
        mkdirp("%s/corge" % self.stage.source_path)
        with open("%s/corge_version.h" % self.stage.source_path, "w") as f:
            f.write(corge_version_h % (self.version[0], self.version[1:]))
        with open("%s/corge/corge.cc" % self.stage.source_path, "w") as f:
            f.write(corge_cc % prefix.config)
        with open("%s/corge/corge.h" % self.stage.source_path, "w") as f:
            f.write(corge_h)
        with open("%s/corge/corgegator.cc" % self.stage.source_path, "w") as f:
            f.write(corgegator_cc)
        gpp = which("/usr/bin/g++")
        if sys.platform == "darwin":
            gpp = which("/usr/bin/clang++")
        gpp(
            "-Dcorge_EXPORTS",
            "-I%s" % self.stage.source_path,
            "-I%s" % spec["quux"].prefix.include,
            "-I%s" % spec["garply"].prefix.include,
            "-O2",
            "-g",
            "-DNDEBUG",
            "-fPIC",
            "-o",
            "corge.cc.o",
            "-c",
            "corge/corge.cc",
        )
        gpp(
            "-Dcorge_EXPORTS",
            "-I%s" % self.stage.source_path,
            "-I%s" % spec["quux"].prefix.include,
            "-I%s" % spec["garply"].prefix.include,
            "-O2",
            "-g",
            "-DNDEBUG",
            "-fPIC",
            "-o",
            "corgegator.cc.o",
            "-c",
            "corge/corgegator.cc",
        )
        if sys.platform == "darwin":
            gpp(
                "-fPIC",
                "-O2",
                "-g",
                "-DNDEBUG",
                "-dynamiclib",
                "-install_name",
                "@rpath/libcorge.dylib",
                "-o",
                "libcorge.dylib",
                "corge.cc.o",
                "-Wl,-rpath,%s" % spec["quux"].prefix.lib64,
                "-Wl,-rpath,%s" % spec["garply"].prefix.lib64,
                "%s/libquux.dylib" % spec["quux"].prefix.lib64,
                "%s/libgarply.dylib" % spec["garply"].prefix.lib64,
            )
            gpp(
                "-O2",
                "-g",
                "-DNDEBUG",
                "-rdynamic",
                "corgegator.cc.o",
                "-o",
                "corgegator",
                "-Wl,-rpath,%s" % prefix.lib64,
                "-Wl,-rpath,%s" % spec["quux"].prefix.lib64,
                "-Wl,-rpath,%s" % spec["garply"].prefix.lib64,
                "libcorge.dylib",
                "%s/libquux.dylib.3.0" % spec["quux"].prefix.lib64,
                "%s/libgarply.dylib.3.0" % spec["garply"].prefix.lib64,
            )
            mkdirp(prefix.lib64)
            copy("libcorge.dylib", "%s/libcorge.dylib" % prefix.lib64)
            os.link("%s/libcorge.dylib" % prefix.lib64, "%s/libcorge.dylib.3.0" % prefix.lib64)
        else:
            gpp(
                "-fPIC",
                "-O2",
                "-g",
                "-DNDEBUG",
                "-shared",
                "-Wl,-soname,libcorge.so",
                "-o",
                "libcorge.so",
                "corge.cc.o",
                "-Wl,-rpath,%s:%s::::" % (spec["quux"].prefix.lib64, spec["garply"].prefix.lib64),
                "%s/libquux.so" % spec["quux"].prefix.lib64,
                "%s/libgarply.so" % spec["garply"].prefix.lib64,
            )
            gpp(
                "-O2",
                "-g",
                "-DNDEBUG",
                "-rdynamic",
                "corgegator.cc.o",
                "-o",
                "corgegator",
                "-Wl,-rpath,%s" % prefix.lib64,
                "-Wl,-rpath,%s" % spec["quux"].prefix.lib64,
                "-Wl,-rpath,%s" % spec["garply"].prefix.lib64,
                "libcorge.so",
                "%s/libquux.so.3.0" % spec["quux"].prefix.lib64,
                "%s/libgarply.so.3.0" % spec["garply"].prefix.lib64,
            )
            mkdirp(prefix.lib64)
            copy("libcorge.so", "%s/libcorge.so" % prefix.lib64)
            os.link("%s/libcorge.so" % prefix.lib64, "%s/libcorge.so.3.0" % prefix.lib64)
        copy("corgegator", "%s/corgegator" % prefix.lib64)
        copy("%s/corge/corge.h" % self.stage.source_path, "%s/corge/corge.h" % prefix.include)
        mkdirp(prefix.bin)
        copy("corge_version.h", "%s/corge_version.h" % prefix.bin)
        os.symlink("%s/corgegator" % prefix.lib64, "%s/corgegator" % prefix.bin)
        os.symlink("%s/quuxifier" % spec["quux"].prefix.lib64, "%s/quuxifier" % prefix.bin)
        os.symlink("%s/garplinator" % spec["garply"].prefix.lib64, "%s/garplinator" % prefix.bin)
