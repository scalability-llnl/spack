from spack import *
import shutil

class Cereal(Package):
    """cereal is a header-only C++11 serialization library. cereal takes arbitrary data types and reversibly turns them into different representations, such as compact binary encodings, XML, or JSON. cereal was designed to be fast, light-weight, and easy to extend - it has no external dependencies and can be easily bundled with other code or used standalone."""
    homepage = "http://uscilab.github.io/cereal/"
    url      = "https://github.com/USCiLab/cereal/archive/v1.1.2.tar.gz"

    version('1.1.2', '34d4ad174acbff005c36d4d10e48cbb9')
    version('1.1.1', '0ceff308c38f37d5b5f6df3927451c27')
    version('1.1.0', '9f2d5f72e935c54f4c6d23e954ce699f')
    version('1.0.0', 'd1bacca70a95cec0ddbff68b0871296b')
    version('0.9.1', '8872d4444ff274ce6cd1ed364d0fc0ad')

    patch("Werror.patch")

    depends_on("cmake @2.6.2:")

    def install(self, spec, prefix):
        # Don't use -Werror
        filter_file(r'-Werror', '', 'CMakeLists.txt')

        # configure
        # Boost is only used for self-tests, which we are not running (yet?)
        cmake('.', '-DCMAKE_DISABLE_FIND_PACKAGE_Boost=TRUE', *std_cmake_args)

        # Build
        make()

        # Install
        shutil.rmtree(join_path(prefix, 'doc'), ignore_errors=True)
        shutil.rmtree(join_path(prefix, 'include'), ignore_errors=True)
        shutil.copytree('doc', join_path(prefix, 'doc'), symlinks=True)
        shutil.copytree('include', join_path(prefix, 'include'), symlinks=True)
