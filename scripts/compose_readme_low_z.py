"""Place the two released low-z panels in the accepted README figure layout."""

from pathlib import Path

from PIL import Image


FIGURES = Path(__file__).resolve().parents[1] / "figures"


def main():
    with Image.open(FIGURES / "readme-combined-structural-high-z-pair-v1.png") as template:
        canvas = Image.new("RGB", template.size, "white")
        # The original header contains only the two generic panel labels.
        canvas.paste(template.crop((0, 0, template.width, 82)))

    for panel, left in [("surface3d", 30), ("contour-lines", 947)]:
        path = FIGURES / f"mpl-{panel}-combined-structural-low-z-v3.png"
        with Image.open(path) as source:
            height = 760
            width = round(source.width * height / source.height)
            scaled = source.convert("RGBA").resize((width, height), Image.Resampling.LANCZOS)
            canvas.paste(scaled, (left, 82), scaled)

    canvas.save(FIGURES / "readme-combined-structural-low-z-pair-v1.png")


if __name__ == "__main__":
    main()
