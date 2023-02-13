from urllib.parse import urlparse
import requests
import markdown

import cloudinary.uploader

from utils.generic_errors import SlideRequestError, UploadSlidesError


class SlideCommonComponents:
    def get_slide_content(slide_url):
        parsed_url = urlparse(slide_url)
        if not parsed_url.scheme and not parsed_url.netloc:
            raise SlideRequestError(f"{slide_url} isn't a valid link", 500)

        slide_request = requests.get(slide_url)

        if slide_request.status_code != 200:
            raise SlideRequestError(
                f"Failed to retrieve slide content from URL: {slide_url}", 500)

        slide_md_content = slide_request.text
        html_form = markdown.markdown(slide_md_content)
        return html_form

    def upload_files(slide_file):
        upload_data = cloudinary.uploader.upload(
            slide_file, resource_type="auto")

        if upload_data is None:
            raise UploadSlidesError("File upload filed", 500)

        return upload_data.get('url')

