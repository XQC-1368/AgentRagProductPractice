from langchain.agents.middleware import ModelRequest, before_model, dynamic_prompt, wrap_tool_call

from utils.prompt_loader import load_report_prompt, load_system_prompt


@dynamic_prompt
def switch_to_report_mode(request: ModelRequest) -> str:
    if request.runtime.context.get("report", False):
        return load_report_prompt()

    return load_system_prompt()



@wrap_tool_call
def monitor_tool(request,handler):
    if request.tool_call["name"] == "fill_context_for_report":
        request.runtime.context["report"] = True   
    return handler(request)


@before_model
def log_before_model(state, runtime):
    pass