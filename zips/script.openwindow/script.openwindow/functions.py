import urllib, urllib2, re, xbmcplugin, xbmcgui, xbmc, xbmcaddon, os, sys, time, xbmcvfs, datetime, zipfile, shutil, binascii, hashlib
import downloader, extract
import threading

ADDON_ID         = 'plugin.program.tbs'
ADDONID          = 'script.openwindow'
ADDON            = xbmcaddon.Addon(ADDONID)
LOG_PATH         = xbmc.translatePath('special://logpath')
HOME             = xbmc.translatePath('special://home')
ADDONS           = xbmc.translatePath('special://home/addons')
ADDON_DATA       = xbmc.translatePath('special://profile/addon_data')
INSTALL_COMPLETE = os.path.join(ADDONS,'packages','INSTALL_COMPLETE')
RUN_WIZARD       = os.path.join(ADDONS,'packages','RUN_WIZARD')
ZIP_SIZES        = os.path.join(ADDON_DATA, ADDON_ID, 'zipcheck')
MY_SOURCES       = os.path.join(ADDON_DATA, ADDONID, 'mysources.xml')
ZIP_PATH         = os.path.join(ADDONS, 'packages', '~~ZIPS~~')
SETTINGS_PATH    = os.path.join(ADDON_DATA, ADDON_ID, 'master_settings')
DIALOG           = xbmcgui.Dialog()
#-----------------------------------------------------------------------------
# Return the build info
def Build_Info():
    Build = ''
    if os.path.exists('/etc/release'):
        Build    = Text_File('/etc/release','r')

    if Build == '':
        logtext = Log_Check()
        Buildmatch  = re.compile('Running on (.+?)\n').findall(logtext)
        Build       = Buildmatch[0] if (len(Buildmatch) > 0) else ''
    return Build.replace(' ','%20')
#-----------------------------------------------------------------------------
# Check any zip files that are in packages/~~ZIPS~~/
# def Check_Sources():
#     content = Text_File(MY_SOURCES, 'r')

#     programs = re.search('<programs>[\s\S]*?<\/programs>', content)
#     xbmc.log('CONTENT: %s' % )
#     local_size = size_array[0] if (len(size_array) > 0) else '0'

# # Attempt to find the local_size
#         try:
#             mypath, local_size, myoem = local_size.split('|')
#         except:
#             local_size = 0

#     if local_size != size:
#         Install_Content(oem, path, local_path, local_size, size, content)
#         try:
#             os.remove(local_path)
#         except:
#             xbmc.log('Failed to remove zip file')
#-----------------------------------------------------------------------------
# Check any zip files that are in packages/~~ZIPS~~/
def Check_Zips(path, size, oem, local_path):
    local_size = 0
    content    = ''
    if os.path.exists(ZIP_SIZES):
        readfile = open(ZIP_SIZES, 'r')
        content  = readfile.read()
        readfile.close()

        size_array = re.compile('p="%s(.+?)"' % path).findall(content)
        local_size = size_array[0] if (len(size_array) > 0) else '0'

# Attempt to find the local_size
        try:
            mypath, local_size, myoem = local_size.split('|')
        except:
            local_size = 0

    if local_size != size:
        Install_Content(oem, path, local_path, local_size, size, content)
        try:
            os.remove(local_path)
        except:
            xbmc.log('Failed to remove zip file')
#-----------------------------------------------------------------------------
# Create Paths if they don't already exist
def Create_Paths(path):
    newdirs = []
    directories = path.split('/')
    directories.pop()

# Remove any blanks in the array (eg /storage on linux creates a blank entry at start of array)
    if directories[0] == '':
        directories[1] = '/'+directories[1]
    for item in directories:
        if item != '':
            newdirs.append(item)

    xbmc.log('DIRS: %s'%newdirs)
    rootpath = HOME
    for d in newdirs:
        rootpath = os.path.join(rootpath, d)
        if not os.path.exists(rootpath):
            try:
                os.makedirs(rootpath)
            except:
                xbmc.log('### Failed to create directory: %s' % rootpath)
#-----------------------------------------------------------------------------
# Return the CPU details
def CPU_Check():
    logtext     = Log_Check()
    CPUmatch    = re.compile('Host CPU: (.+?) available').findall(logtext)
    CPU         = CPUmatch[0] if (len(CPUmatch) > 0) else ''
    return CPU.replace(' ','%20')
