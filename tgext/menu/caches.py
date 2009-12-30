import sys

from pylons import config
from tg.controllers import TGController

class entry(object):
    def __init__(self, path, name, extension, permission, url):
        self._path = path
        self._name = name
        self._extension = extension
        self._permission = permission
        self._url = url
        self.func = None
        
    def __str__(self):
        return '%s at %s' % (str(self._path), str(self._url))

class shared_menu_cache(object):
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state
        if not(hasattr(self, '_menuitems')):
            self._menuitems = {}

    def addEntry(self, menuitem):
        if menuitem._name not in self._menuitems:
            self._menuitems[menuitem._name] = {}
        self._menuitems[menuitem._name][menuitem._path] = menuitem
        
    def removeEntry(self, menuitem):
        if menuitem._name in self._menuitems:
            if menuitem._path in self._menuitems[menuitem._name]:
                del self._menuitems[menuitem._name][menuitem._path]
            
    def getEntry(self, menuname, path):
        if menuname in self._menuitems:
            if path in self._menuitems[menuname]:
                return self._menuitems[menuname][path]
            else:
                return None
        else:
            return None
        
        return None
    
    def removeMenu(self, menuname):
        if menuname in self._menuitems:
            del self._menuitems[menuname]
            
    def getMenu(self, menuname):
        return self._menuitems[menuname] if menuname in self._menuitems else dict()
    
    def updateUrls(self):
        pname = '%s.controllers.root' % (config['package'].__name__)
        __import__(pname)
        r = sys.modules[pname].RootController
        for menuname in self._menuitems:
            for menuitem in self._menuitems[menuname]:
                mi = self._menuitems[menuname][menuitem]
                mi._url = find_url(r, self._menuitems[menuname][menuitem])
                print self._menuitems[menuname][menuitem]
        1/0


def find_url(root, menuitem):
    n = menuitem.func.__name__
    if n in root.__dict__:
        if root.__dict__[n] is menuitem.func:
            return '/%s' % (n)
    for i in root.__dict__:
        if isinstance(root.__dict__[i], TGController):
            v = find_url(root.__dict__[i].__class__, menuitem)
            if v is not None:
                return '/%s%s' % (i, v)
    return None

shared_cache = shared_menu_cache()
