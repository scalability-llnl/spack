# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyGym(PythonPackage):
    """OpenAI Gym is a toolkit for developing and comparing
    reinforcement learning algorithms. This is the gym open-source
    library, which gives you access to a standardized set of
    environments."""

    homepage = "https://github.com/openai/gym"
    pypi     = "gym/0.18.0.tar.gz"

    version('0.18.0', sha256='a0dcd25c1373f3938f4cb4565f74f434fba6faefb73a42d09c9dddd0c08af53e')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-numpy@1.10.4:', type=('build', 'run'))
    depends_on('py-pyglet@1.4.0:1.5.0', type=('build', 'run'), when='@0.18.0')
    depends_on('py-pyglet@1.4.0:1.5.15', type=('build', 'run'), when='@0.18.1')
    depends_on('pil@:8.2.0', type=('build', 'run'), when='@0.18.1')
    depends_on('pil@:7.2.0', type=('build', 'run'), when='@0.18.0')
    depends_on('py-cloudpickle@1.2.0:1.6.999', type=('build', 'run'))
