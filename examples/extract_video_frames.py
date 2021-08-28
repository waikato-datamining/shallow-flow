from shallowflow.base.controls import Flow, run_flow
from shallowflow.base.sources import FileSupplier
from shallowflow.base.transformers import IncVariable
from shallowflow.imaging.transformers import VideoFrames
from shallowflow.imaging.sinks import ImageWriter

files = FileSupplier({"files": ["./data/track_book.mjpeg"]})

# extract every 10th frame, but only 10 at most
frames = VideoFrames({"nth_frame": 10, "max_frames": 10})

inc = IncVariable({"var_name": "i"})

writer = ImageWriter({"output_file": "./output/track_book-@{i}.jpg"})

flow = Flow()
flow.actors = [files, frames, inc, writer]
run_flow(flow)
