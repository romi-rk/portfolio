\# License Plate Detection and Recognition (ANPR)



A complete automatic number plate recognition pipeline built from scratch: detecting vehicles and license plates in traffic footage, tracking each vehicle across frames, reading the plate text, and rendering an annotated output video.

\## What it does



Given a traffic video, the pipeline:

1\. Detects vehicles (cars, trucks, buses, motorcycles) using a pretrained YOLO26 COCO model.

2\. Detects license plates using a YOLO26 detector I trained myself on a labeled plate dataset.

3\. Tracks each vehicle across frames with SORT (Simple Online and Realtime Tracking), so a reading can be tied to a specific car over time rather than just a single frame.

4\. Crops each detected plate and reads the text with EasyOCR, applying UK plate format validation and character level correction (common OCR confusions like O and 0, or S and 5) to clean up the result.

5\. Picks the highest confidence reading per tracked vehicle, interpolates bounding boxes for frames where detection briefly dropped out, and renders a final annotated video with each vehicle's best plate reading overlaid.





\## Tech stack



Python, Ultralytics YOLO26, OpenCV, EasyOCR, SORT tracking, NumPy, pandas, SciPy (for interpolation), trained locally on an NVIDIA RTX 4070 with CUDA.



\## Training the plate detector



The plate detector was trained on a labeled dataset from Roboflow Universe (license plate images in YOLO format), starting from a smaller european plates dataset and later retrained on a larger 24,000 plus image UK specific dataset for comparison. Final detector performance: precision 0.94, recall 0.96, mAP50 0.985 on the original run.



\## Results



Tested against real UK highway footage with manually verified ground truth plates, the pipeline correctly read 63% of plates exactly right, with most remaining errors being genuine single character OCR confusions between visually similar letters (for example V and W, or C and G) rather than detection or tracking failures, which is a fairly typical error profile for this kind of unconstrained real world footage.

## Example output

![Vehicle and plate detection with tracking](docs/screenshot_1.png)
![Vehicle and plate detection with tracking](docs/screenshot_2.png)