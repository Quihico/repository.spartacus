import sys
import re
import os
import xbmc
import xbmcgui
import urllib2
import urllib
import time
import downloader
import hashlib

from sqlite3 import dbapi2 as sqlite
from default import encryptme as encryptme
from default import URL_Params as URL_Params

dialog   = xbmcgui.Dialog()
dbpath   = xbmc.translatePath('special://profile/addon_data/plugin.program.tbs/social.db')

def DB_Open():
    global cur
    global con
    con = sqlite.connect(dbpath)
    cur = con.cursor()
    
if not os.path.exists(dbpath):
    DB_Open()
    cur.execute('create table shares(path TEXT, stamp TEXT);')
    con.commit()
    cur.execute('create table friends(id INTEGER, name TEXT, friendgroup TEXT, PRIMARY KEY(id));')
    con.commit()
    cur.execute('create table inbox(id INTEGER, fiendid INTEGER, message TEXT, read TEXT, PRIMARY KEY(id));')
    con.commit()
    cur.execute('create table sent(id INTEGER, fiendid INTEGER, message TEXT, read TEXT, PRIMARY KEY(id));')
    con.commit()
    cur.close()
    con.close()


def Open_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link     = response.read()
    response.close()
    if link=='':
        link='no response'
    return link
    
def Open_URL2(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    try:
        response = urllib2.urlopen(req, timeout = 30)
    except:
        response = 'no response'
    if response != 'no response':
        link     = response.read()
        response.close()
    else:
       link = 'no response'
        
    return link.replace('\r','').replace('\n','').replace('\t','')
 
if __name__ == '__main__':
    choice         = 0
    urlparams      = URL_Params()
    item           = sys.listitem.getLabel()
    item           = item.replace('[COLOR ]','').replace('[/COLOR]','')
    path           = xbmc.getInfoLabel('ListItem.FolderPath')
    xbmc.log('### ORIG PATH: %s' % path)
    path           = urllib.unquote(path)
    xbmc.log('### UNQUOTED PATH: %s' % path)
    try:
        scrap,fullpath = path.split('path=')
        xbmc.log('### FULL PATH ORIG: %s' % fullpath)
        fullpath       = xbmc.translatePath(fullpath)
    except:
        fullpath = "not a SF"
    xbmc.log('### FULL PATH FINAL: %s' % fullpath)
    
    if fullpath != "not a SF":
        localcheck = hashlib.md5(open(os.path.join(fullpath,'favourites.xml'),'rb').read()).hexdigest()
        xbmc.log('### md5: '+localcheck)
        mylistpath = urllib.quote(fullpath.split("HOME_",1)[1], safe='')
        xbmc.log('clean path: '+mylistpath)
        DB_Open()
        cur.execute("SELECT COUNT(*) from shares where path LIKE '"+mylistpath+"';")
        data = cur.fetchone()[0]
        if data:
            xbmc.log('### Updating Share in db: '+mylistpath)
            cur.execute("update shares set stamp='"+localcheck+"' where path LIKE '"+mylistpath+"';")
        else:
            xbmc.log('### Adding Share to db: '+mylistpath)
            cur.execute("insert into shares (path, stamp) values ('"+mylistpath+"','"+localcheck+"');")
        con.commit()
        cur.close()
        con.close()
    else:
        dialog.ok(item.capitalize()+' Not Submitted', 'Items must be added to a valid Super Favourite folder first.')


    try:
        scrap,newpath  = path.split('Super Favourites'+os.sep)
    except:
        newpath  = "not a SF"
        newpath = newpath.replace('\\','/')

    if os.path.exists(os.path.join(fullpath,'favourites.xml')):
        xmlfile  = open(os.path.join(fullpath,'favourites.xml'),'r')
        xml = xmlfile.read()
        xml = xml.replace(xbmc.translatePath('special://home'),'special://home/').replace(urllib.quote(xbmc.translatePath('special://home').encode("utf-8")),'special://home/').replace('\r','').replace('\n','').replace('\t','')
        xmlfile.close()
    else:
        xml="not a SF"
        
    try:
        cfgfile=open(os.path.join(fullpath,'folder.cfg'),'r')
        cfg = cfgfile.read()
        cfg = cfg.replace('\r','').replace('\n','').replace('\t','')
        cfgfile.close()
    except:
        cfg=''

    
    try:
        pluginname=xbmc.getInfoLabel('Container.PluginName')
        xbmc.log("### plugin name: %s" % str(pluginname))
    except:
        pluginname='none'

    quit = 0
    if pluginname == 'plugin.program.super.favourites':
# Enable once we have private share options
    #        choice = dialog.select('Choose Share Type',['Share publicly','Add to my private share'])
        if xml == "not a SF" or newpath  == "not a SF":
            dialog.ok('Empty Folder','This folder doesn\'t contain any content. Please populate with content and try again.')
            quit = 1
#        if choice == 0 and quit != 1:
        elif quit != 1:
            try:
                sendfaves = Open_URL2('http://tlbb.me/boxer/share.php?x=%s&z=gs&k=%s&c=%s&p=%s' % (encryptme('e',urlparams), encryptme('e',xml), encryptme('e',cfg), encryptme('e',newpath)))
                xbmc.log('http://tlbb.me/boxer/share.php?x=%s&z=gs&k=%s&c=%s&p=%s' % (encryptme('e',urlparams), encryptme('e',xml), encryptme('e',cfg), encryptme('e',newpath)))
                if 'success' in sendfaves:
                    dialog.ok('Content Submitted', 'Thank you for sharing with the community.',item+' has now been shared and is publicly available.')
                elif 'no response' in sendfaves:
                    dialog.ok(item.capitalize()+' Not Submitted', 'There was an error trying to contact the server, please try again later.')
                elif 'Too Long' in sendfaves:
                    dialog.ok(item.capitalize()+' Not Submitted', 'Super Favourites contents are too large, please trim down in size and try again.')
            except:
                dialog.ok(item.capitalize()+' Not Submitted', 'There was an error trying to add your content, please try again.')
#        if choice == 1 and quit != 1:
#            dialog.ok('Work In Progress','Sorry the private content section is currently a work in progress. Please check back soon.')
    if pluginname != 'plugin.program.super.favourites' and quit != 1:
        xbmc.executebuiltin('RunScript(special://home/addons/plugin.program.super.favourites/capture.py)')
#        dialog.ok('Not Yet Available','Currently the sharing menu can only be used from Super Favourites. New features will be unlocked over the coming months so check back soon!')
    

#    message = "Clicked on '%s'" % sys.listitem.getLabel()
#    print"Item: "+item
#    print"Location: "+xbmc.getInfoLabel('Container.FolderPath')
#    print"Path: "+xbmc.getInfoLabel('ListItem.FolderPath')
#    print"Addon_ID: "+xbmc.getInfoLabel('Container.PluginName')
#    xbmc.executebuiltin("Notification(\"Hello context items!\", \"%s\")" % message)