from mitmproxy import proxy, options, http
from mitmproxy.tools.dump import DumpMaster
import sys
import getopt
import requests
import json
import base64

class AddHeader:
    @staticmethod
    def request(flow):
        if flow.request.pretty_host == "s3.amazonaws.com":

            if doSoundFix == True:
                if flow.request.path.__contains__("MinecraftResources"):
                    flow.request.host = "resourceproxy.pymcl.net"

            if doSkinFix == True:
                if flow.request.path.__contains__("MinecraftSkins"):
                    response = requests.get("http://api.mojang.com/users/profiles/minecraft", verify=False)
                    uid = json.loads(response.content)["id"]
                    img64 = requests.get("http://sessionserver.mojang.com/session/minecraft/profile/" + uid, verify=False)
                    img = requests.get(base64.decode(img64)["textures"]["SKIN"])
                    flow.response = http.HTTPResponse.make(
                        200,
                        img,
                        {"Content-Type": "image/png"}
                    )

            if doCapeFix == True:
                if flow.request.path.__contains__("MinecraftCloaks"):
                    flow.request.host = "resourceproxy.pymcl.net"
                    flow.request.path = "/capeapi.php?user=" + flow.request.path.split("/")[2].split(".")[0]


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
