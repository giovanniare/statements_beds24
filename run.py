from code_updates.git_process import GitHandler 


if __name__ == "__main__":
    git = GitHandler()
    git.checkout_all()
    git.pull()

    # run application
    from app import App
    app = App()
    app.run()

