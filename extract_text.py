import json
import os.path
import sys
from dataclasses import dataclass
from itertools import groupby
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


@dataclass
class Fragment:
    pos: Point
    text: str
    level: float
    width: int
    height: int
    line_number: int = 0

    @classmethod
    def build(cls, item: dict):
        [[x0, y0], [x1, _], [_, y2]] = item["points"][:-1]

        width = x1 - x0
        height = y2 - y0
        text = item["str"]
        if text == "":
            text = " "
        return cls(Point(x0, y2), text, item["level"], width, height)


def main(files: list[str]):
    for file in files:
        if not os.path.exists(file):
            print(file, "not found")
            continue
        fragments = [Fragment.build(item) for item in load_json(file)]
        width, height = get_text_metrics(fragments)

        set_line_number(fragments, height)

        text = ""
        key_func = lambda f: f.line_number  # noqa:E731
        for _, grp in groupby(sorted(fragments, key=key_func), key=key_func):
            lst = sorted(grp, key=lambda f: f.pos.x)
            for n, f in enumerate(lst[:-1]):
                text += f.text
                # fragment 間の距離に応じた空白を出力
                n_spaces = (lst[n + 1].pos.x - (f.pos.x + f.width) + width - 1) // width
                text += " " * n_spaces
            text += lst[-1].text + "\n"
        with open(txt_filename(file), "w") as fp:
            fp.write(text)
        print(f"{file}: write {txt_filename(file)}")


def load_json(file):
    with open(file) as fp:
        return json.load(fp)


def get_text_metrics(fragments: list[Fragment]) -> tuple[int]:
    """平均文字幅と平均高さを計算"""
    total_width = 0
    total_chars = 0
    total_height = 0
    for f in fragments:
        total_width += f.width
        total_chars += len(f.text)
        total_height += f.height

    return total_width // total_chars, total_height // len(fragments)


def set_line_number(fragments, height):
    """行番号を計算"""
    for f in fragments:
        f.line_number = (f.pos.y + height - 1) // height


def txt_filename(file):
    base, _ = os.path.splitext(file)
    return base + ".txt"


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(f"usage: py {os.path.exists(__file__)} file [file ...]")
        exit()
    main(sys.argv[1:])
