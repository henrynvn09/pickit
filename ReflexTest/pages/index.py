"""The home page of the app."""

from ReflexTest import styles
from ReflexTest.templates import template
import pandas as pd
import ReflexTest.CRUD.user_db as user_db
from ReflexTest.components.db_connection import get_db_instance
from ReflexTest.classes.user import User

import reflex as rx
nba_data = pd.read_csv("https://raw.githubusercontent.com/elliotfayman/Pickit/main/assets/rank.csv")

mydb = get_db_instance()

class ModalState(rx.State):
    show: bool = False

    saved_username: str = rx.Cookie(
        name="username_pickit", max_age=36000
    )

    def hide_modal(self):
        self.show = False
    def show_modal(self):
        self.show = True
    
    def logout(self):
        self.saved_username = ""
        return rx.redirect("/login")
    
    def save_user_to_cookie(self, username: str):
        self.saved_username = username
        # print("saved user to cookie", self.saved_username)

    def get_saved_user(self):
        return self.saved_username

    def isAuthenticated(self):
        return self.saved_username != ""
        
    def redir(self):
        """redirect to the login page if not logged in"""
        if not self.is_hydrated:
            return ModalState.redir()

        page = self.router.page.path
        if not self.isAuthenticated() and page != "/login":
            return rx.redirect("/login")


class UserState(ModalState):
    username: str = ""
    password: str = ""
    avatar: str = "default_avatar.png"
    points: int = 0
    trash_logs: list[dict] = [{"name": "plastic", "point": 0, "img": ""}]

    def fetch_user(self):
        if self.get_saved_user() == "":
            return
        # user = user_db.get_user_without_password(mydb, "username1")
        user:User = user_db.get_user_without_password(mydb, self.get_saved_user())
        self.username = user.username
        self.password = user.password
        self.avatar = user.avatar
        self.points = user.points
        self.trash_logs = user.trash_logs

color = "rgb(107,99,246)"
@template(route="/", title="Home")
def index() -> rx.Component:
    """The home page.

    Returns:
        The UI for the home page.
    """
    top_bar = rx.hstack(
                rx.button(
                    "", rx.icon(tag="arrow-left-from-line"), color="black"
                    , border=f"1px solid gray", 
                    background_color="#FDF8FA", border_radius="10%",
                    margin_right="1.5rem"
                    ,on_click=ModalState.logout
                ),

                rx.image(src="/pickit_logo.png", width="125px",
                         height="auto", align="center", padding_bottom="1rem",
                         margin_x="9%"
                         , padding_top="10%"),
                
                rx.flex(
                    rx.button(
                            "Rank 🏆",
                            on_mount=UserState.fetch_user,
                            background_color="#8693a3",
                        ),
                    on_click=ModalState.show_modal,
                    height="100%",
                    width="100%",
                ),
                rx.chakra.modal(
                        rx.chakra.modal_overlay(
                            rx.chakra.modal_content(
                                rx.chakra.modal_header("Leaderboard"),
                                rx.chakra.modal_body(
                                    rx.data_table(
                                    data = nba_data[["Rank", "Username", "Points"]],
                                    pagination= True,
                                    search= True,
                                    sort= True,
                                ),
                                ),
                                rx.chakra.modal_footer(
                                    rx.chakra.button(
                                        "Close",
                                        on_click=ModalState.hide_modal,
                                    )
                                ),
                            ),
                        ),
                        on_click=ModalState.hide_modal,
                        is_open=ModalState.show,
                    ),
                position="fixed", top=0, padding_top="1.04rem",
                width="100%", justify="between", background_color="#FDF8FA")
            

    return rx.cond(
        ModalState.is_hydrated,
        rx.vstack(
            top_bar,
            rx.container(rx.image(src="/lahacksdino.png" , width="120px", border_radius="50%",
                                  height="auto", align="center"), margin_top="4rem", margin_left="7rem", padding="5px", 
                                  background="black", align="center", border_radius="50%",
                                    box_shadow="0.8px 0.8px 3px #222")
            ,
            rx.center(
                    rx.text(UserState.points, font_size="6rem", color="black", text_shadow="0.8px 0.8px 2px #222"
                    ), margin_top="2rem", margin="auto"
            ),
            rx.button(
                        "Share your findings! 📷",
                        
                padding="30px",
                align="center",
                justify="center",
                font_size="1.4rem",
                margin_top="2rem",
                background_color="#185c1c",
                margin_x="auto",
                margin_bottom="2rem",

                on_click=rx.redirect(
                "/trashupload",
                external=False,)
            ),
             rx.grid(
                        rx.foreach(
                            UserState.trash_logs,
                            lambda i: rx.card(rx.flex(
                                rx.avatar(src=rx.get_upload_url(i["img"]), width="100%",height="10vh"),
                                rx.text(i["point"], "pts - ", i["name"], font_size="1.2rem"),
                                direction="column"
                            )
                        , height="15vh"),
                        ),
                        columns="2",
                        spacing="4",
                        width="100%",
                    )
        
        ),
     rx.center(
         rx.chakra.spinner(on_mount=ModalState.redir)
     )
    )

# @rx.page(route="/test", title="test")
# def test():
#     import ReflexTest.authentication.local_storage as ls
#     return ls.client_storage_example()
