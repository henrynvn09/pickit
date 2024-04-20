from ReflexTest.templates import template
import reflex as rx
import ReflexTest.CRUD.user_db as userDB
from ReflexTest.components.db_connection import get_db_instance

mydb = get_db_instance()

class SignUpState(rx.State):
    """Handle login form submission and redirect to proper routes after authentication."""

    error_message: str = ""
    redirect_to: str = ""

    async def on_submit(self, form_data) -> None:
        """Handle form submission."""
        
        username = form_data["username"]
        password = form_data["password"]
        
        if username == "" or password == "":
            self.error_message = "Please fill in all fields."
            return
        
        user = userDB.get_user(mydb, username, password)
        
        if user:
            self.error_message = "User already exists."
        else:
            if userDB.add_user(mydb, username, password):
                print("User added")
                rx.redirect("/login")
                
                
        

@template(route="/signup", title="Sign Up")
def signup() -> rx.Component:

    signup_form = rx.box(
        rx.vstack(
            rx.form(
                rx.fragment(
                    rx.heading(
                        "Create an Account", size="7", margin_bottom="2rem"
                    ),
                    rx.input(
                        placeholder="username",
                        id="username",
                        border_color="hsl(240,3.7%,15.9%)",
                        justify_content="center",
                    ),
                    rx.input(
                        placeholder="password",
                        id="password",
                        border_color="hsl(240,3.7%,15.9%)",
                        justify_content="center",
                        type="password",
                    ),
                    rx.box(
                        rx.button(
                            "Sign Up",
                            type="submit",
                            width="100%",
                        ),
                        padding_top="14px",
                    ),
                ),
                on_submit=SignUpState.on_submit,
            ),
            rx.link("Register", href="/login"),
            align_items="center"
        ),
        padding="8rem 10rem",
        margin_top="10vh",
        margin_x="auto",
        border="2px solid black",
        border_color="gray.300",
        border_radius=10,
    )

    return rx.fragment(
        rx.cond(
            SignUpState.is_hydrated,  # type: ignore
            rx.vstack(
                rx.cond(  # conditionally show error messages
                    SignUpState.error_message != "",
                    rx.callout(
                        rx.text("This is an error"),
                        # LoginState.error_message,
                        icon="triangle_alert",
                        color_scheme="red",
                        role="alert",
                    ),
                ),
                signup_form,
                padding_top="10vh",
            ),
        )
    )