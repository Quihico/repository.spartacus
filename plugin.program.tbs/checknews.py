import xbmc, default, binascii
xbmc.log("### starting Grab Updates")
default.Grab_Updates(binascii.unhexlify('687474703a2f2f746c62622e6d652f636f6d6d2e7068703f783d'))
xbmc.executebuiltin('RunScript(special://home/addons/script.openwindow/functions.py)')