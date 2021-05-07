This README will guide you through the steps needed to install Spack and 
start running it on a fresh Windows machine.

# Step 1: Install prerequisites

Before downloading and configuring Spack, we have to prepare our box for the 
installation. The following packages are required to successfully build and 
run the installer, in addition to running Spack in general:

* Visual Studio
* Python
* Git
* Wix

## Visual Studio

Microsoft Visual Studio provides the Windows C/C++ compiler that is currently supported by Spack.

We require several specific components to be included in the Visual Studio installation.  One is the C/C++ toolset, which can be selected as "Desktop development with C++" or "C++ build tools," depending on installation type (Professional, Build Tools, etc.)  The other required component is "C++ CMake tools for Windows," which can be selected from among the optional packages.  This provides CMake and Ninja for use during Spack configuration.

If you already have Visual Studio installed, you can make sure these components are installed by
rerunning the installer.  Next to your installation, select "Modify" and look at the "Installation details" pane on the right.

## Python

Python 3 can be downloaded from the Windows Store and will appear in your
path if installed from there.

## Git

Git is a version control system similar to Subversion and will be needed to
download Spack and the appropriate installation files. A bash console and GUI
can be downloaded from https://git-scm.com/downloads. If you are unfamiliar
with Git, there are a myriad of resources online to help guide you through
checking out repositories and switching development branches.

## Wix Toolset

Wix is a utility used for .msi creation and can be downloaded and
installed at https://wixtoolset.org/releases/. The Visual Studio
extensions are not necessary.

# Step 2: Get Spack

We are now ready to get the Spack environment set up on our machine. We
begin by creating a top-level directory to do our work in: we will call
it ``spack_install`` in this tutorial. Inside this directory, use Git to
clone the Spack repo, hosted at https://github.com/spack/spack.git.

The files and scripts used for Windows installation are on the
features/windows-support branch; ``cd`` into the repo and use 
``git checkout`` to switch to it. Then navigate to 
``lib\spack\spack\cmd\installer`` and copy the ``scripts`` directory and
``spack_cmd.bat`` up to the top-level ``spack_install`` directory.

Your file structure should look like this after following the above
steps:

```
spack_install
    |--------spack
    |--------scripts
    |--------spack_cmd.bat
```

# Step 3: Make the installer

To actually make the installer, start by running ``spack_cmd.bat`` from
Windows Explorer (this may require you to Run as Administrator). If a
warning appears that Python is not in your path, which can happen if you
installed Python from the website instead of Windows Store, add it in now.

``spack_cmd.bat`` will produce a DOS console window. Navigate to your
``spack_install`` directory (i.e. where you placed ``spack_cmd.bat``), and
create a new directory to store the installation (say, ``tmp``). This ``tmp``
directory must exist for the following commands to not fail.

There are two ways to create the installer. If you would like to create it
from a release version of Spack, say, 0.16.0, and store it in ``tmp``, you
can use the following command:

``spack make-installer -v 0.16.0 tmp``

The path to ``tmp`` can be either relative or absolute, but again, the
directory itself must already exist.

Alternatively, if you would like to build the installer using a local
checkout of Spack source (release or development), you can use the
-s flag to specify the directory where that checkout is. For example,
if you are doing development in a directory called ``spack-develop``
and want to generate an installer with the source there, you can use:

``spack make-installer -s spack-develop tmp``

# Step 4: Run the installer

Regardless of your method, a file called ``Spack.msi`` will be created
inside the ``tmp`` directory, which can then be run from Windows Explorer
like any other installer. After accepting the terms of service, select
where on your computer you would like Spack installed, and after a few minutes
Spack will be installed and ready for use.

If your Spack installation needs to be modified, repaired, or uninstalled, 
you can do any of these things by rerunning Spack.msi.

Running the installer also creates a shortcut on your desktop that, when launched,
will load a console identical to ``spack_cmd``, but with its initial directory
being wherever Spack was installed on your computer.

# Step 5: Configure Spack and test

The last thing to do after running the installer is to finish Spack configuration. This
is covered in the online documentation for Spack, but there are a few Windows-specific
steps that are necessary.

First, inside the Spack console, run the following command:

``spack compiler find``

This creates a .spack directory in our home directory, along with a windows subdirectory
containing a compilers.yaml file. On a fresh Windows install, the only compiler that
should be found is your installation of Microsoft Visual Studio.

We need to provide the config.yaml and packages.yaml configurations by ourselves. Open 
your text editor of choice and enter the following lines for config.yaml:

```
config:
  locks: false
  install_tree:
    root: $spack\opt\spack
    projections:
      all: '${ARCHITECTURE}\${COMPILERNAME}-${COMPILERVER}\${PACKAGE}-${VERSION}-${HASH}'
```

(These settings are identical to those in the default config.yaml
provided with your Spack checkout, except with forward slashes replaced by backslashes for
Windows compatibility.) It is important that all indentions in .yaml files are done with spaces
and not tabs, so take care when editing one by hand.

For the packages.yaml file, we need to direct spack towards the CMake and Ninja installations
we set up with Visual Studio. Therefore, your packages.yaml file will look something
like this, with possibly slight variants in the paths to CMake and Ninja:

```
packages:
  cmake:
    externals:
    - spec: cmake@3.19
      prefix: 'c:\Program Files (x86)\Microsoft Visual Studio
\2019\Professional\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake'
    buildable: False
  ninja:
    externals:
    - spec: ninja@1.8.2
      prefix: 'c:\Program Files (x86)\Microsoft Visual Studio
\2019\Professional\Common7\IDE\CommonExtensions\Microsoft\CMake\Ninja'
    buildable: False
```	

You can also use an external installation of CMake if you have one and prefer
to use it. If you don't have a path to Ninja analogous to the above, then you can
obtain it by running the Visual Studio Insaller and following the instructions
in Step 1 of this walkthrough.

Once all three of these files are present in your ``.spack/windows`` directory,
it is time to give the installation a test. Install a basic package though the
Spack console via:

``spack install cpuinfo``

If you are a developer and want to use your source version of Spack instead of
a release version, simply replace Spack in the above call with:

``python path\to\your\checkout\bin\spack``
