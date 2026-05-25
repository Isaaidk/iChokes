import cv2

def draw_detections(image, predictions):

    for pred in predictions:

        x = int(pred["x"])
        y = int(pred["y"])
        w = int(pred["width"])
        h = int(pred["height"])

        x1 = int(x - w / 2)
        y1 = int(y - h / 2)

        x2 = int(x + w / 2)
        y2 = int(y + h / 2)

        label = f"{pred['class']} {pred['confidence']:.2f}"

        cv2.rectangle(
            image,
            (x1, y1),
            (x2, y2),
            (0,255,255),
            2
        )

        cv2.putText(
            image,
            label,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0,255,255),
            2
        )

    return image