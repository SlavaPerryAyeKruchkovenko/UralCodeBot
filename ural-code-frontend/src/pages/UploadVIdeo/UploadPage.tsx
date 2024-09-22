import {useState, useRef, useEffect} from 'react';
import {Flex, Steps, Upload, Button, message} from "antd";
import {UploadOutlined} from '@ant-design/icons';
import axios from "axios";
import constants from "../../constants";

function UploadPage() {
    const [stage, setStage] = useState(1);
    const [videoFile, setVideoFile] = useState(null);
    const [file, setFile] = useState(null);
    const [imageSrc, setImageSrc] = useState('');
    const [floorPoints, setFloorPoints] = useState([]);
    const [doorPoints, setDoorPoints] = useState([]);

    const [loading, setLoading] = useState(false);
    const videoRef = useRef(null);
    const canvasRef = useRef(null);

    // Захватываем кадр из видео на 5-й секунде
    const captureFrame = () => {
        const videoElement = videoRef.current;
        const canvasElement = canvasRef.current;

        if (!canvasElement || !videoElement) {
            console.error("Canvas или Video элемент не найден.");
            return;
        }

        const context = canvasElement.getContext('2d');

        if (!context) {
            console.error("Не удалось получить 2D контекст для canvas.");
            return;
        }

        // Устанавливаем время на 5 секундах
        videoElement.currentTime = 5;

        // Ждем пока видео загрузится на 5 секунду
        videoElement.onseeked = () => {
            context.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);
            const image = canvasElement.toDataURL('image/png');
            setImageSrc(image); // Устанавливаем кадр как изображение
            setStage(2); // Переход к разметке
        };
    };



    const getBase64 = (file) =>
        new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => resolve(reader.result as string);
            reader.onerror = (error) => reject(error);
        });

    const handleVideoChange = (info: any) => {
        const file = info.file; // Используем originFileObj для получения исходного файла
        console.log({file})
        if (file) {
            const videoURL = URL.createObjectURL(file); // Создаем URL для видео
            console.log({videoURL})
            getBase64(file).then((res) => {
                console.log({res})
                setFile(res)
            })

            setVideoFile(videoURL); // Сохраняем URL видео
            message.success('Видео загружено');
            setStage(2); // Переключаемся на стадию разметки
        }
    };


    // Отправка данных на сервер
    const handleSubmit = async () => {
        // Пример отправки данных

        const reqFile = {
            file: file
        }
        const reqCoords = {
            doorCoors: doorPoints,
            sectionCoors: floorPoints,
        }

        console.log({
            reqFile,
            reqCoords
        })

        await axios.post(constants.apiUrl + 'coordinate', reqCoords
        ).then(async () => {
            message.success('Координаты отправлены, началась отправка видео!')

            setLoading(true)
            const data = await axios.post(constants.apiUrl + 'upload', reqFile, {
            }).then((result) => {
                message.success('Данные успешно отправлены!');
                setLoading(false)
                return result
            }).catch(() => {
                message.error('Ерор')
                setFloorConfirmed(false)
                setFloorPoints([])
                setDoorPoints([])
                setStage(2)
            })
        }).catch(() => {
            message.error('Ерор')
            setFloorConfirmed(false)
            setFloorPoints([])
            setDoorPoints([])
            setStage(2)
        })


    };

    // Добавляем точку по клику

    const handleCanvasClick = (event: any) => {
        const canvasElement = canvasRef.current;
        const canvasRect = canvasElement.getBoundingClientRect();
        const x = event.clientX - canvasRect.left;
        const y = event.clientY - canvasRect.top;

        // Добавляем новую точку
        setFloorPoints((prevPoints) => {
            const newPoints = [...prevPoints, { x, y }];

            // Перерисовываем холст с новыми точками и линиями
            drawPointsAndLines(newPoints, 'red');
            return newPoints;
        });

    };

    const handleCanvasDoorClick = (event: any) => {
        const canvasElement = canvasRef.current;
        const canvasRect = canvasElement.getBoundingClientRect();
        const x = event.clientX - canvasRect.left;
        const y = event.clientY - canvasRect.top;

        // Добавляем новую точку
        setDoorPoints((prevPoints) => {
            const newPoints = [...prevPoints, { x, y }];

            // Перерисовываем холст с новыми точками и линиями
            drawPointsAndLines(newPoints, 'green');
            return newPoints;
        });

    };

    const drawPointsAndLines = (points: { x: number, y: number }[], color: string) => {
        const canvasElement = canvasRef.current;
        const context = canvasElement.getContext('2d');

        if (!context) {
            console.error("Не удалось получить 2D контекст для canvas.");
            return;
        }

        // Очищаем холст перед перерисовкой
        context.clearRect(0, 0, canvasElement.width, canvasElement.height);

        // Рисуем фон (если есть изображение)
        if (imageSrc) {
            const background = new Image();
            background.src = imageSrc;
            background.onload = () => {
                context.drawImage(background, 0, 0, canvasElement.width, canvasElement.height);

                // Рисуем линии между точками
                if (points.length > 1) {
                    context.beginPath();
                    context.moveTo(points[0].x, points[0].y);

                    for (let i = 1; i < points.length; i++) {
                        context.lineTo(points[i].x, points[i].y);
                    }

                    // Если выбрано 4 точки, замыкаем фигуру
                    if (points.length >= 3) {
                        context.lineTo(points[0].x, points[0].y);
                    }

                    context.strokeStyle = color; // Цвет линии
                    context.lineWidth = 2; // Толщина линии
                    context.stroke();
                }

                // Рисуем точки поверх линий
                points.forEach((point) => {
                    context.beginPath();
                    context.arc(point.x, point.y, 5, 0, 2 * Math.PI); // Рисуем круг с радиусом 5
                    context.fillStyle = color; // Цвет точек
                    context.fill();
                });
            };
        }
    };

