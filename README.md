[![Download](https://api.bintray.com/packages/bincrafters/public-conan/ragel_installer%3Abincrafters/images/download.svg) ](https://bintray.com/bincrafters/public-conan/ragel_installer%3Abincrafters/_latestVersion)
[![Build status](https://ci.appveyor.com/api/projects/status/github/bincrafters/conan-ragel_installer?branch=stable%2F6.10&svg=true)](https://ci.appveyor.com/project/bincrafters/conan-ragel_installer)

[Conan.io](https://conan.io) package recipe for [*ragel_installer*](http://www.colm.net/open-source/ragel).

Ragel compiles executable finite state machines from regular languages. Ragel targets C, C++ and ASM. 

The packages generated with this **conanfile** can be found on [Bintray](https://bintray.com/bincrafters/public-conan/ragel_installer%3Abincrafters).

## For Users: Use this package

### Basic setup

    $ conan install ragel_installer/6.10@bincrafters/stable

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    ragel_installer/6.10@bincrafters/stable


Complete the installation of requirements for your project running:

    $ mkdir build && cd build && conan install ..

Note: It is recommended that you run conan install from a build directory and not the root of the project directory.  This is because conan generates *conanbuildinfo* files specific to a single build configuration which by default comes from an autodetected default profile located in ~/.conan/profiles/default .  If you pass different build configuration options to conan install, it will generate different *conanbuildinfo* files.  Thus, they should not be added to the root of the project, nor committed to git.

## For Packagers: Publish this Package

The example below shows the commands used to publish to bincrafters conan repository. To publish to your own conan respository (for example, after forking this git repository), you will need to change the commands below accordingly.

## Build and package

The following command both runs all the steps of the conan file, and publishes the package to the local system cache.  This includes downloading dependencies from "build_requires" and "requires" , and then running the build() method.

    $ conan create bincrafters/stable



## Add Remote

    $ conan remote add bincrafters "https://api.bintray.com/conan/bincrafters/public-conan"

## Upload

    $ conan upload ragel_installer/6.10@bincrafters/stable --all -r bincrafters

## Package License
[https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html](LICENSE)

## Conan Recipe License

This conan recipe license applies only to the files of this recipe, which can be used to build and package ragel_installer. 
It does *not* in any way apply to the actual software being packaged.

*MIT License*

Copyright (c) 2017 Bincrafters

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
