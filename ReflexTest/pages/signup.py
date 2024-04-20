from ReflexTest.templates import template
import reflex as rx
import ReflexTest.CRUD.user_db as userDB
from ReflexTest.components.db_connection import get_db_instance

mydb = get_db_instance()

class SignUpState(rx.State):
    """Handle login form submission and redirect to proper routes after authentication."""

    error_message: str = ""
    redirect_to: str = ""

    def on_submit(self, form_data) -> None:
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
                return rx.redirect("/login")
            else:
                self.error_message = "please try again the connection"

                
        

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
            rx.cond(  # conditionally show error messages
                    SignUpState.error_message != "",
                    rx.callout(
                        rx.text(SignUpState.error_message),
                        # LoginState.error_message,
                        icon="triangle_alert",
                        color_scheme="red",
                        role="alert",
                    ),
                ),
            
            rx.center(rx.link("Login", href="/login"), width="100%", justify_content="center")
        ),
        padding="20px 25px",
        border="1px solid gray",
        border_color="gray.300",
        border_radius=10,
        align_items="center",
        box_shadow= "3px 3px 5px #222"
    )

    return rx.center(
        rx.cond(
            SignUpState.is_hydrated,  # type: ignore
            signup_form
        ),
        width="100%",
        height="70vh",
        align_items="center",
        justify_content="center",
        align="center",
        overflow="hidden"
    )
