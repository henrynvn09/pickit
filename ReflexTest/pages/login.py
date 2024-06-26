from ReflexTest.templates import template
import reflex as rx
import ReflexTest.CRUD.user_db as userDB
from ReflexTest.classes.user import User
import ReflexTest.components.db_connection as db

mydb = db.get_db_instance()


class LoginState(rx.State):
    """Handle login form submission and redirect to proper routes after authentication."""

    error_message: str = ""
    redirect_to: str = ""

    saved_username: str = rx.Cookie(
        name="username_pickit", max_age=36000
    )

    def logout(self):
        self.saved_username = ""
    
    def save_user_to_cookie(self, username: str):
        self.saved_username = username
        # print("saved user to cookie", self.saved_username)
        
    def get_saved_user(self):
        return self.saved_username

    def isAuthenticated(self):
        return self.saved_username != ""
        

    def on_submit(self, form_data) -> None:
        """Handle form submission."""
        username = form_data["username"]
        password = form_data["password"]

        if username == "" or password == "":
            self.error_message = "Please fill in all fields."
            return

        user: User = userDB.get_user(mydb, username, password)

        if not user:
            self.error_message = "User is not exists."
        else:
            self.save_user_to_cookie(username)
            print("saved user to cookie", self.saved_username)
            return rx.redirect("/")
        
    
    def redir(self):
        """redirect to the login page if not logged in"""
        if not self.is_hydrated:
            return LoginState.redir()

        page = self.router.page.path
        if page == "/login" and self.isAuthenticated():
            return rx.redirect("/")
    

@template(route="/login", title="Login")
def login() -> rx.Component:
    """Render the login page.

    Returns:
        A reflex component.
    """

    rx.center(rx.text("Pickit"),
              position="fixed",
              top="0px",
            )

    login_form = rx.center(
        rx.vstack(
            rx.form(
                rx.fragment(
                    rx.center(rx.image(src="/pickit_logo.png", width="120px",
                                       height="auto", align="center", padding_bottom="1rem"
                                       , padding_top="1rem")
                              ),
                    rx.heading(
                        "Account Login", size="7", margin_bottom="2rem", align="center"
                    ),
                    rx.input(
                        placeholder="username",
                        id="username",
                        border_color="hsl(240,3.7%,15.9%)",
                        justify_content="center",
                    ),
                    rx.container(
                        height="5px"
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
                            "Sign in",
                            type="submit",
                            width="100%",
                        ),
                        padding_top="14px",
                    ),
                    rx.container(height="5px"),
                    rx.center(rx.link("Sign Up", href="/signup"), width="100%", justify_content="center")
                    ,
                ),
                on_submit=LoginState.on_submit,
            ),
            # rx.link("Register", href=REGISTER_ROUTE),
            align_items="center",
            overflow="hidden"
        ),
        padding="20px 25px",
        border="1px solid gray",
        border_color="gray.300",
        border_radius=10,
        align_items="center",
        box_shadow="3px 3px 5px #222",
        overflow="hidden"
    )

    return rx.cond( 
        LoginState.is_hydrated,
        rx.center(
            rx.cond(
                LoginState.is_hydrated,  # type: ignore
                login_form
            ),
            width="100%",
            height="70vh",
            align_items="center",
            justify_content="center",
            align="center",
            overflow="hidden"
        ),
        rx.center(
            rx.chakra.spinner(on_mount=LoginState.redir),
        ),
        )

