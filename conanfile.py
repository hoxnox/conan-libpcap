from nxtools import NxConanFile
from conans import AutoToolsBuildEnvironment, tools
from conans.tools import SystemPackageTool

class LibPcapConan(NxConanFile):
    name = "libpcap"
    description = "A system-independent library for user-level network packet capture."
    version = "1.8.1"
    options = {"shared":[True, False],       \
               "ipv6":[True, False],         \
               "canusb":[True, False],       \
               "bluetooth":[True, False],    \
               "snf":[True, False],          \
               "dbus":[True, False],         \
               "libnl":[True, False]}
    default_options = "shared=False",        \
                      "ipv6=True",          \
                      "canusb=False",        \
                      "bluetooth=False",     \
                      "snf=False",           \
                      "dbus=False",          \
                      "libnl=False"
    url = "https://github.com/hoxnox/conan-libpcap.git"
    license = "http://www.tcpdump.org/license.html"

    def system_requirements(self):
        package_tool = SystemPackageTool()
        package_tool.install(packages="bison flex", update=True)

    def do_source(self):
        self.retrieve("673dbc69fdc3f5a86fb5759ab19899039a8e5e6c631749e48dcd9c6f0c83541e",
            [
                'vendor://tcpdump.org/libpcap/libpcap-{version}.tar.gz'.format(version=self.version),
                'http://www.tcpdump.org/release/libpcap-{version}.tar.gz'.format(version=self.version)
            ], "libpcap-{v}.tar.gz".format(v = self.version))

    def do_build(self):
        build_dir = "{staging_dir}/src".format(staging_dir=self.staging_dir)
        tools.untargz("libpcap-{v}.tar.gz".format(v=self.version), build_dir)
        env_build = AutoToolsBuildEnvironment(self)
        with tools.environment_append(env_build.vars):
            self.run("cd {build_dir}/libpcap-{v} && ./configure --prefix=\"{staging}\""
                     " {shared} {ipv6} {canusb} {bluetooth} {snf} {dbus} {libnl}".format(
                         v = self.version,
                         build_dir=build_dir,
                         staging=self.staging_dir,
                         shared="--enable-shared --disable-static" if self.options.shared else "--enable-static --disable-shared",
                         ipv6="--enable-ipv6" if self.options.ipv6 else "--disable-ipv6",
                         canusb="--enable-canusb" if self.options.canusb else "--disable-canusb",
                         bluetooth="--enable-bluetooth" if self.options.bluetooth else "--disable-bluetooth",
                         dbus="--enable-dbus" if self.options.dbus else "--disable-dbus",
                         snf="--with-snf" if self.options.snf else "--without-snf",
                         libnl="--with-libnl" if self.options.snf else "--without-libnl"))
            self.run("cd {build_dir}/libpcap-{v} && make install".format(v = self.version, build_dir = build_dir))

    def do_package_info(self):
        self.cpp_info.libs = ["pcap"]

