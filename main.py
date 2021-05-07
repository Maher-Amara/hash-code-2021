def input_data_set(file):
    data = dict()
    with open(file) as f:
        line1 = f.readline()
        duration, nbr_intersections, nbr_streets, nbr_cars, score = line1.split()

        data['duration'] = int(duration)
        data['nbr_intersections'] = int(nbr_intersections)
        data['nbr_streets'] = int(nbr_streets)
        data['nbr_cars'] = int(nbr_cars)
        data['score'] = int(score)
        streets = list()
        for _ in range(data['nbr_streets']):
            street_data = f.readline().split()
            street = {
                'name': street_data[2],
                'start_intersection': int(street_data[0]),
                'end_intersection': int(street_data[1]),
                'street_duration': int(street_data[3]),
            }
            streets += [street]
        data['streets'] = streets

        cars_data = f.readlines()
        cars = list()
        for car_data in cars_data:
            car = car_data[:-1].split()[1:]
            cars += [car]
        data['cars'] = cars
        return data


def out_put(data, file):
    output_directory = 'result/'
    with open(output_directory + file, 'w')as f:
        data_text = str()
        data_text += str(data['nbr_intersections']) + '\n'
        for intersection in data['intersections']:
            data_text += str(intersection['id']) + '\n'
            data_text += str(intersection['nbr_in_streets']) + '\n'
            for street in intersection['streets']:
                data_text += str(street['name']) + ' ' + str(street['duration']) + '\n'
        f.write(data_text)


def street_score(car_paths, street):
    a = 1
    b = 1
    c = 1
    score = 0
    for path in car_paths:
        if street in path:
            score += path.index(street) / len(path)
    return score


def street_duration(street_name, car_paths):
    score = street_score(car_paths, street_name)
    if score > 0:
        duration = 2
    else:
        duration = 0

    return duration


def add_intersection(id, name, car_paths):
    duration = street_duration(name, car_paths)
    if duration > 0:
        intersection = {
            'id': id,
            'nbr_in_streets': 1,
            'streets': [
                {
                    'name': name,
                    'duration': duration  # duration in seconds
                }
            ]
        }
    else:
        intersection = 0

    return intersection


def intersection_data(data):
    intersections = list()
    for street in data['streets']:
        # first iteration
        if len(intersections) == 0:
            intersection = add_intersection(street['end_intersection'], street['name'], data['cars'])
            if intersection != 0:
                intersections += [intersection]
        else:
            # search for intersection
            intersection_found = False
            for intersection in intersections:
                if intersection['id'] == street['end_intersection']:
                    duration = street_duration(street['name'], data['cars'])
                    if duration > 0:
                        intersection['streets'] += [
                            {
                                'name': street['name'],
                                'duration': duration
                            }
                        ]
                        intersection['nbr_in_streets'] += 1

                    intersection_found = True
                    break

            if not intersection_found:
                # add intersection
                intersection = add_intersection(street['end_intersection'], street['name'], data['cars'])
                if intersection != 0:
                    intersections += [intersection]
    return intersections


def system(input_data):
    intersections = intersection_data(input_data)
    data = {
        'nbr_intersections': len(intersections),
        'intersections': intersections,
    }
    return data


def main():
    input_directory = 'input_files/'
    files = ['c.txt', 'e.txt', 'f.txt']  # 'a.txt', 'b.txt', 'c.txt', 'd.txt', 'e.txt', 'f.txt'
    for file in files:
        input_data = input_data_set(input_directory + file)
        out_put_data = system(input_data)
        out_put(out_put_data, file)


main()
