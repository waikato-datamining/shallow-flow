from scoping import scoping
from shallowflow.base.controls import Flow, Branch, run_flow
from shallowflow.base.sources import FileSupplier
from shallowflow.base.transformers import IncVariable
from shallowflow.imaging.transformers import VideoFrames
from shallowflow.imaging.sinks import ImageWriter, VideoWriter

files = FileSupplier({"files": ["./data/track_book.mjpeg"]})

# extract every 2nd frame, but only 10 at most
frames = VideoFrames({"nth_frame": 2, "max_frames": 10})

inc = IncVariable({"var_name": "i"})

branch = Branch()

with scoping():
    writer = ImageWriter({"output_file": "./output/track_book-@{i}.jpg"})
    branch.append(writer)

with scoping():
    writer = VideoWriter({"output_file": "./output/track_book.avi"})
    branch.append(writer)

flow = Flow()
flow.actors = [files, frames, inc, branch]
run_flow(flow)
