from os.path import expanduser
from shallowflow.base.sources import DirectoryLister
from shallowflow.api.io import Directory

dl = DirectoryLister({
    "dir": Directory(expanduser("~")),
    "list_files": True,
    "list_dirs": True,
    "sort": True,
    "recursive": True,
    "max_items": 100
})
msg = dl.setup()
if msg is None:
    msg = dl.execute()
    if msg is None:
        while dl.has_output():
            print(dl.output())
    else:
        print(msg)
else:
    print(msg)
