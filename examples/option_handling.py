from shallowflow.base.sources import DirectoryLister

dl = DirectoryLister()
# print the help string
print(dl.to_help())
# print the current options
print(dl.options)
# update an option
dl.options = {"debug": True}
print(dl.options)
# trying to update a non-existing option
dl.options = {"debug2": True}
print(dl.options)
print(dl.get("debug"))
# reset options
dl.option_manager.reset()
print(dl.get("debug"))
