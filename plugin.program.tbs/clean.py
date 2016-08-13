import urllib, urllib2, re, xbmcplugin, xbmcgui, xbmc, xbmcaddon
import os, sys, time, xbmcvfs, glob, shutil, datetime, zipfile, ntpath
import subprocess, threading

try:
    from sqlite3 import dbapi2 as database

except:
    from pysqlite2 import dbapi2 as database

def Remove_Textures():
    textures   =  xbmc.translatePath('special://home/userdata/Database/Textures13.db')
    try:
        dbcon = database.connect(textures)
        dbcur = dbcon.cursor()
        dbcur.execute("DROP TABLE IF EXISTS path")
        dbcur.execute("VACUUM")
        dbcon.commit()
        dbcur.execute("DROP TABLE IF EXISTS sizes")
        dbcur.execute("VACUUM")
        dbcon.commit()
        dbcur.execute("DROP TABLE IF EXISTS texture")
        dbcur.execute("VACUUM")
        dbcon.commit()
        dbcur.execute("""CREATE TABLE path (id integer, url text, type text, texture text, primary key(id))""")
        dbcon.commit()
        dbcur.execute("""CREATE TABLE sizes (idtexture integer,size integer, width integer, height integer, usecount integer, lastusetime text)""")
        dbcon.commit()
        dbcur.execute("""CREATE TABLE texture (id integer, url text, cachedurl text, imagehash text, lasthashcheck text, PRIMARY KEY(id))""")
        dbcon.commit()
    except:
        pass

def Wipe_Cache():
    PROFILE_ADDON_DATA = os.path.join(xbmc.translatePath(os.path.join('special://profile','addon_data')))
    ADDON_DATA         = os.path.join(xbmc.translatePath(os.path.join('special://home','userdata','addon_data')))
    HOME               = os.path.join(xbmc.translatePath('special://home'))
    cachelist = [
        (PROFILE_ADDON_DATA),
        (ADDON_DATA),
        (os.path.join(HOME,'cache')),
        #(os.path.join(HOME,'temp')),
        (os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')),
        (os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')),
        (os.path.join(ADDON_DATA,'script.module.simple.downloader')),
        (os.path.join(xbmc.translatePath(os.path.join('special://profile','addon_data','script.module.simple.downloader')))),
        (os.path.join(ADDON_DATA,'plugin.video.itv','Images')),
        (os.path.join(xbmc.translatePath(os.path.join('special://profile','addon_data','plugin.video.itv','Images'))))]

    for item in cachelist:
        if os.path.exists(item) and item != ADDON_DATA and item != PROFILE_ADDON_DATA:
            for root, dirs, files in os.walk(item):
                file_count = 0
                file_count += len(files)
                if file_count > 0:
                    for f in files:
                        try:
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                            print"### Successfully cleared "+str(file_count)+" files from "+os.path.join(item,d)
                        except:
                            print"### Failed to wipe cache in: "+os.path.join(item,d)
        else:
            for root, dirs, files in os.walk(item):
                for d in dirs:
                    if 'Cache' in d or 'cache' in d or 'CACHE' in d:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                            print"### Successfully wiped "+os.path.join(item,d)
                        except:
                            print"### Failed to wipe cache in: "+os.path.join(item,d)

# Genesis cache - held in database file
    try:
        genesisCache = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.genesis'), 'cache.db')
        dbcon = database.connect(genesisCache)
        dbcur = dbcon.cursor()
        dbcur.execute("DROP TABLE IF EXISTS rel_list")
        dbcur.execute("VACUUM")
        dbcon.commit()
        dbcur.execute("DROP TABLE IF EXISTS rel_lib")
        dbcur.execute("VACUUM")
        dbcon.commit()
    except:
        pass

Remove_Textures()
Wipe_Cache()
