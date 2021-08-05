from os.path import expanduser
from shallowflow.base.sources import DirectoryLister

dl = DirectoryLister()
dl.set("dir", expanduser("~"))
dl.set("list_files", True)
dl.set("list_dirs", True)
dl.set("sort", True)
dl.set("recursive", True)
dl.set("max_items", 100)
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
