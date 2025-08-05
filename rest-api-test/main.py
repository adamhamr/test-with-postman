from fastapi import FastAPI, Request
from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
import logging
from logging.handlers import RotatingFileHandler
import sys
from transformers import AutoTokenizer
from threading import Lock

# --- Logging Setup ---
logger = logging.getLogger("suggestion_api")
logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler("suggestion_api.log", maxBytes=5 * 1024 * 1024, backupCount=3)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))

logger.addHandler(file_handler)
logger.addHandler(console_handler)

# --- App and Tokenizer ---
app = FastAPI()
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
call_count = 0
counter_lock = Lock()

# --- BUG 1: Python Version Check Block ---
if sys.version_info >= (3, 12):
    raise RuntimeError("This server only supports Python 3.12 or lower.")  # --- Bug 1

# --- Central Color List ---
COMMON_COLORS = [
    'red', 'blue', 'green', 'yellow', 'black', 'white', 'gray', 'orange',
    'pink', 'purple', 'brown', 'cyan', 'magenta', 'lime', 'indigo',
    'gold', 'silver', 'beige'
]

# --- BUG 2: Removing second color from COMMON_COLORS ---
del COMMON_COLORS[1]  # --- Bug 2

# --- Schema ---
class InputData(BaseModel):
    name: str = Field(..., min_length=1)
    age: Optional[int] = Field(None, ge=1, le=100)
    favorite_color: Optional[Literal[tuple(COMMON_COLORS)]] = Field(
        None,
        description="Choose a color from the common list"
    )

    @validator("name")
    def name_not_blank(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be blank")
        return v

# --- Suggestion Endpoint ---
@app.post("/suggest")
def suggest(data: InputData, request: Request):
    global call_count
    with counter_lock:
        call_count += 1
        current_call = call_count

    logger.info(f"Request #{current_call} from {request.client.host} - data: {data.json()}")

    name_clean = data.name.strip()

    # --- BUG 3: Encoding the name (instead of keeping it string) ---
    name_clean = tokenizer.convert_ids_to_tokens(tokenizer.encode(name_clean, add_special_tokens=False))  # --- Bug 3

    suggestion = f"Hi {name_clean}!"

    if data.age:
        if data.age < 18:
            suggestion += " You're quite young! Keep learning and exploring."
        elif data.age < 60:
            suggestion += " Hope you're balancing work and fun!"
        else:
            suggestion += " Enjoy your golden years!"

    if data.favorite_color:
        suggestion += f" Also, {data.favorite_color} is a beautiful color!"

    # --- BUG 4: Every 5th call returns -999 token count ---
    if current_call % 5 == 0:
        logger.warning(f"Intentional token bug #1 injected on call #{current_call}")
        return {
            "suggestion": suggestion,
            "token_count": -999
        }  # --- Bug 4

    # --- BUG 5: On 7th call, return negative token count (flipped sign) ---
    if current_call == 7:
        tokens = tokenizer.encode(suggestion, add_special_tokens=False)
        token_count = -len(tokens)
        logger.error(f"Intentional token bug #2 (flipped sign) injected on call #{current_call}")
        return {
            "suggestion": suggestion,
            "token_count": token_count
        }  # --- Bug 5

    # --- Correct Behavior ---
    tokens = tokenizer.encode(suggestion, add_special_tokens=False)
    token_count = len(tokens)
    logger.info(f"Response #{current_call}: {suggestion} ({token_count} tokens)")

    return {
        "suggestion": suggestion,
        "token_count": token_count
    }
