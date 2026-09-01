import string
import easyocr

reader = easyocr.Reader(['en'], gpu=True)

dict_char_to_int = {'O': '0', 'I': '1', 'Z': '2', 'B': '3', 'A': '4', 'S': '5', 'T': '7', 'G': '9'}
dict_int_to_char = {'0': 'O', '1': 'I', '2': 'Z', '3': 'B', '4': 'A', '5': 'S', '6': 'B', '7': 'T', '8': 'B', '9': 'G'}


def write_csv(results, output_path):
    with open(output_path, 'w') as f:
        f.write('{},{},{},{},{},{},{}\n'.format('frame_nmr', 'car_id', 'car_bbox',
                                                  'license_plate_bbox', 'license_plate_bbox_score',
                                                  'license_number', 'license_number_score'))
        for frame_nmr in results.keys():
            for car_id in results[frame_nmr].keys():
                if 'car' in results[frame_nmr][car_id].keys() and \
                   'license_plate' in results[frame_nmr][car_id].keys() and \
                   'text' in results[frame_nmr][car_id]['license_plate'].keys():
                    f.write('{},{},{},{},{},{},{}\n'.format(
                        frame_nmr, car_id,
                        '[{} {} {} {}]'.format(*results[frame_nmr][car_id]['car']['bbox']),
                        '[{} {} {} {}]'.format(*results[frame_nmr][car_id]['license_plate']['bbox']),
                        results[frame_nmr][car_id]['license_plate']['bbox_score'],
                        results[frame_nmr][car_id]['license_plate']['text'],
                        results[frame_nmr][car_id]['license_plate']['text_score']))


def license_complies_format(text):
    if len(text) != 7:
        return False
    if (text[0] in string.ascii_uppercase or text[0] in dict_int_to_char.keys()) and \
       (text[1] in string.ascii_uppercase or text[1] in dict_int_to_char.keys()) and \
       (text[2] in '0123456789' or text[2] in dict_char_to_int.keys()) and \
       (text[3] in '0123456789' or text[3] in dict_char_to_int.keys()) and \
       (text[4] in string.ascii_uppercase or text[4] in dict_int_to_char.keys()) and \
       (text[5] in string.ascii_uppercase or text[5] in dict_int_to_char.keys()) and \
       (text[6] in string.ascii_uppercase or text[6] in dict_int_to_char.keys()):
        return True
    return False


def format_license(text):
    license_plate_ = ''
    mapping = {0: dict_int_to_char, 1: dict_int_to_char, 4: dict_int_to_char, 5: dict_int_to_char,
               6: dict_int_to_char, 2: dict_char_to_int, 3: dict_char_to_int}
    for j in range(7):
        if text[j] in mapping[j].keys():
            license_plate_ += mapping[j][text[j]]
        else:
            license_plate_ += text[j]
    return license_plate_


def read_license_plate(license_plate_crop):
    detections = reader.readtext(license_plate_crop, allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    for detection in detections:
        bbox, text, score = detection
        text = text.upper().replace(' ', '')
        if license_complies_format(text):
            return format_license(text), score
    return None, None


def get_car(license_plate, vehicle_track_ids):
    x1, y1, x2, y2, score, class_id = license_plate
    found_it = False
    for j in range(len(vehicle_track_ids)):
        xcar1, ycar1, xcar2, ycar2, car_id = vehicle_track_ids[j]
        if x1 > xcar1 and y1 > ycar1 and x2 < xcar2 and y2 < ycar2:
            car_index = j
            found_it = True
            break
    if found_it:
        return vehicle_track_ids[car_index]
    return -1, -1, -1, -1, -1