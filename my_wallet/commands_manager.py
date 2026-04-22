import argparse
import importlib
import logging

from flask import Flask


logger = logging.getLogger(__name__)


def compose_command_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--command", action="store", default=None, help="Command to run"
    )
    return parser


def run_command(
    app: Flask,
    command_name: str,
    commands_module: str,
    callable_name: str = "run",
) -> None:
    command_importable_path = f"{commands_module}.{command_name}"
    logger.info(f"Running command {command_name} from module {command_importable_path}")
    try:
        command_module = importlib.import_module(command_importable_path)
    except ModuleNotFoundError:
        logger.error(f"Module {command_importable_path} not found")
        return
    try:
        command_callable = getattr(command_module, callable_name)
    except AttributeError:
        logger.error(
            f"Module {command_importable_path} has no attribute {callable_name}"
        )
        return

    with app.app_context():
        command_callable(app=app)
