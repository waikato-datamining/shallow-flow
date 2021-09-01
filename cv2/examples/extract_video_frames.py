from scoping import scoping
from shallowflow.base.controls import Flow, Branch, Trigger, run_flow
from shallowflow.base.sources import FileSupplier, GetVariable
from shallowflow.base.transformers import IncVariable, SetVariable
from shallowflow.base.sinks import ConsoleOutput
from shallowflow.cv2.transformers import VideoFileReader
from shallowflow.cv2.sinks import ImageFileWriter, VideoWriter

files = FileSupplier({"files": ["./data/track_book.mjpeg"]})

# extract every 2nd frame, but only 10 at most
frames = VideoFileReader({"nth_frame": 2, "max_frames": 10})

inc = IncVariable({"var_name": "i"})

# filename for frame
setvar = SetVariable({"var_name": "out_file", "var_value": "./output/track_book-@{i}.jpg", "expand": True})

branch = Branch()

# output filename of frames
with scoping():
    trig = Trigger({"name": "output filenames of frames"})
    trig.actors = [
        GetVariable({"var_name": "out_file"}),
        ConsoleOutput({"prefix": "saving: "})
    ]
    branch.append(trig)

# save frame as jpg
with scoping():
    writer = ImageFileWriter({"output_file": "@{out_file}"})
    branch.append(writer)

# save frame in video
with scoping():
    writer = VideoWriter({"output_file": "./output/track_book.avi"})
    branch.append(writer)

flow = Flow()
flow.actors = [files, frames, inc, setvar, branch]
msg = run_flow(flow)
if msg is not None:
    print(msg)
