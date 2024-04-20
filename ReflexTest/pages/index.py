"""The home page of the app."""

from ReflexTest import styles
from ReflexTest.templates import template
import pandas as pd

import reflex as rx
nba_data = pd.read_csv("https://media.geeksforgeeks.org/wp-content/uploads/nba.csv")

class ModalState(rx.State):
    show: bool = False

    def change(self):
        self.show = not (self.show)
    
    saved_username: str = rx.Cookie(
        name="", max_age=36000
    )

    def save_user_to_cookie(self, username: str):
        self.saved_username = username

    def get_saved_user(self):
        return self.saved_username
    


@template(route="/", title="Home")
def index() -> rx.Component:
    """The home page.

    Returns:
        The UI for the home page.
    """
    print("from index: ", ModalState.get_saved_user())
    return(
        rx.flex(
            rx.button(
                    "🏆",
                ),
            direction="column",
            align="end",
            justify="end",
            on_click=ModalState.change,
            #direction="row",
            height="100%",
            width="100%",
        ),
        rx.chakra.modal(
                rx.chakra.modal_overlay(
                    rx.chakra.modal_content(
                        rx.chakra.modal_header("Leaderboard"),
                        rx.chakra.modal_body(
                            rx.data_table(
                            data = nba_data[["Name", "Height", "Age"]],
                            pagination= True,
                            search= True,
                            sort= True,
                        ),
                        ),
                        rx.chakra.modal_footer(
                            rx.chakra.button(
                                "Close",
                                on_click=ModalState.change,
                            )
                        ),
                    )
                ),
                is_open=ModalState.show,
            ),
        rx.flex(
            rx.flex(
                rx.text("Hello World!"),
                padding_top="17em",
                align="center",
                justify="center",
                direction="row",
                height="100%",
            ),
            align="center",
            justify="center",
            direction="column",
            width="100%",
        ),
        rx.flex(
            rx.button(
                    "📷",
                ),
            direction="column",
            padding_top="5em",
            align="center",
            justify="center",
            on_click=rx.redirect(
            "http://localhost:3000/trashupload",
            external=False,),
            #direction="row",
            height="100%",
            width="100%",
        ),
        rx.chakra.accordion(
            items=[
                (rx.flex(
            rx.text(
                    "Collected Trash",
                ),
            direction="column",
            align="center",
            justify="center",
            #direction="row",
            height="100%",
            width="100%",
        ), rx.grid(
                    rx.foreach(
                        rx.Var.range(12),
                        lambda i: rx.card(f"Card {i + 1}", height="10vh"),
                    ),
                    columns="3",
                    spacing="4",
                    width="100%",
                ))
            ],
            padding_top="17em",
            width="100%",
            allow_toggle=True,
        )
    )

# @rx.page(route="/test", title="test")
# def test():
#     import ReflexTest.authentication.local_storage as ls
#     return ls.client_storage_example()
