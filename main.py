from my_wallet.app import compose_app
from my_wallet.commands_manager import compose_command_argparser, run_command

if __name__ == "__main__":
    app = compose_app()
    args = compose_command_argparser().parse_args()
    if args.command:
        run_command(
            app,
            args.command,
            commands_module="my_wallet.commands",
        )
    else:
        app.run(debug=True)
