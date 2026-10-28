import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPT_TEMPLATE_DIR = os.path.join(BASE_DIR, "prompt_template")


def load_prompt_template(file_name: str) -> str:
    with open(os.path.join(PROMPT_TEMPLATE_DIR, file_name), "r", encoding="utf-8") as f:
        return f.read()


def load_system_prompt() -> str:
    return load_prompt_template("system_prompt.txt")


def load_report_prompt() -> str:
    return load_prompt_template("report_prompt.txt")
