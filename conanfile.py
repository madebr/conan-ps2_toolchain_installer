# -*- coding: utf-8 -*-

from conans import ConanFile, tools
from conans.util.env_reader import get_env
from contextlib import contextmanager
import os
import shutil
import tempfile


class Ps2ToolchainInstallerConan(ConanFile):
    name = "ps2_toolchain_installer"
    version = "20190225"
    license = "GPL-2.0"
    author = "Anonymous Maarten <anonymous.maarten@gmail.com>"
    url = "https://www.github.com/rwengine/conan-ps2_toolchain_installer"
    description = "ps2 toolchain"
    topics = ("ps2", "toolchain", "gcc", "binutils", "mips", "ee",)
    settings = "os_build", "arch_build", "compiler",
    exports_sources = "LICENSE.md",

    def system_requirements(self):
        if tools.os_info.with_yum or tools.os_info.with_apt:
            installer = tools.SystemPackageTool()
            packages = []
            if self.develop:
                packages.append("patch")
            for package in packages:
                installer.install(package)

    def build_requirements(self):
        self.build_requires("ucl/1.03@madebr/testing")

    def source(self):
        def github_fetch(ps2dev_project, commit, sha256):
            url = "https://github.com/ps2dev/{}/archive/{}.tar.gz".format(ps2dev_project, commit)
            filename = "ps2dev_{}_{}.tar.gz".format(ps2dev_project, commit)
            dlfilepath = os.path.join(tempfile.gettempdir(), filename)
            if os.path.exists(dlfilepath) and not get_env("PS2TOOLCHAININSTALLER_FORCE_DOWNLOAD", False):
                self.output.info("Skipping download. Using cached {}".format(dlfilepath))
            else:
                self.output.info("Downloading {} from {}".format(filename, url))
                tools.download(url, dlfilepath)
            tools.check_sha256(dlfilepath, sha256)
            tools.unzip(dlfilepath)
            extracted_dir = "{}-{}".format(ps2dev_project, commit)
            os.rename(extracted_dir, ps2dev_project)

        github_fetch("ps2toolchain",
                     "b690fc9eff3b1e35c6c25c5474d463076cfaf9c1",
                     "26bea0b5290a822ecabc090c020622677fe795f1497bded0f235b4bbf3106624")
        github_fetch("ps2eth",
                     "795b745d11a30480796537eb8b247eb249d6cbab",
                     "5bba58c8e2def2242e25bb8a213b69f066a71c06e49fad9ca96ee0fa679fcd49")
        github_fetch("ps2-packer",
                     "f6e53e773de836549f476cd4e2d34acba8890327",
                     "959a9069091555a3525f82f39510e0884ba3cdfeb934905967423c693a9cd8c1")

        tools.replace_in_file(os.path.join("ps2toolchain", "toolchain.sh"),
                              "DEPEND_SCRIPTS=(`ls ../depends/*.sh | sort`)",
                              "DEPEND_SCRIPTS=$(ls ../depends/*.sh | sort)")
        tools.replace_in_file(os.path.join("ps2toolchain", "toolchain.sh"),
                              "BUILD_SCRIPTS=(`ls ../scripts/*.sh | sort`",
                              "BUILD_SCRIPTS=$(ls ../scripts/*.sh | sort)")

    def _get_environment(self, ps2dev=None):
        if ps2dev is None:
            ps2dev = os.path.join(self.build_folder, "ps2dev")
        ps2sdk = os.path.join(ps2dev, "ps2sdk")
        paths = [
            os.path.join(ps2dev, "bin"),
            os.path.join(ps2dev, "dvp", "bin"),
            os.path.join(ps2dev, "ee", "bin"),
            os.path.join(ps2dev, "iop", "bin"),
            os.path.join(ps2sdk, "bin"),
        ]
        return ps2dev, ps2sdk, paths

    @contextmanager
    def _ps2dev_environment(self, ps2dev=None):
        ps2dev, ps2sdk, paths = self._get_environment(ps2dev)
        try:
            os.mkdir(ps2dev)
        except FileExistsError:
            pass
        try:
            os.mkdir(ps2sdk)
        except FileExistsError:
            pass
        env = {
            "PS2DEV": ps2dev,
            "PS2SDK": ps2sdk,
            "PATH": paths,
        }
        with tools.environment_append(env):
            yield

    def build(self):
        with self._ps2dev_environment():
            with tools.chdir(os.path.join(self.source_folder, "ps2toolchain")):
                self.run("sh '{}'".format(os.path.join(".", "toolchain.sh")))
                self.run("make -C {}".format((os.path.join(self.source_folder, "ps2eth"))))
            with tools.chdir(os.path.join(self.source_folder, "ps2packer")):
                self.run("make install")

    def package(self):
        self.copy("*", src=os.path.join(self.build_folder, "ps2dev", "bin"), dst=os.path.join(self.package_folder, "bin"))
        self.copy("*", src=os.path.join(self.build_folder, "ps2dev", "share"), dst=os.path.join(self.package_folder, "share"))
        self.copy("*", src=os.path.join(self.build_folder, "ps2dev", "dvp"), dst=os.path.join(self.package_folder, "dvp"))
        self.copy("*", src=os.path.join(self.build_folder, "ps2dev", "ee"), dst=os.path.join(self.package_folder, "ee"))
        self.copy("*", src=os.path.join(self.build_folder, "ps2dev", "iop"), dst=os.path.join(self.package_folder, "iop"))
        self.copy("*", src=os.path.join(self.build_folder, "ps2dev", "ps2sdk"), dst=os.path.join(self.package_folder, "ps2sdk"))
        shutil.rmtree(os.path.join(self.package_folder, "ps2sdk", "samples"))

        self.copy("LICENSE.md", src=self.source_folder, dst="licenses")

    def package_id(self):
        del self.info.settings.compiler

    def package_info(self):
        ps2dev, ps2sdk, paths = self._get_environment(os.path.join(self.package_folder, "bin"))

        self.output.info("Setting PS2DEV environment variable: {}".format(ps2dev))
        self.env_info.PS2DEV = ps2dev

        self.output.info("Setting PS2SDK environment variable: {}".format(ps2dev))
        self.env_info.PS2SDK = ps2sdk

        self.output.info("Extending PATH environment variable: {}".format(paths))
        self.env_info.PATH.append(paths)