#-----------------------------------------------------------------------------
# Encryption function
def Encrypt(mode, message):
    if mode == 'e':
        import random
        count = 0
        finaltext = ''
        while count < 4:
            count += 1
            randomnum = random.randrange(1, 31)
            hexoffset = hex(randomnum)[2:]
            if len(hexoffset)==1:
                hexoffset = '0'+hexoffset
            finaltext = finaltext+hexoffset
        randomchar = random.randrange(1,4)
        if randomchar == 1: finaltext = finaltext+'0A'
        if randomchar == 2: finaltext = finaltext+'04'
        if randomchar == 3: finaltext = finaltext+'06'
        if randomchar == 4: finaltext = finaltext+'08'
        key1    = finaltext[-2:]
        key2    = int(key1,16)
        hexkey  = finaltext[-key2:-(key2-2)]
        key     = -int(hexkey,16)

# enctrypt/decrypt the message
        translated = ''
        finalstring = ''
        for symbol in message:
            num = ord(symbol)
            num2 = int(num) + key
            hexchar = hex(num2)[2:]
            if len(hexchar)==1:
                hexchar = '0'+hexchar
            finalstring = str(finalstring)+str(hexchar)
        return finalstring+finaltext
    else:
        key1    = message[-2:]
        key2    = int(key1,16)
        hexkey  = message[-key2:-(key2-2)]
        key     = int(hexkey,16)
        message = message [:-10]
        messagearray = [message[i:i+2] for i in range(0, len(message), 2)]
        numbers = [ int(x,16)+key for x in messagearray ]
        finalarray = [ str(unichr(x)) for x in numbers ]
        finaltext = ''.join(finalarray)
        return finaltext.encode('utf-8')
#-----------------------------------------------------------------------------
# Return mac address, not currently checked on Mac OS
def Get_Mac(protocol):
    cont    = 0
    counter = 0
    mac     = ''
    while mac == '' and counter < 5: 
        if sys.platform == 'win32': 
            mac = ''
            for line in os.popen("ipconfig /all"):
                if protocol == 'wifi':
                    if line.startswith('Wireless LAN adapter Wi'):
                        cont = 1
                    if line.lstrip().startswith('Physical Address') and cont == 1:
                        mac = line.split(':')[1].strip().replace('-',':').replace(' ','')
                        xbmc.log('(count: %s) (len: %s) wifi: %s' % (counter, len(mac), mac))
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1

                else:
                    if line.lstrip().startswith('Physical Address'): 
                        mac = line.split(':')[1].strip().replace('-',':').replace(' ','')
                        xbmc.log('(count: %s) (len: %s) ethernet: %s' % (counter, len(mac), mac))
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1

        elif sys.platform == 'darwin': 
            mac = ''
            if protocol == 'wifi':
                for line in os.popen("ifconfig en0 | grep ether"):
                    if line.lstrip().startswith('ether'):
                        mac = line.split('ether')[1].strip().replace('-',':').replace(' ','')
                        xbmc.log('(count: %s) (len: %s) wifi: %s' % (counter, len(mac), mac))
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1

            else:
                for line in os.popen("ifconfig en1 | grep ether"):
                    if line.lstrip().startswith('ether'):
                        mac = line.split('ether')[1].strip().replace('-',':').replace(' ','')
                        xbmc.log('(count: %s) (len: %s) ethernet: %s' % (counter, len(mac), mac))
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1

        elif xbmc.getCondVisibility('System.Platform.Android'):
            mac = ''
            if os.path.exists('/sys/class/net/wlan0/address') and protocol == 'wifi':
                readfile = open('/sys/class/net/wlan0/address', mode='r')
            if os.path.exists('/sys/class/net/eth0/address') and protocol != 'wifi':
                readfile = open('/sys/class/net/eth0/address', mode='r')
            mac = readfile.read()
            readfile.close()
            try:
                mac = mac.replace(' ','')
                xbmc.log('(count: %s) (len: %s) mac: %s' % (counter, len(mac), mac))
                mac = mac[:17]
            except:
                mac = ''
                counter += 1

        else:
            if protocol == 'wifi':
                for line in os.popen("/sbin/ifconfig"): 
                    if line.find('wlan0') > -1: 
                        mac = line.split()[4]
                        xbmc.log('(count: %s) (len: %s) wifi: %s' % (counter, len(mac), mac))
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1

            else:
               for line in os.popen("/sbin/ifconfig"): 
                    if line.find('eth0') > -1: 
                        mac = line.split()[4] 
                        xbmc.log('(count: %s) (len: %s) ethernet: %s' % (counter, len(mac), mac))
                        if len(mac) == 17:
                            break
                        else:
                            mac = ''
                            counter += 1
    if mac == '':
        xbmc.log('#### CANNOT FIND MAC DETAILS ON YOUR DEVICE. THIS UNIT CANNOT CURRENTLY BE USED WITH OUR SERVICE')
        mac = 'Unknown'

    return str(mac)
