## Personal tool that I use to create images for my Instagram and post them.

### `main.py` > generates images from tsv (tabbed csv) file
### `post.py` > posts generated image

**More details**:

`main.py` requires `quotes.tsv` and `bg_green.jpeg`, `bg_blue.jpeg` in `.\static` folder.
Produced images will be saved in `.\out` folder.

`quotes.tsv` requirements:
`quotes.tsv` should contain `auote`, `author` and `post_date` fields. `Tab` sparated, `"` as quotechar
`post_date` used to determine file name of produced image which in turn will be used to determine when to post it
I use "YYYY-MM-DD" format, but any should work.
`quote` length recommended `< 70` chars. This will be waped to fit into background image.

`post.py` takes images from `.\out` folder. It pick the one with current date in file name. Then posts in and moves to `.\out\posted` folder