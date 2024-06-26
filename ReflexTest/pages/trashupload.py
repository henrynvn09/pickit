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
import json

from ReflexTest.components.db_connection import get_db_instance
import ReflexTest.CRUD.user_db as userDB 
from .index import UserState



try:
    api_key = os.environ["API_KEY"]
except KeyError:
    # Handle the case where API_KEY is not set
    print("API_KEY is not set!")
    api_key = None  # Or any default value or action you prefer

genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel('gemini-pro-vision')
text_model = genai.GenerativeModel('gemini-pro')

mydb = get_db_instance()
# mydict = {"f_name": "ryan", "l_name": "perez", "user_ID": "123", "password": "123",
#           "points": "", "img_list": []}
# x = mycol.insert_one(mydict)


class TrashUploadState(rx.State):
    """The app state."""
    set_rating_text = False
    # The images to show.
    img: list[str] = []
    data: str = ""
    score: str = ""
    name: str = ""
    description = ""
    error_msg: bool = True
    saved_username: str = rx.Cookie(
        name="username_pickit", max_age=36000
    )
    
    def clear_state(self):
        self.img = []
        self.data = ""
        self.score = ""
        self.description = ""
        self.name = ""
        self.error_msg = False
        self.set_rating_text = False


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
        userDB.add_a_trash(mydb, self.saved_username, int(self.score), self.name, self.img[0])

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
            # response = model.generate_content(["""Make sure to cover the important details of the
            # the subject in focus, but describe it in as few words as possible.""",img], stream=True)
            # response.resolve()
            # self.data = self.data.replace(self.data, response.text)
            # text_response = text_model.generate_content([
            #     "Give a number between 1-10 that accurately represents the quantity "
            #     "at which the environment will improve if removed from the hiking trail it was found in. "
            #     "10 being the best score. "
            #     "Give Score based on how long it would take for the item to decompose,"
            #     "and how toxic is to its environment. For example a biodegradable spoon is a 1, "
            #     "while a plastic six pack rigs are a 10. If there are multiple items, "
            #     "do an arthimetic sum of the indivivual scores of the items. Only give me a number.",
            #     self.data], stream=True)
            # text_response.resolve()
            text_response = model.generate_content([img,
                """please set the random seed = 393948394 so that all answers will be consistent
                help me make a scale to grade the impact of the trash to the environment. Highest is worst with requirements below.
                Q1. tell me the name of the trash
                Q2: Give a number between 1-15 that accurately represents the quantity at which the environment will improve if removed from the hiking trail it was found in. 20 being the best score. Score based on Carbon Footprint, Recycling Rate, and Toxicity. Each of them has score ranging from 0 to 5. give me the answer in number for each scale only.

                answer in term of a JSON, for example
                {
                    "name": "plastic bags",
                    "description": "describe below 20 words about its impact on the environment",
                    "data": "3 (Carbon Footprint) + 2 (Recycling Rate) + 4 (Toxicity)",
                    "total": "9"
                }
                """,
                self.data], stream=True)
            text_response.resolve()

            response = text_response.text[8:-3]
            response_obj = json.loads(response)

            self.data = self.data.replace(self.data, response_obj["data"])
            self.name = self.name.replace(self.name, response_obj["name"])
            self.description = self.description.replace(self.description, response_obj["description"])
            self.score = self.score.replace(self.score, response_obj["total"])
            self.set_rating_text = True
            # self.score = self.score.replace(self.score, text_response.text)
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
        self.description = ""
        self.set_rating_text= False
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
            align="center"
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
                icon="camera",
                color_scheme="grass",
                role="alert",
            ),

        ),
        rx.flex(
            rx.cond(
                not rx.upload_files(upload_id="upload1"),
                rx.button(
                "Scan",
                disabled=True,
                padding_x="1.5rem",
                ),
                rx.button(
                "Scan",

                padding_x="1.5rem",
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
        rx.text(TrashUploadState.description),
        rx.text(TrashUploadState.data),
        rx.cond(TrashUploadState.set_rating_text,
                rx.text("This piece is worth " + TrashUploadState.score + " points!"),),
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
        
        padding="4em", align="center"
    )

