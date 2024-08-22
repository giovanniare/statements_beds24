from code_updates.git_process import GitHandler
from code_updates.cmd_line_args import CmdLineArgs


if __name__ == "__main__":
    cmd_line = CmdLineArgs()
    cmd_line.initialize()
    cmd_line.build()

    args = cmd_line.args
    if not args.dev:
        git = GitHandler()
        git.checkout_all()
        branch = args.branch
        if branch:
            git.switch_to_brach(branch)
        else:
            git.set_main()

        git.pull()

    # run application
    from app import App
    app = App()
    app.run()

