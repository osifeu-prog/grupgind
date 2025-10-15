from PIL import Image
from pathlib import Path
from config import DST_ROOT, TARGET_SIZES
import logging

logger = logging.getLogger(__name__)

def process_image_file(src_path: str) -> list[tuple[str, tuple[int,int]]]:
    path = Path(src_path)
    img = Image.open(path)
    base = path.stem
    outputs = []

    DST_ROOT.mkdir(parents=True, exist_ok=True)
    for w, h in TARGET_SIZES:
        out_dir = DST_ROOT / f"{w}x{h}"
        out_dir.mkdir(exist_ok=True)
        out_path = out_dir / f"{base}_{w}x{h}{path.suffix}"
        img.resize((w, h), Image.LANCZOS).save(out_path)
        outputs.append((str(out_path), (w, h)))
        logger.info(f"Saved resized image: {out_path}")

    path.unlink()
    return outputs