#-----------------------------------------------------------------------------
# Return the params
def Get_Params():
    try:
        wifimac = Get_Mac('wifi').rstrip().lstrip()
    except:
        wifimac = 'Unknown'
    try:
        ethmac  = Get_Mac('eth0').rstrip().lstrip()
    except:
        ethmac  = 'Unknown'
    try:
        cpu     = CPU_Check().rstrip().lstrip()
    except:
        cpu     = 'Unknown'
    try:
        build   = Build_Info().rstrip().lstrip()
    except:
        build   = 'Unknown'

    if ethmac == 'Unknown' and wifimac != 'Unknown':
        ethmac = wifimac
    if ethmac != 'Unknown' and wifimac == 'Unknown':
        wifimac = ethmac

    if ethmac != 'Unknown' and wifimac != 'Unknown':
        return Encrypt('e', (wifimac+'&'+cpu+'&'+build+'&'+ethmac).replace(' ','%20'))
    else:
        return 'Unknown'
#-----------------------------------------------------------------------------
# If filesize differs from online we download new content
def Install_Content(oem, path, local_path, local_size = '', new_size = '', content = ''):
    remote_path = 'http://tlbb.me/custzip/%s/.kodi/%s' % (oem, path)
    Create_Paths(local_path)
    urllib.urlretrieve(remote_path, local_path)
    if remote_path.endswith('master_settings'):
        Set_New_Settings()

    if not '~~ZIPS~~' in path and path != '':
        xbmc.log('### UPDATED: %s' % path)
    
    else:
        xbmc.log('## ATTEMPTING TO EXTRACT ZIP')
        try:
            if zipfile.is_zipfile(local_path):
                extract.all(local_path, HOME)
                xbmc.log('## EXTRACTED SUCCESSFULLY')

            else:
                xbmc.log('### IMPORTANT: %s is not a valid zip file, it cannot be installed ####' % local_path)


# Grab an arary of each line in the zipsizes - will allow for multiple different zips in future
            if os.path.exists(ZIP_SIZES):
                with open(ZIP_SIZES) as f:
                    content = f.read().splitlines()

            else:
                content = []

# Write back each line apart from the one we're changing
            writefile = open(ZIP_SIZES, 'w')
            counter = 0
            for line in content:
                if not path in line:
                    if not counter:
                        writefile.write(line)
                    else:
                        writefile.write('\n'+line)
                    counter += 1

# Now write the new details to the end of that file
            writefile.write('p="%s|%s|%s"' % (path, new_size, oem))
            writefile.close()
    
        except:
            xbmc.log('### Failed to extract from %s' % local_path)
#-----------------------------------------------------------------------------
# Return the log contents
def Log_Check():
    xbmc.log('--- Log Check initiated ---')
    finalfile = 0
    logfilepath = os.listdir(LOG_PATH)
    for item in logfilepath:
        if item.endswith('.log') and not item.endswith('.old.log'):
            mylog        = os.path.join(LOG_PATH,item)
            lastmodified = os.path.getmtime(mylog)
            if lastmodified>finalfile:
                finalfile = lastmodified
                logfile   = mylog
    
    filename    = open(logfile, 'r')
    logtext     = filename.read()
    filename.close()
    return logtext
#-----------------------------------------------------------------------------
# Return the ethernet mac if it exists, if not return the wifi mac
def My_Mac():
    if Get_Mac('eth') != 'Unknown':
        return Get_Mac('eth')
    else:
        return Get_Mac('wifi')