// Сброс точек и очистка холста
    const handleReset = () => {
        setFloorPoints([]); // Сбрасываем точки
        const canvasElement = canvasRef.current;
        const context = canvasElement.getContext('2d');
        context.clearRect(0, 0, canvasElement.width, canvasElement.height); // Очищаем холст
    };

    const handleDoorReset = () => {
        setDoorPoints([]); // Сбрасываем точки
        const canvasElement = canvasRef.current;
        const context = canvasElement.getContext('2d');
        context.clearRect(0, 0, canvasElement.width, canvasElement.height); // Очищаем холст
    };


    const [floorConfirmed, setFloorConfirmed] = useState(false)
// Подтверждение выбора
    const handleFloorConfirm = () => {
        if (floorPoints.length > 2) {
            message.success('Область успешно выбрана! Теперь выберите дверь!');
            // setStage(3)
            setFloorConfirmed(true)
        } else {
            message.error('Необходимо выбрать минимум 3 точки');
        }
    };

    const handleConfirm = () => {
        if (doorPoints.length > 2) {
            message.success('Область успешно выбрана!');
            setStage(3)
            // Логика для отправки точек или выполнения других действий
            handleSubmit().then()
            console.log({points: floorPoints})

        } else {
            message.error('Необходимо выбрать минимум 3 точки');
        }
    };

    return (
        <Flex vertical>
            <Steps current={stage - 1} items={[
                {
                    title: 'Загрузка видео',
                    description: 'Загрузите видео для обработки нейронной сетью.',
                },
                {
                    title: 'Разметка',
                    description: 'Ограничьте опасную зону, выбрав 4 точки.',
                },
                {
                    title: 'Получение результата',
                    description: 'Ожидайте результата обработки видео.',
                    status: stage === 3 && !loading ? 'process' : undefined
                }
            ]}/>

            {stage === 1 && (
                <Upload
                    beforeUpload={() => false}
                    onChange={handleVideoChange}
                    maxCount={1}
                >
                    <Button icon={<UploadOutlined/>}>Загрузить видео</Button>
                </Upload>
            )}

            {stage === 2 && (
                <div>
                    <video ref={videoRef} src={videoFile} style={{display: 'none'}}/>
                    <Button onClick={captureFrame}>Взять кадр на 5 сек</Button>
                </div>
            )}

            {stage === 2 && !floorConfirmed && (
                <div>
                    <p>Выберите 4 точки для замкнутой области опасной зоны:</p>
                    <canvas
                        ref={canvasRef}
                        width={500}
                        height={300}
                        style={{ backgroundImage: `url(${imageSrc})`, backgroundSize: 'cover' }}
                        onClick={handleCanvasClick}
                    />
                    <div style={{ marginTop: '10px' }}>
                        <Button type="primary" onClick={handleFloorConfirm} style={{ marginRight: '10px' }}>
                            Подтвердить выбор
                        </Button>
                        <Button onClick={handleReset}>
                            Сбросить
                        </Button>
                    </div>
                </div>
            )}

            {stage === 2 && floorConfirmed && (
                <div>
                    <p>Выберите 4 точки для выбора двери:</p>
                    <canvas
                        ref={canvasRef}
                        width={500}
                        height={300}
                        style={{ backgroundImage: `url(${imageSrc})`, backgroundSize: 'cover' }}
                        onClick={handleCanvasDoorClick}
                    />
                    <div style={{ marginTop: '10px' }}>
                        <Button type="primary" onClick={handleConfirm} style={{ marginRight: '10px' }}>
                            Подтвердить выбор
                        </Button>
                        <Button onClick={handleDoorReset}>
                            Сбросить
                        </Button>
                    </div>
                </div>
            )}
        </Flex>
    );
}

export default UploadPage;
