import re, xbmcplugin, xbmcgui, xbmc, xbmcaddon, os, sys, time, shutil

def SF(command,SF_folder,SF_link):
    check4='SF'
# Check if folder exists, if not create folder and favourites.xml file
    folder = xbmc.translatePath(os.path.join(ADDON_DATA,'plugin.program.super.favourites','Super Favourites',SF_folder))
    SF_favs   = os.path.join(folder,'favourites.xml')
    
    if command=='add':

        if not os.path.exists(folder):
            os.makedirs(folder)
            localfile = open(SF_favs, mode='w+')
            localfile.write('<favourites>\n</favourites>')
            localfile.close()
        
# Grab content between favourites tags, we'll replace this later
        localfile2 = open(SF_favs, mode='r')
        content2 = localfile2.read()
        localfile2.close()

        favcontent    = re.compile('<favourite name="[\s\S]*?\/favourites>').findall(content2)
        faves_content = favcontent[0] if (len(favcontent) > 0) else '\n</favourites>'
        
# Copy clean contents of online SF command into memory - if we grab and pass through as paramater the /r /t /n etc. tags fail to translate correctly
        localfile = open(progresstemp, mode='r')
        newcontent = localfile.read()
        localfile.close()
        
#Write new favourites file
        if not newcontent in content2:
            localfile = open(SF_favs, mode='w+')
            if faves_content == '\n</favourites>':
                newfile = localfile.write('<favourites>\n\t'+newcontent+faves_content)
            else:
                newfile = localfile.write('<favourites>\n\t'+newcontent+'\n\t'+faves_content)
            localfile.close()
        
    if command=='delete':

# Grab content between favourites tags, we'll replace this later
        try:
            localfile2 = open(SF_favs, mode='r')
            content2 = localfile2.read()
            localfile2.close()

# Copy clean contents of online SF command into memory - if we grab and pass through as paramater the /r /t /n etc. tags fail to translate correctly
            localfile = open(progresstemp, mode='r')
            newcontent = localfile.read()
            localfile.close()
        
#Write new favourites file
            localfile = open(SF_favs, mode='w+')
            newfile = localfile.write(content2.replace('\n\t'+newcontent,''))
            localfile.close()
        except:
            pass

# Attempt to delete the SF folder
    if command=='delfolder':

        try:
            shutil.rmtree(folder)
        except:
            pass

