def bounding_box_to_points(bbox):
    min_lat, max_lat, min_lon, max_lon = bbox

    points = [
        (min_lat, min_lon),  # Bottom-left
        (min_lat, max_lon),  # Bottom-right
        (max_lat, min_lon),  # Top-left
        (max_lat, max_lon)  # Top-right
    ]

    return points


def get_bb_points(boundingbox):
    # Convert string values to floats
    boundingbox = list(map(float, boundingbox))

    # Get the four corner points
    points = bounding_box_to_points(boundingbox)
    return points
