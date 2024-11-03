import cv2
import requests
import time

# Загрузка YOLO-модели
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# URL вашего Flask сервера
server_url = 'http://localhost:5000/update-road-status'

# Открытие камеры или видеофайла
cap = cv2.VideoCapture(0)  # Если хотите использовать видео, укажите путь к файлу

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Преобразование изображения для модели YOLO
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Подсчёт машин
    car_count = sum(1 for out in outs for detection in out if detection[5:].argmax() == 2 and detection[5:].max() > 0.5)

    # Определение цвета дороги
    color = "green"
    if car_count >= 30:
        color = "red"
    elif car_count >= 20:
        color = "orange"

    # Отправка данных на сервер
    data = {'road': 'Улица 1', 'color': color}
    requests.post(server_url, json=data)

    # Показ изображения для проверки
    cv2.imshow('Traffic Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
