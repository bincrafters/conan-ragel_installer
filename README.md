[ ![Download](https://api.bintray.com/packages/sigmoidal/public-conan/ragel_installer%3Asigmoidal/images/download.svg?version=6.10%3Astable) ](https://bintray.com/sigmoidal/public-conan/ragel_installer%3Asigmoidal/6.10%3Astable/link)
[![Build status](https://ci.appveyor.com/api/projects/status/se14gom9yvuq9ps4?svg=true)](https://ci.appveyor.com/project/sigmoidal/conan-ragel_installer)

Ragel compiles executable finite state machines from regular languages. Ragel targets C, C++ and ASM. 

[Conan.io](https://conan.io) package for the [ragel](http://www.colm.net/open-source/ragel/) project.

The packages generated with this **conanfile** can be found in [Bintray](https://bintray.com/sigmoidal/public-conan/ragel_installer%3Asigmoidal).

## For Users: Use this package

### Basic setup

    $ conan install ragel_installer/6.10@sigmoidal/stable

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    ragel_installer/6.10@sigmoidal/stable

    [generators]
    txt

Complete the installation of requirements for your project running:

    $ mkdir build && cd build && conan install ..

Note: It is recommended that you run conan install from a build directory and not the root of the project directory.  This is because conan generates *conanbuildinfo* files specific to a single build configuration which by default comes from an autodetected default profile located in ~/.conan/profiles/default .  If you pass different build configuration options to conan install, it will generate different *conanbuildinfo* files.  Thus, they should not be added to the root of the project, nor committed to git.

## For Packagers: Publish this Package

The example below shows the commands used to publish to sigmoidal conan repository. To publish to your own conan respository (for example, after forking this git repository), you will need to change the commands below accordingly.

## Build and package

The following command both runs all the steps of the conan file, and publishes the package to the local system cache.  This includes downloading dependencies from "build_requires" and "requires" , and then running the build() method.

    $ conan create sigmoidal/stable

## Add Remote

	$ conan remote add sigmoidal "https://api.bintray.com/conan/sigmoidal/public-conan"

## Upload

    $ conan upload ragel_install/6.10@sigmoidal/stable --all -r sigmoidal

### License
[GNU GPL v2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
