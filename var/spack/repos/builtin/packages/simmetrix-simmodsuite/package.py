# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


def simmodsuite_releases():
    releases = [
        {
            'version': '14.0-191122',
            'components': {
                'gmadv': ['01cea5f7aff5e442ea544df054969740ad33e2ff4097cf02de31874d16a0c7c2', 'advmodel'],
                'msadapt': ['69839698f24969f97963869fd212bdcff0b5d52dd40ec3fdc710d878e43b527a', 'base'],
                'gmvoxel': ['bfea15e1fc5d258ed9db69132042a848ca81995e92bf265215e4b88d08a308a8', 'voxel'],
                'gmabstract': ['dccdcd4b71758e4110cd69b0befa7875e5c1f3871f87478410c6676da3f39092', 'abstract'],
                'fdcore': ['6981b2eb0c0143e6abc3ec29918fc3552f81018755770bf922d2491275984e1a', 'base'],
                'msparallelmesh': ['1e1a431ec9dd85354ff42c6a2a41df7fbe3dfe5d296f40105c4d3aa372639dc3', 'parallelmesh'],
                'mscore': ['bca80fcb2c86e7b6dc0259681ccd73197ce85c47f00f1910bd6b518fa0b3a092', 'base'],
                'discrete': ['430e5f2270864b1ab9c8dff75d2510147a0c5cde8af0828975d9e38661be3a35', 'discrete'],
                'gmimport': ['e83b3c43b7c695fa96ed42253a4b317a2882bcb8987fd3225c09492e353e49aa', 'import'],
                'pskrnl': ['31455cfce746b2339b3644f3890d4444014fb839654a9f576ec747d28ff6c1c4', 'parasolid'],
                'gmcore': ['af5d89b9ce266cac5b45f2bf96e1324e87e54c6e2f568bd5b6a85c41122d39e4', 'base'],
                'aciskrnl': ['764e5633e6d502951788accfb8c34ed59430a4779a44d1775fd67f9aab8a654a', 'acis'],
                'msparalleladapt': ['8ae607112958f6b9d319736c71a6597cf99a8a59ceed733f2a939cb9cfa6dd67', 'paralleladapt'],
                'psint': ['f6c90b2fe87e690b2cba20f357d03c5962fed91541d6b79e01dc25cb8f01d1e0', 'parasolid'],
                'msadv': ['f18a8285d539cb07b00fde06fe970d958eceabf2a10182bcca6c8ad1c074c395', 'adv'],
            },
            'docs': {
                'MeshSim': ['f3c475072f270ff49ac2f6639ca1cddb0642889648cbea7df1a3f1b85f7cac36', 'base'],
                'GeomSimVoxel': ['9f4ee5a8204fee1d899cb912e0379f8be7a826e81ca0a0d8a670a4b804ca1276', 'voxel'],
                'MeshSimAdvanced': ['8c8bc3709238e600e8938c7c345588f8947d89eae98a228b0d0e3d46f5f4c0d9', 'adv'],
                'GeomSimDiscreteModeling': ['4e8e26a88e8a5ad396a637597a52f5973d8f77abc0a5b99fa737caf37226d6cc', 'discrete'],
                'GeomSimAdvanced': ['5efb38317d6be7862ce34024922ca372b30691a30af820474e2e26e4c3055278', 'advmodel'],
                'GeomSimParasolid': ['6851bdaf6d96e7b2335fce3394825e9876800f0aba0a42644758dc1bd06f60fe', 'parasolid'],
                'GeomSimImport': ['d931ecfc332460c825b473c0950c7ae8ff9f845e0d1565f85bfd7698da5e6d26', 'import'],
                'ParallelMeshSim': ['0f0d235b25a660271e401488e412220f574b341dadb827f7b82f0e93172b5cdb', 'parallelmesh'],
                'ParallelMeshSimAdapt': ['7964ebbd7e8d971ea85fc5260e44f7e876da5ad474dc67d8d6fc939bfa5ba454', 'paralleladapt'],
                'GeomSimAcis': ['dea82efbc4e3043ecda163be792ef295057e08be17654a7783ce7ca5e786f950', 'acis'],
                'MeshSimAdapt': ['ee4d5595572c1fe1a0d78bd9b85c774a55e994c48170450d6c5f34b05fcf2411', 'base'],
                'FieldSim': ['6b09b4ab278911d3e9229fd4cd8dc92ba188f151d42d9d7b96d542aad2af1fac', 'base'],
                'GeomSim': ['0673823d649998367c0e427055911eae971bb6e8c76625882e7a7901f4d18c44', 'base'],
                'GeomSimDiscrete': ['58dfd33fc5cdd2ab24e9084377943f28d5ba68b8c017b11b71cde64c5e4f2113', 'discrete'],
                'GeomSimAbstract': ['16248cd2a0d133029eb4b79d61397da008e4d5b5c3eaf0161a0a44148b0bc519', 'abstract'],
            }
        },
        {
            'version': '12.0-191027',
            'components': {
                'gmadv': ['1a133523062974c4d9acb1d52baa3893dc891482aebaaeb79a7dc907461d5dbc', 'advmodel'],
                'fdcore': ['c3a89093f811cb489698d203dbe68ca910e6c67ea75c0a7aba73dd369508b9ec', 'base'],
                'mscore': ['a2f043278d45d8729020b663c66c57960fcec33dafd3d90db55f0a9e32723bce', 'base'],
                'msparallelmesh': ['2f6fd47d3c5c2f1ece4634985a522ac599d3cee20ad8a4623f252cc75aa32c4c', 'parallelmesh'],
                'msparalleladapt': ['8d288730b1300215a32f3b21624bd2e0e2d8a684fe928459757fcec7e0aeb7d3', 'paralleladapt'],
                'gmabstract': ['3b608f21e6c11db5bb48e49f9cd7e9d88aeec4feadebd778529a5c9d506d08c6', 'abstract'],
                'gmimport': ['fc1626c7b1522b90eaa3926e1253b84d28440c7df8634decdedb79b5229be800', 'import'],
                'discrete': ['a15ead08138f0c59c7ee46cd0d348d4f26e1b021d2580a134cf2b84a7337bcf9', 'discrete'],
                'aciskrnl': ['8773f00e08d237052c877e79d1a869214f59891e812d70df938b2a5e5423a96f', 'acis'],
                'msadv': ['41bdb9555ab9feb0891f0832a49fc29777d40957473f315e1c33e1c0077cba7d', 'adv'],
                'psint': ['b040ab48833eb2a748f757e2de6929f3002aa98db459ba92bd9a88e443e5cb07', 'parasolid'],
                'gmvoxel': ['19fba83c9c7eac20d9613236530fbae652dc8edef35233214f0f92b81c91a877', 'voxel'],
                'msadapt': ['1a752adb6724c3328fffb26f1aebed007d3c2a5df725cd29aa0cf0fdfda1f39a', 'base'],
                'gmcore': ['ec95bae84b36644e6e04cf0a6b4e813a51990d0a30519176ebb8a05f681af7f2', 'base'],
                'pskrnl': ['7b7b4952513e06c8c23aa8f7c1748f5c199d9af70ea06c4a359412237ed8ac1d', 'parasolid'],
            },
            'docs': {
                'FieldSim': ['5109d91fe61ccdaf0af5aa869aea9c38ec98760746ec3983d100f870cbb1cb63', 'base'],
                'ParallelMeshSim': ['a1e6618a77022a9580beac4c698dd4b9aa70f617a27db9ce13ab1f2388475290', 'parallelmesh'],
                'GeomSimAcis': ['f0319b32eb417fa9b237575d9b2dc1c061848888c36fd4da97d97cdbb3cf19c3', 'acis'],
                'GeomSimAbstract': ['c44023e6944522057c47925db49089031c7de9b67938ca6a987e04fadfeda9b7', 'abstract'],
                'GeomSimDiscrete': ['ad648752fa7d2dc1ce234a612e28ce84eb1f064a1decadf17b42e9fe56967350', 'discrete'],
                'MeshSimAdapt': ['dcb7d6ec74c910b41b5ae707d9fd4664fcb3a0fdb2c876caaa28a6f1cf701024', 'base'],
                'MeshSim': ['e5a8cb300b1e13b9f2733bf8b738872ffb37d9df15836a6ab264483c10000696', 'base'],
                'GeomSimParasolid': ['2bf33cc5b3879716437d45fde0a02caaa165e37d248d05b4b00708e76573a15e', 'parasolid'],
                'GeomSimImport': ['5309433dcdce660e062412f070719eefcc6299764e9b0169533ff343c9c9c406', 'import'],
                'ParallelMeshSimAdapt': ['2e8e0ceede3107b85dba9536f3bbf5e6959793073a5147548cfb01ca568c8da2', 'paralleladapt'],
                'GeomSimDiscreteModeling': ['ff88ec234b890315cc36539e3f73f4f977dab94160860950e7b7ee0303c9b55e', 'discrete'],
                'GeomSim': ['62ae33372f999d5e62a1b7b161ddd7de04c055adc85cfd258e088c95b76d5fef', 'base'],
                'GeomSimVoxel': ['7a624ddaebd833077511acac3efd4b4c1dab09bd9feff40aba0813182eeb262f', 'voxel'],
                'GeomSimAdvanced': ['f0ab801ddf3d701a4ac3f8c47900cc858a4488eb0fe2f663504ba260cd270d20', 'advmodel'],
                'MeshSimAdvanced': ['bb532027e4fcc311a7c376383da010aed5ee133a9122b186a4e5c7d0cf1d976b', 'adv'],
            }
        }
    ]
    return releases


