import base64
import json
import logging
import os
from pathlib import Path
from typing import List

from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion

from app.prompts import system_prompt, user_prompt

from . import APP_DIRECTORY

DATA_DIR = APP_DIRECTORY.parent / "data"

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"), organization=os.getenv("OPENAI_ORGANIZATION")
)


def get_dalle_prompts() -> List[str]:
    logging.info(f"Sending system prompt: {system_prompt}")
    logging.info(f"Sending user prompt: {user_prompt}")

    response: ChatCompletion = client.chat.completions.create(
        model=os.getenv("GPT_MODEL"),
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    logging.info(f"Got response: {response.model_dump()}")

    reply = response.model_dump()["choices"][0]["message"]["content"]
    reply_dict = json.loads(reply)
    return reply_dict["prompts"]


def save_image_to_jpg(b64_data: str, image_dir: Path) -> None:
    if not image_dir.exists():
        image_dir.mkdir(parents=True)

    with open(image_dir / "image.jpg", "wb") as f:
        f.write(base64.b64decode(b64_data))

    logging.info(f"Saved image to {image_dir}")


def get_dalle_images(prompt: str):
    logging.info(f"Sending prompt: {prompt}")
    response = client.images.generate(
        model=os.getenv("DALL_E_MODEL"),
        prompt=prompt,
        size=os.getenv("DALL_E_IMAGE_SIZE"),
        quality=os.getenv("DALL_E_IMAGE_QUALITY"),
        style=os.getenv("DALL_E_IMAGE_STYLE"),
        n=1,
        response_format="b64_json",
    )

    data = response.model_dump()
    logging.info(f"Got response: {data}")
    b64_data = response.data[0].b64_json

    image_dir = DATA_DIR / prompt
    save_image_to_jpg(b64_data, image_dir)


def main():
    prompts = get_dalle_prompts()
    for prompt in prompts:
        get_dalle_images(prompt)
