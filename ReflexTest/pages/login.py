from ReflexTest.templates import template
import reflex as rx
import ReflexTest.CRUD.user_db as db


class LoginState(rx.State):
    """Handle login form submission and redirect to proper routes after authentication."""

    error_message: str = ""
    redirect_to: str = ""


@template(route="/login", title="login")
def login() -> rx.Component:
    """Render the login page.

    Returns:
        A reflex component.
    """

    login_form = rx.box(
        rx.vstack(
            rx.form(
                rx.fragment(
                    rx.heading(
                        "Login into your Account", size="7", margin_bottom="2rem"
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
                            "Sign in",
                            type="submit",
                            width="100%",
                        ),
                        padding_top="14px",
                    ),
                ),
                # on_submit=LoginState.on_submit,
            ),
            # rx.link("Register", href=REGISTER_ROUTE),
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
            LoginState.is_hydrated,  # type: ignore
            rx.vstack(
                rx.cond(  # conditionally show error messages
                    LoginState.error_message != "",
                    rx.callout(
                        rx.text("This is an error"),
                        # LoginState.error_message,
                        icon="triangle_alert",
                        color_scheme="red",
                        role="alert",
                    ),
                ),
                login_form,
                padding_top="10vh",
            ),
        )
    )
