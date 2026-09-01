import csv
import numpy as np
from scipy.interpolate import interp1d


def parse_bbox(bbox_str):
    return [float(v) for v in bbox_str.strip('[]').split()]


def interpolate_bounding_boxes(data):
    frame_numbers = np.array([int(row['frame_nmr']) for row in data])
    car_ids = np.array([float(row['car_id']) for row in data])
    car_bboxes = np.array([parse_bbox(row['car_bbox']) for row in data])
    license_plate_bboxes = np.array([parse_bbox(row['license_plate_bbox']) for row in data])

    interpolated_data = []
    unique_car_ids = np.unique(car_ids)

    for car_id in unique_car_ids:
        car_mask = car_ids == car_id
        car_frame_numbers = frame_numbers[car_mask]
        car_bboxes_masked = car_bboxes[car_mask]
        license_plate_bboxes_masked = license_plate_bboxes[car_mask]

        car_bboxes_interpolated = []
        license_plate_bboxes_interpolated = []

        first_frame_number = car_frame_numbers[0]

        for i in range(len(car_bboxes_masked)):
            frame_number = car_frame_numbers[i]
            car_bbox = car_bboxes_masked[i]
            license_plate_bbox = license_plate_bboxes_masked[i]

            if i > 0:
                prev_frame_number = car_frame_numbers[i - 1]
                prev_car_bbox = car_bboxes_interpolated[-1]
                prev_license_plate_bbox = license_plate_bboxes_interpolated[-1]

                if frame_number - prev_frame_number > 1:
                    gap = frame_number - prev_frame_number
                    x = np.array([prev_frame_number, frame_number])
                    x_new = np.linspace(prev_frame_number, frame_number, num=gap, endpoint=False)

                    interp_func = interp1d(x, np.vstack((prev_car_bbox, car_bbox)), axis=0, kind='linear')
                    car_bboxes_interpolated.extend(interp_func(x_new)[1:].tolist())

                    interp_func = interp1d(x, np.vstack((prev_license_plate_bbox, license_plate_bbox)), axis=0, kind='linear')
                    license_plate_bboxes_interpolated.extend(interp_func(x_new)[1:].tolist())

            car_bboxes_interpolated.append(car_bbox.tolist())
            license_plate_bboxes_interpolated.append(license_plate_bbox.tolist())

        for i in range(len(car_bboxes_interpolated)):
            frame_number = first_frame_number + i
            row = {
                'frame_nmr': str(frame_number),
                'car_id': str(car_id),
                'car_bbox': '[{} {} {} {}]'.format(*car_bboxes_interpolated[i]),
                'license_plate_bbox': '[{} {} {} {}]'.format(*license_plate_bboxes_interpolated[i]),
            }

            if frame_number not in car_frame_numbers:
                row['license_plate_bbox_score'] = '0'
                row['license_number'] = '0'
                row['license_number_score'] = '0'
            else:
                original_row = [p for p in data
                                 if int(p['frame_nmr']) == frame_number and float(p['car_id']) == car_id][0]
                row['license_plate_bbox_score'] = original_row['license_plate_bbox_score']
                row['license_number'] = original_row['license_number']
                row['license_number_score'] = original_row['license_number_score']

            interpolated_data.append(row)

    return interpolated_data


with open('test.csv', 'r') as file:
    reader = csv.DictReader(file)
    data = list(reader)

interpolated_data = interpolate_bounding_boxes(data)

header = ['frame_nmr', 'car_id', 'car_bbox', 'license_plate_bbox',
          'license_plate_bbox_score', 'license_number', 'license_number_score']
with open('test_interpolated.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    writer.writerows(interpolated_data)

print("Done, saved test_interpolated.csv")