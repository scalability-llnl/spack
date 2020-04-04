# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class GitLfs(MakefilePackage):
    """Git LFS is a system for managing and versioning large files in
       association with a Git repository.  Instead of storing the large files
       within the Git repository as blobs, Git LFS stores special "pointer
       files" in the repository, while storing the actual file contents on a
       Git LFS server."""

    homepage = "https://git-lfs.github.com"
    url      = "https://github.com/git-lfs/git-lfs/archive/v2.6.1.tar.gz"

    version('2.9.0', sha256='f1963ad88747577ffeeb854649aeacaa741c59be74683da4d46b129a72d111b7')
    version('2.8.0', sha256='10b476bb8862ebceddc6f0a55f5fb63e2c1e5bed6554f6e3b207dd0155a196ad')
    version('2.7.2', sha256='e65659f12ec557ae8c778c01ca62d921413221864b68bd93cfa41399028ae67f')
    version('2.7.1', sha256='af60c2370d135ab13724d302a0b1c226ec9fb0ee6d29ecc335e9add4c86497b4')
    version('2.7.0', sha256='1c829ddd163be2206a44edb366bd7f6d84c5afae3496687405ca9d2a5f3af07b')
    version('2.6.1', sha256='e17cd9d4e66d1116be32f7ddc7e660c7f8fabbf510bc01b01ec15a22dd934ead')

    depends_on('go@1.11:', type='build')  # module/vendor support
    depends_on('git@1.8.2:', type='run')

    patch('patches/issue-10702.patch', when='@2.7.0:2.7.1')

    parallel = False

    # dependencies are vendored, ensure that they're used
    def setup_build_environment(self, env):
        # forcibly enable module mode
        env.set('GO111MODULE', 'on')
        # forcibly enable vendoring, prevent network access
        env.set('GOFLAGS', '-mod=vendor')

    # Git-lfs does not provide an 'install' target in the Makefile
    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install(join_path('bin', 'git-lfs'), prefix.bin)
