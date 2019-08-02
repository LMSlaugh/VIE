from imageai.Detection import VideoObjectDetection

detector = VideoObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath("DataFiles\\yolo.h5")
detector.loadModel()
video_path = detector.detectObjectsFromVideo(input_file_path=os.path.join(execution_path, "traffic.mp4"),output_file_path=os.path.join(execution_path, "traffic_detected"), frames_per_second=20, log_progress=True)