import os
from shallowflow.base.controls import Flow, Branch, Trigger, run_flow
from shallowflow.base.sinks import ConsoleOutput
from shallowflow.base.sources import FileSupplier, GetVariable
from shallowflow.base.transformers import IncVariable, SetVariable
from shallowflow.cv2.sinks import ImageFileWriter, VideoWriter
from shallowflow.cv2.transformers import VideoFileReader
from shallowflow.api.io import File

flow = Flow().manage([
    FileSupplier({"files": [File("./data/track_book.mjpeg")]}),
    VideoFileReader({"nth_frame": 2, "max_frames": 10}),  # extract every 2nd frame, but only 10 at most
    IncVariable({"var_name": "i"}),
    SetVariable({"var_name": "out_file", "var_value": "./output/track_book-@{i}.jpg", "expand": True}),  # filename for frame
    Branch().manage([
        Trigger({"name": "output filenames of frames"}).manage([  # output filename of frames
            GetVariable({"var_name": "out_file"}),
            ConsoleOutput({"prefix": "saving: "}),
        ]),
        ImageFileWriter({"output_file": "@{out_file}"}),
        VideoWriter({"output_file": File("./output/track_book.avi")}),
    ]),
])

msg = run_flow(flow, dump_file="./output/" + os.path.splitext(os.path.basename(__file__))[0] + ".json")
if msg is not None:
    print(msg)
