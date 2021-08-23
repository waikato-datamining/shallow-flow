import os
import tempfile
from shallowflow.base.sources import DirectoryLister
from shallowflow.api.io import save_actor, load_actor
from shallowflow.base.help import PlainText

dl = DirectoryLister()

# print the help string
PlainText().generate(dl)

print("\nOption setting/getting\n======================")
# print the current options
print(dl.options)
# update an option
dl.options = {"debug": True}
print(dl.options)
# update an option with wrong type
dl.options = {"debug": 42}
print(dl.options)
# trying to update a non-existing option
dl.options = {"debug2": True}
print(dl.options)
print(dl.get("debug"))
# reset options
dl.option_manager.reset()
print(dl.get("debug"))

# save to file
print("\nI/O\n===")
dl.options = {"debug": True, "dir": tempfile.gettempdir(), "list_files": True, "recursive": True}
print("actor:", dl.options)
fname = os.path.join(tempfile.gettempdir(), "out.json")
print("Saving actor to: %s" % fname)
msg = save_actor(dl, fname)
if msg is not None:
    raise Exception(msg)
print("Loading actor from: %s" % fname)
dl2 = load_actor(fname)
print("actor:", dl.options)
