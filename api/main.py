from fastapi import FastAPI, File, UploadFile
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
from io import BytesIO

app = FastAPI()

# Загрузка модели и процессора
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

# Настройка параметров процессора
processor.clean_up_tokenization_spaces = True


@app.post("/generate-caption/")
async def generate_caption(file: UploadFile = File(...)):
    # Открытие загруженного изображения
    image = Image.open(BytesIO(await file.read()))

    # Проверка формата изображения и преобразование в PNG, если необходимо
    if image.format.lower() not in ["png", "jpeg", "jpg"]:
        image = image.convert("RGB")
        image_bytes = BytesIO()
        image.save(image_bytes, format="PNG")
        image_bytes.seek(0)
        image = Image.open(image_bytes)

    # Подготовка изображения для модели
    inputs = processor(images=image, return_tensors="pt")

    # Генерация описания
    outputs = model.generate(**inputs, max_new_tokens=20)
    caption = processor.decode(
        outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True
    )

    return {"caption": caption}
