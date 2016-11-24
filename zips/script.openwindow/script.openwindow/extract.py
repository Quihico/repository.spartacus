import zipfile, xbmc, os

def all(_in, _out, dp = None):
    if os.path.exists(_in):
        zin    = zipfile.ZipFile(_in,  'r')
        nFiles = float(len(zin.infolist()))
        count  = 0

        for item in zin.infolist():
            try:
                count += 1
                update = count / nFiles * 100
                if dp:
                    dp.update(int(update))
                zin.extract(item, _out)
        
            except Exception, e:
                xbmc.log(str(e))

        return True