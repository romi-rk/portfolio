import cv2
import numpy as np
import pandas as pd


def parse_bbox(bbox_str):
    return [float(v) for v in bbox_str.strip('[]').split()]


def draw_border(img, top_left, bottom_right, color=(0, 255, 0), thickness=10, line_length=100):
    x1, y1 = top_left
    x2, y2 = bottom_right
    cv2.line(img, (x1, y1), (x1, y1 + line_length), color, thickness)
    cv2.line(img, (x1, y1), (x1 + line_length, y1), color, thickness)
    cv2.line(img, (x1, y2), (x1, y2 - line_length), color, thickness)
    cv2.line(img, (x1, y2), (x1 + line_length, y2), color, thickness)
    cv2.line(img, (x2, y1), (x2 - line_length, y1), color, thickness)
    cv2.line(img, (x2, y1), (x2, y1 + line_length), color, thickness)
    cv2.line(img, (x2, y2), (x2, y2 - line_length), color, thickness)
    cv2.line(img, (x2, y2), (x2 - line_length, y2), color, thickness)
    return img


results = pd.read_csv('test_interpolated.csv')

cap = cv2.VideoCapture('example.mp4')
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter('out.mp4', fourcc, fps, (width, height))

license_plate = {}
for car_id in np.unique(results['car_id']):
    car_rows = results[results['car_id'] == car_id]
    best_row = car_rows.loc[car_rows['license_number_score'].astype(float).idxmax()]
    license_plate[car_id] = str(best_row['license_number'])

frame_nmr = -1
ret = True
while ret:
    ret, frame = cap.read()
    frame_nmr += 1
    if ret:
        df_ = results[results['frame_nmr'] == frame_nmr]
        for row_indx in range(len(df_)):
            car_x1, car_y1, car_x2, car_y2 = parse_bbox(df_.iloc[row_indx]['car_bbox'])
            draw_border(frame, (int(car_x1), int(car_y1)), (int(car_x2), int(car_y2)),
                        (0, 255, 0), 8, line_length=60)

            x1, y1, x2, y2 = parse_bbox(df_.iloc[row_indx]['license_plate_bbox'])
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 3)

            car_id = df_.iloc[row_indx]['car_id']
            text = license_plate.get(car_id, '')

            (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)
            cv2.putText(frame, text,
                        (int((car_x1 + car_x2 - text_width) / 2), max(int(car_y1) - 15, 30)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)

        out.write(frame)

out.release()
cap.release()
print("Done, saved to out.mp4")