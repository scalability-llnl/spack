# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyNbconvert(PythonPackage):
    """Jupyter Notebook Conversion"""

    homepage = "https://github.com/jupyter/nbconvert"
    pypi = "nbconvert/nbconvert-6.0.1.tar.gz"

    version('6.0.1', sha256='db94117fbac29153834447e31b30cda337d4450e46e0bdb1a36eafbbf4435156')
    version('5.6.0', sha256='427a468ec26e7d68a529b95f578d5cbf018cb4c1f889e897681c2b6d11897695')
    version('5.5.0', sha256='138381baa41d83584459b5cfecfc38c800ccf1f37d9ddd0bd440783346a4c39c')
    version('4.2.0', sha256='55946d7522741294fcdd50799bd1777d16673ce721fecca0610cdb86749863c6')
    version('4.1.0', sha256='e0296e45293dd127d028f678e3b6aba3f1db3283a134178bdb49eea402d4cf1c')
    version('4.0.0', sha256='472ad15d1a71f1ef00c4094c11bb93638858fc89fb2c5838b3aa6b67d981b437')

    variant('serve', default=True, description='Include a webserver')

    depends_on('python@2.7:2.8,3.3:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'), when='@5:')
    depends_on('python@3.6:', type=('build', 'run'), when='@6:')
    depends_on('py-setuptools', type=('build', 'run'), when='@5:')
    depends_on('py-pycurl', type='build', when='^python@:2.7.8')
    depends_on('py-mistune@0.8.1:1.999', type=('build', 'run'))
    depends_on('py-jinja2', type=('build', 'run'))
    depends_on('py-jinja2@2.4:', type=('build', 'run'), when='@5:')
    depends_on('py-pygments', type=('build', 'run'))
    depends_on('py-pygments@2.4.1:', type=('build', 'run'), when='@6:')
    depends_on('py-jupyterlab-pygments', type=('build', 'run'), when='@6:')
    depends_on('py-traitlets', type=('build', 'run'))
    depends_on('py-traitlets@4.2:', type=('build', 'run'), when='@5:')
    depends_on('py-jupyter-core', type=('build', 'run'))
    depends_on('py-nbformat', type=('build', 'run'))
    depends_on('py-nbformat@4.4.0:', type=('build', 'run'), when='@5:')
    depends_on('py-entrypoints', type=('build', 'run'))
    depends_on('py-entrypoints@0.2.2:', type=('build', 'run'), when='@5:')
    depends_on('py-bleach', type=('build', 'run'), when='@5:')
    depends_on('py-pandocfilters@1.4.1:', type=('build', 'run'), when='@5:')
    depends_on('py-testpath', type=('build', 'run'), when='@5:')
    depends_on('py-defusedxml', type=('build', 'run'), when='@5:')
    depends_on('py-nbclient@0.5.0:0.5.999', type=('build', 'run'), when='@6:')
    depends_on('py-tornado@4.0:', type=('build', 'run'), when='+serve')

    def patch(self):
        # We bundle this with the spack package so that the installer
        # doesn't try to download it.
        install(join_path(self.package_dir, 'style.min.css'),
                join_path('nbconvert', 'resources', 'style.min.css'))

    def setup_run_environment(self, env):
        env.prepend_path("JUPYTER_PATH", self.prefix.share.jupyter)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path("JUPYTER_PATH", self.prefix.share.jupyter)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path("JUPYTER_PATH", self.prefix.share.jupyter)
