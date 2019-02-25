[![Download](https://api.bintray.com/packages/rwengine/public-conan/ps2toolchain%3Arwengine/images/download.svg) ](https://bintray.com/rwengine/public-conan/ps2toolchain%3Arwengine/_latestVersion)
[![Build Status](https://travis-ci.org/rwengine/conan-ps2toolchain.svg?branch=stable%2F20190225)](https://travis-ci.org/rwengine/conan-ps2toolchain)

[Conan.io](https://conan.io) package recipe for *ps2toolchain*.

<Description of Ps2toolchain here>

The packages generated with this **conanfile** can be found on [Bintray](https://bintray.com/rwengine/public-conan/ps2toolchain%3Arwengine).

## For Users: Use this package

### Basic setup

    $ conan install ps2toolchain/20190225@rwengine/stable

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    ps2toolchain/20190225@rwengine/stable

    [generators]
    txt

Complete the installation of requirements for your project running:

    $ mkdir build && cd build && conan install ..

Note: It is recommended that you run conan install from a build directory and not the root of the project directory.  This is because conan generates *conanbuildinfo* files specific to a single build configuration which by default comes from an autodetected default profile located in ~/.conan/profiles/default .  If you pass different build configuration options to conan install, it will generate different *conanbuildinfo* files.  Thus, they should not be added to the root of the project, nor committed to git.

## For Packagers: Publish this Package

The example below shows the commands used to publish to rwengine conan repository. To publish to your own conan respository (for example, after forking this git repository), you will need to change the commands below accordingly.

## Build and package

The following command both runs all the steps of the conan file, and publishes the package to the local system cache.  This includes downloading dependencies from "build_requires" and "requires" , and then running the build() method.

    $ conan create rwengine/stable



## Add Remote

    $ conan remote add rwengine "https://api.bintray.com/conan/rwengine/public-conan"

## Upload

    $ conan upload ps2toolchain/20190225@rwengine/stable --all -r rwengine


## Conan Recipe License

NOTE: The conan recipe license applies only to the files of this recipe, which can be used to build and package ps2toolchain.
It does *not* in any way apply or is related to the actual software being packaged.

[MIT](https://github.com/rwengine/conan-ps2_toolchain-installer.git/blob/master/LICENSE.md)
