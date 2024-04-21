"""The Trash Upload page."""

from ReflexTest.templates import template
import google.generativeai as genai
import reflex as rx
import os
import PIL.Image
from PIL import Image
import io
import pymongo
from pymongo import MongoClient

try:
    api_key = os.environ["API_KEY"]
except KeyError:
    # Handle the case where API_KEY is not set
    print("API_KEY is not set!")
    api_key = None  # Or any default value or action you prefer

genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel('gemini-pro-vision')
text_model = genai.GenerativeModel('gemini-pro')

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["Users"]
# mydict = {"f_name": "ryan", "l_name": "perez", "user_ID": "123", "password": "123",
#           "points": "", "img_list": []}
# x = mycol.insert_one(mydict)


class TrashUploadState(rx.State):
    """The app state."""

    # The images to show.
    img: list[str] = []
    data: str = ""
    score: str = ""
    error_msg: bool = True
    
    def clear_state(self):
        self.img = []
        self.data = ""
        self.score = ""
        self.error_msg = False

    def add_points(self, total_points, new_points):
        try:
            points = int(total_points)
            new_points = int(new_points)
            points = + new_points
            return points
        except ValueError:
            print("ValueError: invalid literal for int() with base 10: 'what'")
            return total_points

    def get_user_points(self, user):
        if user:
            # Extract points and assign to a variable
            return user["points"]
        else:
            return 0

    # def add_image_to_DB(self, image):
    #     client = MongoClient()
    #     db = client.testdb
    #     images = db.images
    #
    #     im = Image.open(image)
    #
    #     image_bytes = io.BytesIO()
    #     im.save(image_bytes, format='JPEG')
    #
    #     image = {
    #         'data': image_bytes.getvalue()
    #     }
    #     return image
    async def handle_save(self):
        self.handle_clear(None)
        return rx.redirect(
            "/",
            )
    
    async def handle_back(self):
        self.handle_clear(None)
        return rx.redirect(
            "/",
            )


    async def handle_upload(self, files: list[rx.UploadFile]=[]):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        if len(files) < 1: 
            self.error_msg = True
            print("caught")
            return None
        else: 
            self.error_msg = False

        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename

            # Save the file.
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)
            img = PIL.Image.open(io.BytesIO(upload_data))
            response = model.generate_content(img)
            self.data = self.data.replace(self.data, response.text)
            text_response = text_model.generate_content([
                "Give a number between 1-10 that accurately represents the quantity "
                "at which the environment will improve if removed from the hiking trail it was found in. "
                "10 being the best score. "
                "Give Score based on how long it would take for the item to decompose,"
                "and how toxic is to its environment. For example a biodegradable spoon is a 1, "
                "while a plastic six pack rigs are a 10. If there are multiple items, "
                "do an arthimetic sum of the indivivual scores of the items. Only give me a number.",
                self.data], stream=True)
            text_response.resolve()
            self.score = self.score.replace(self.score, text_response.text)
            # image_bytes = io.BytesIO()
            # img.save(image_bytes, format='JPEG')
            # image = {
            #           'data': img.getvalue()
            #         }
            # mycol.update_one({"user_ID": "123"}, {"$push": {"img_list": image}})
            #
            # user = mycol.find_one({"user_ID": "123"})
            # points = self.get_user_points(user)
            # mycol.update_one({"user_ID": "123"}, {"$set": {"points": self.add_points(points, self.score)}})
            # Update the img var.
            self.img.append(file.filename)

    def handle_clear(self, clearHandle):
        self.img = []
        self.data = ""
        self.score = ""
        self.error_msg = True
        return None

color = "rgb(107,99,246)"



@template(route="/trashupload", title="Trash Upload")
def trashupload() -> rx.Component:
    """The Trash Upload page.

    Returns:
        The UI for the Trash Upload page.
    """
    rx.redirect("/current-page")
    return rx.vstack(
        rx.heading("Trash Upload"),
        rx.text(
            "Upload your trash here to earn some more points!",
            font_weight="bold",
            font_size="1em",
            ),
        rx.upload(
            rx.vstack(
                rx.button("Select File", color=color, bg="white", border=f"1px solid {color}"),
            ),
            id="upload1",
            border=f"1px dotted {color}",
            border_radius= "5px",
            padding="4em",
        ),
        rx.hstack(rx.foreach(rx.selected_files("upload1"), rx.text)),
        rx.cond(
            TrashUploadState.error_msg,
            rx.callout(
                "Please upload an image.",
                icon="alert_triangle",
                color_scheme="red",
                role="alert",
            ),
        ),
        rx.flex(
            rx.cond(
                not rx.upload_files(upload_id="upload1"),
                rx.button(
                "Upload",
                disabled=True,
                ),
                rx.button(
                "Upload",
                on_click=TrashUploadState.handle_upload(rx.upload_files(upload_id="upload1")),
                )
            ),
            rx.button(
                "Clear",
                on_click=TrashUploadState.handle_clear(rx.clear_selected_files("upload1")),
            ),
            spacing="2"
        ),
        
        rx.foreach(TrashUploadState.img, lambda img: rx.image(src=rx.get_upload_url(img))),
        rx.text(TrashUploadState.data),
        rx.text(TrashUploadState.score),
        rx.flex(
            rx.button(
                "Back",
                on_click=TrashUploadState.handle_back(),
            ),
            rx.cond(TrashUploadState.error_msg,        
            rx.button(
                "Save",
                on_click=TrashUploadState.handle_save(),
                disabled=True,
            ),
            rx.button(
                "Save",
                on_click=TrashUploadState.handle_save(),
            ),
            ),
            spacing="2"
        ),
        
        padding="4em",
    )

