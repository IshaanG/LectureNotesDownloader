import requests
import img2pdf
from urllib.parse import urlparse
import sys

page_url = sys.argv[1]
notes_id = urlparse(page_url).path.split('/')[2].split('-')[0]
notes_name = ' '.join(urlparse(page_url).path.split('/')[2].split('-')[1:])

base_url = "https://lecturenotes.in/material/v2/{}/page-{}?noOfItems=30"
page_data = []

for page_no in range(1, 1000, 30):
    r = requests.get(base_url.format(notes_id, page_no))
    if(not r.ok):
        break
    page_data.extend(r.json()['page'])

images = []
for row in page_data:
    image_url = "https://lecturenotes.in" + row['path']
    r = requests.get(image_url)
    images.append(r.content)

a4inpt = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297))
layout_fun = img2pdf.get_layout_fun(a4inpt)
with open(f"{notes_name}.pdf","wb") as f:
	f.write(img2pdf.convert(images, layout_fun=layout_fun))