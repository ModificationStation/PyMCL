from mitmproxy import proxy, options, http
from mitmproxy.tools.dump import DumpMaster
import sys
import getopt

class AddHeader:
    @staticmethod
    def request(flow):
        if flow.request.pretty_host == "s3.amazonaws.com" or flow.request.pretty_host == "slins.minecraft.net":

            if doSoundFix:
                if flow.request.path.__contains__("MinecraftResources") or flow.request.path.__contains__("/resources/"):
                    flow.request.host = "resourceproxy.pymcl.net"
                    flow.request.path = "/MinecraftResources"

            if doSkinFix:
                if flow.request.path.__contains__("MinecraftSkins"):
                    flow.request.host = "resourceproxy.pymcl.net"
                    flow.request.path = "/skinapi.php?user=" + flow.request.path.split("/")[2].split(".")[0]

            if doCapeFix:
                if flow.request.path.__contains__("MinecraftCloaks"):
                    flow.request.host = "resourceproxy.pymcl.net"
                    flow.request.path = "/capeapi.php?user=" + flow.request.path.split("/")[2].split(".")[0]

        if flow.request.pretty_host.__contains__("minecraft.net"):
            if doSkinFix:
                if flow.request.path.__contains__("skin"):
                    flow.request.host = "resourceproxy.pymcl.net"
                    flow.request.path = "/skinapi.php?user=" + flow.request.path.split("/")[2].split(".")[0]

            if doCapeFix:
                if flow.request.path.__contains__("cloak"):
                    flow.request.host = "resourceproxy.pymcl.net"
                    flow.request.path = "/capeapi.php?user=" + flow.request.path.split("=")[1]


def start():
    myaddon = AddHeader()
    opts = options.Options(listen_host="0.0.0.0", listen_port=25560)
    pconf = proxy.config.ProxyConfig(opts)
    m = DumpMaster(opts)
    m.server = proxy.server.ProxyServer(pconf)
    m.addons.add(myaddon)

    try:
        m.run()
    except KeyboardInterrupt:
        m.shutdown()


doCapeFix = False
doSkinFix = False
doSoundFix = False
helptext = "Usage: python proxy.py (-s <true:false>; -k <true:false>)"
try:
    opts, args = getopt.getopt(sys.argv[1:], "hskc", ["soundfix", "skinfix", "capefix"])
except getopt.GetoptError:
    print(helptext)
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print(helptext)
        sys.exit()
    elif opt in ("-s", "--soundfix"):
        doSoundFix = True
    elif opt in ("-k", "--skinfix"):
        doSkinFix = True
    elif opt in ("-c", "--capefix"):
        doCapeFix = True
    else:
        print(helptext)
        sys.exit()

start()
