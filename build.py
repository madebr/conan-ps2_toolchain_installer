#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conan.packager import ConanMultiPackager
from conans.client.tools.oss import detected_os
from conans.util.env_reader import get_env


if __name__ == "__main__":
    arch_str = get_env("ARCH", "x86,x86_64")
    archs = arch_str.split(",")

    builder = ConanMultiPackager(
        # docker_entry_script="pwd && ls",
    )
    for arch in archs:
        builder.add(settings={"arch_build": arch, "os_build": detected_os(), })
    builder.run()
