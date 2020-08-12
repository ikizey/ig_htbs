from pathlib import Path
from csv import DictReader

from PIL import Image


def read_from_csv(file_path):
    with open(file_path, 'r') as quotes:
        lines = DictReader(quotes, delimiter='\t', quotechar='"')
        for line in lines:
            yield line['quote'], line['author'], line['post_date']


def dict_of_images(path: Path) -> dict:
    # # smart but fuck it, i only have 2
    # files = [file for file in path.iterdir() if file.suffix == '.jpeg']
    # backgrouds = [Image.open(str(file)).convert("RGBA") for file in files]
    # # keys go like this : 0, 2, 4, 6 ...
    # backgrouds = {
    #     k: v for k, v in zip((z * 2 for z in range(len(backgrouds))), backgrouds)
    # }

    bgs_paths = (path.joinpath("bg_green.jpeg"), path.joinpath("bg_blue.jpeg"))
    backgrounds = [Image.open(str(file)).convert("RGBA") for file in bgs_paths]
    bgs = {0: backgrounds[0], 2: backgrounds[1]}
    return bgs


if __name__ == "__main__":

    from utils import MyInstaImgCreator

    BASE_DIR = Path(__file__).resolve().parent  # Django? :)

    static = BASE_DIR.joinpath("static")  # backgorunds and csv with data
    out = BASE_DIR.joinpath("out")

    backgorunds = dict_of_images(static)

    iic = MyInstaImgCreator()

    counter = 0
    for quote, author, date in read_from_csv(static.joinpath("quotes.tsv")):
        iic.quote = quote
        iic.author = author

        ## use different backgrounds: 2 green 2 blue repeat
        if counter == 0 or counter == 2:
            iic.image = backgorunds[counter]
        counter = 0 if counter > 3 else counter + 1

        out_file_path = str(out.joinpath(f"{date}.jpeg"))
        iic.get_complete_image().save(out_file_path, "JPEG2000")

        break
