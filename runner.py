import streamlit.web.bootstrap as bootstrap
import os

os.environ["AUTOGEN_USE_DOCKER"] = "no"


if __name__ == "__main__":
    bootstrap.run("main.py", flag_options={}, is_hello=False, args=[])