#-----------------------------------------------------------------------------
# Open URL and return the contents
def Open_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 10.0; WOW64; Windows NT 5.1; en-GB; rv:1.9.0.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36 Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req, timeout = 20)
    link     = response.read()
    response.close()
    return link
#-----------------------------------------------------------------------------
def Set_New_Settings():
    xbmc.log('### Setting master settings ###')
    with open(SETTINGS_PATH) as file:
        content = file.read().splitlines()
    
    for line in content:
        setting, value = line.split('|')
        Set_Setting(setting, value)
#-----------------------------------------------------------------------------
# Set a setting via json, this one requires a list to be sent through whereas Set_Setting() doesn't.
def Set_Setting(setting, value):
    setting = '"%s"' % setting
    value = '"%s"' % value

    query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (setting, value)
    response = xbmc.executeJSONRPC(query)
    xbmc.log(query)
    xbmc.log('### Set [%s, %s]' % (setting, value))
    xbmc.log('### RETURN %s' % response)

    if 'error' in str(response):
        query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (setting, value.replace('"',''))
        response = xbmc.executeJSONRPC(query)
        xbmc.log(query)
        xbmc.log('### Set [%s, %s]' % (setting, value))
        xbmc.log('### RETURN %s' % response)
#-----------------------------------------------------------------------------
# Read or write to a file
def Text_File(path, mode, text = ''):
    textfile = open(path, mode)
    if mode == 'r':
        content  = textfile.read()
        textfile.close()
        return content
    if mode == 'w':
        textfile.write(text)
        textfile.close()
#-----------------------------------------------------------------------------
if __name__ == '__main__':
    if os.path.exists(MY_SOURCES):
        Check_Sources()

    try:
        if sys.argv[1]=='startup':
            startup = 1
        else:
            startup = 0
    except:
        startup = 0

# Make sure Kodi isn't playing any files, we don't want to interrupt anything
    if not startup:
        isplaying = xbmc.Player().isPlaying()
        while isplaying:
            xbmc.sleep(1000)
            isplaying = xbmc.Player().isPlaying()
        xbmc.executebuiltin('ActivateWindow(busydialog)')

    if not os.path.exists(ZIP_PATH):
        os.makedirs(ZIP_PATH)

    local_size   = 0
    url          = 'http://tlbb.me/login/trtv/update.php?x=%s' % Get_Params()

# If connected to the internet we do the updates
    try:
        link         = Open_URL(url).replace('\r','').replace('\n','').replace('\t','')
        update_array = re.compile('p="(.+?)"').findall(link)
        for item in update_array:
            path, size, oem = item.split('|')
            if path != '':
                local_path = os.path.join(HOME, path)
            
                if os.path.exists(local_path) and not '~~ZIPS~~' in path:
                    local_size = os.path.getsize(os.path.join(local_path))
                
                if str(local_size) != size and not '~~ZIPS~~' in path:
                    xbmc.log('## UPDATING %s' % path)
                    Install_Content(oem, path, local_path)

                elif '~~ZIPS~~' in path:
                    xbmc.log('### DOING ZIP CHECK')
                    Check_Zips(path, size, oem, local_path)

        if not startup:
            xbmc.executebuiltin("Dialog.Close(busydialog)")
        xbmc.log('### ALL UPDATES COMPLETE')
        if os.path.exists(RUN_WIZARD):
            try:
                os.makedirs(INSTALL_COMPLETE)
                xbmc.log('### Created install_complete folder')
            except:
                xbmc.log('### Failed to create install_complete folder')

# If not connected to the internet we try and load wifi settings
    except:
        xbmc.executebuiltin("Dialog.Close(busydialog)")
        DIALOG.ok(ADDON.getLocalizedString(30123), ADDON.getLocalizedString(30124))
        
        content = Log_Check()
        if xbmc.getCondVisibility('System.Platform.Android'):
            xbmc.executebuiltin('StartAndroidActivity(,android.settings.WIFI_SETTINGS)')
        
        elif 'Running on OpenELEC' in content or 'Running on LibreELEC' in content:
            try:
                xbmcaddon.Addon(id='service.openelec.settings').getAddonInfo('name')
                xbmc.executebuiltin('RunAddon(service.openelec.settings)')
            except:
                xbmcaddon.Addon(id='service.libreelec.settings').getAddonInfo('name')
                xbmc.executebuiltin('RunAddon(service.libreelec.settings)')