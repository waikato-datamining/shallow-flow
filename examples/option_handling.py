from shallowflow.base.source import DirectoryLister

dl = DirectoryLister()
# print the help string
print(dl.to_help())
# print the current options
print(dl.config)
# update an option
dl.config = {"debug": True}
print(dl.config)
# trying to update a non-existing option
dl.config = {"debug2": True}
print(dl.config)
print(dl.get("debug"))
# reset options
dl.configmanager.reset()
print(dl.get("debug"))