def simmetrix_makecomponenturl(name):
    """only supporting the linux libraries"""
    prefix = "file://{0}/".format(os.getcwd())
    suffix = "-" + "linux64.tgz"
    return prefix + name + suffix


def simmetrix_makedocurl(name):
    """doc zip files are not os/arch specific"""
    prefix = "file://{0}/".format(os.getcwd())
    suffix = '.zip'
    return prefix + name + suffix


def simmetrix_setkernelcmakeprefixpath(spec, path, env):
    if '+acis' in spec:
        env.append_path('CMAKE_PREFIX_PATH', join_path(path, 'acisKrnl'))
        env.append_path('LD_LIBRARY_PATH', join_path(path, 'acisKrnl'))
    if '+parasolid' in spec:
        env.append_path('CMAKE_PREFIX_PATH', join_path(path, 'psKrnl'))
        env.append_path('LD_LIBRARY_PATH', join_path(path, 'psKrnl'))


def simmetrix_resource(name, url, sha256, condition):
    # The tarballs/zips each have the same directory structure.  Because of
    # this, and the bug in spack described here:
    # https://github.com/spack/spack/pull/3553#issuecomment-391424244
    # , they cannot be expanded into the source root directory.
    # Once this is fixed the 'destination=name' argument can be removed.
    resource(
        name=name,
        url=url,
        sha256=sha256,
        destination=name,
        when=condition
    )


