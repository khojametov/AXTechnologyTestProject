#!/usr/bin/env python
import typer
import uvicorn
from sqlmodel import Session

from auth.services import create_admin_user
from config.db import engine

cli = typer.Typer()


@cli.command("runserver")
def _runserver(
    host: str = typer.Option("0.0.0.0"), port: int = typer.Option(8000)
) -> None:
    """
    Run development server
    """

    uvicorn.run("config.asgi:app", reload=True, host=host, port=port)


@cli.command("create_admin")
def _create_admin(
    email: str = typer.Option(default=str, prompt="email", help="email"),
    password: str = typer.Option(
        default=str,
        confirmation_prompt=True,
        hide_input=True,
        prompt="password",
        help="password",
    ),
):
    """
    Create admin user
    """

    with Session(engine) as session:
        try:
            create_admin_user(session, email=email, password=password)
        except Exception as e:
            typer.secho(str(e), fg="red")
        else:
            typer.secho("User created successfully", fg="green")


if __name__ == "__main__":
    cli()
