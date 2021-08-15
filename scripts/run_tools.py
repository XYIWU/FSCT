from preprocessing import Preprocessing
from inference import SemanticSegmentation
from post_segmentation_script import PostProcessing
from report_writer import ReportWriter
import glob
import numpy as np
from measure import MeasureTree
import tkinter as tk
import tkinter.filedialog as fd
import glob
import os
import sys


def FSCT(parameters, preprocess=True, segmentation=True, postprocessing=True, measure_plot=True, make_report=True, clean_up_files=False):
    print(parameters['point_cloud_filename'])

    if preprocess:
        preprocessing = Preprocessing(parameters)
        preprocessing.preprocess_point_cloud()
        del preprocessing

    if segmentation:
        sem_seg = SemanticSegmentation(parameters)
        sem_seg.inference()
        del sem_seg

    if postprocessing:
        object_1 = PostProcessing(parameters)
        object_1.process_point_cloud()
        del object_1

    if measure_plot:
        measure1 = MeasureTree(parameters)
        measure1.run_measurement_extraction()
        del measure1

    if make_report:
        report_writer = ReportWriter(parameters)
        report_writer.make_report()

    if clean_up_files:
        report_writer = ReportWriter(parameters)
        report_writer.clean_up_files()


def directory_mode():
    root = tk.Tk()
    point_clouds_to_process = []
    directory = fd.askdirectory(parent=root, title='Choose directory')
    unfiltered_point_clouds_to_process = glob.glob(directory + '/**/*.las', recursive=True)
    for i in unfiltered_point_clouds_to_process:
        if 'FSCT_output' not in i:
            point_clouds_to_process.append(i)
    root.destroy()
    return point_clouds_to_process


def file_mode():
    root = tk.Tk()
    point_clouds_to_process = fd.askopenfilenames(parent=root, title='Choose files',
                                                  filetypes=[("LAS", "*.las"), ("LAZ", "*.laz"), ("CSV", "*.csv")])
    root.destroy()
    return point_clouds_to_process