class SimmetrixSimmodsuite(Package):
    """Simmetrix' Simulation Modeling Suite is a set of component software
    toolkits that allow developers to easily implement geometry-based
    simulation applications.
    Each component of the Simulation Modeling Suite is designed to address
    specific capabilities:
    | MeshSim - automatic mesh generation
    | FieldSim - simulation data management
    | GeomSim - direct, untranslated access to geometry from a wide variety
    of sources
    """

    homepage = "http://www.simmetrix.com/products/SimulationModelingSuite/main.html"
    manual_download = True

    license_required = True
    license_vars     = ['SIM_LICENSE_FILE']

    variant('base', default=True, description='enable the base components')
    variant('advmodel', default=False, description='enable advaced modeling')
    variant('abstract', default=False, description='enable abstract modeling')
    variant('voxel', default=False, description='enable voxel modeling')
    variant('discrete', default=False, description='enable discrete modeling')
    variant('acis', default=False, description='enable acis modeling')
    variant('parasolid', default=False, description='enable parasolid modeling')
    variant('granite', default=False, description='enable granite modeling')
    variant('import', default=False, description='enable import modeling')
    variant('adv', default=False, description='enable advanced meshing')
    variant('parallelmesh', default=False, description='enable parallel meshing')
    variant('paralleladapt', default=False, description='enable parallel adaptation')

    depends_on('mpi')

    oslib = 'x64_rhel7_gcc48'

    releases = simmodsuite_releases()
    for release in releases:
        # define the version using the mscore tarball
        sim_version = release['version']
        main_pkg_name = 'mscore'
        url = simmetrix_makecomponenturl(main_pkg_name)
        sha256 = release['components'][main_pkg_name][0]
        version(sim_version, sha256=sha256, url=url)
        # define resources for the other tarballs
        for name, atts in release['components'].items():
            # skip the tarball used for the version(...) call
            if name == 'mscore':
                continue
            sha256 = atts[0]
            feature = atts[1]
            url = simmetrix_makecomponenturl(name)
            condition = "@{0}+{1}".format(sim_version, feature)
            simmetrix_resource(name, url, sha256, condition)
        # define resources for the document zip files
        for name, atts in release['docs'].items():
            sha256 = atts[0]
            feature = atts[1]
            url = simmetrix_makedocurl(name)
            condition = "@{0}+{1}".format(sim_version, feature)
            simmetrix_resource(name, url, sha256, condition)

    def setup_dependent_build_environment(self, env, dependent_spec):
        archlib = join_path(prefix.lib, self.oslib)
        env.append_path('CMAKE_PREFIX_PATH', archlib)
        simmetrix_setkernelcmakeprefixpath(self.spec, archlib, env)

    def setup_run_environment(self, env):
        archlib = join_path(prefix.lib, self.oslib)
        env.append_path('CMAKE_PREFIX_PATH', archlib)
        simmetrix_setkernelcmakeprefixpath(self.spec, archlib, env)

    def install(self, spec, prefix):
        if not spec.satisfies('platform=linux'):
            raise InstallError('Only the linux platform is supported')
        source_path = self.stage.source_path
        for release in simmodsuite_releases():
            simversion = release['version']
            if simversion != spec.version.string:
                continue
            for name, atts in release['components'].items():
                feature = atts[1]
                if '+' + feature in spec:
                    if name == 'mscore':
                        install_tree(join_path(source_path, 'lib'), prefix.lib)
                        install_tree(
                            join_path(source_path, 'include'),
                            prefix.include)
                    else:
                        path = join_path(
                            source_path,
                            name,
                            self.version.string)
                        install_tree(path, prefix)
            for name, atts in release['docs'].items():
                feature = atts[1]
                if '+' + feature in spec:
                    path = join_path(
                        source_path,
                        name,
                        self.version.string)
                    install_tree(path, prefix)

        workdir = prefix.code.PartitionWrapper
        if '+parallelmesh' in spec:
            with working_dir(workdir):
                mpi_id = spec['mpi'].name + spec['mpi'].version.string
                # build the wrapper lib
                make("-f", "Makefile.custom",
                     "CC=%s" % spec['mpi'].mpicc,
                     "CXX=%s" % spec['mpi'].mpicxx,
                     "PARALLEL=%s" % mpi_id,
                     "PQUAL=-%s" % mpi_id,
                     "OPTFLAGS=-O2 -DNDEBUG " + self.compiler.cc_pic_flag)
                libname = 'libSimPartitionWrapper-' + mpi_id + '.a'
                wrapperlibpath = join_path(workdir, 'lib', libname)
                install(wrapperlibpath, join_path(prefix.lib, self.oslib))
