
from ara.download_utils import download_images
from ara.file_utils import read_text_file_to_list

urls = read_text_file_to_list("./result/image.urls", separator="\t")
urls = [x[0] for x in urls]
download_images(urls, "./result", max_workers=5, data_slices=5)

