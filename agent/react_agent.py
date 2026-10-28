from langchain.agents import create_agent
from langchain_core.messages import AIMessage

from agent.agent_tools import (
    fill_context_for_report,
    get_usage,
    location,
    month,
    rag_summary,
    user_id,
    weather,
)
from agent.middleware import log_before_model, monitor_tool, switch_to_report_mode
from model.factory import ChatModelFactory


class ReactAgent:
    def __init__(self) -> None:
        self.agent=create_agent(
            model= ChatModelFactory().generate_factory(),
            tools=[
                get_usage,
                fill_context_for_report,
                rag_summary,
                weather,
                location,
                user_id,
                month
            ],
            middleware=[monitor_tool, log_before_model, switch_to_report_mode],
        )

    def execute_stream(self, question: str):
        input_dict = {
            "messages": [
                {"role": "user", "content": question},
            ]
        }
        for message_chunk, metadata in self.agent.stream(
            input=input_dict,
            context={"report": False},
            stream_mode="messages",
        ):
            # 只输出 agent 模型节点的最终回答；工具内部模型的输出、工具结果和带工具调用的中间消息都会被过滤
            if (
                metadata.get("langgraph_node") == "model"
                and isinstance(message_chunk, AIMessage)
                and message_chunk.content
                and not message_chunk.tool_calls
            ):
                yield message_chunk.content


if __name__ == "__main__":
    TEST_QUESTIONS = [
        "滤芯多久更换一次？",
        "今天天气怎么样？",
        "帮我生成我 2026-10 月的使用报告",
    ]

    agent = ReactAgent()
    for question in TEST_QUESTIONS:
        print(f"\n{'=' * 30}\n用户：{question}")
        print("助手：", end="", flush=True)
        answer = ""
        for text in agent.execute_stream(question):
            answer += text
            print(text, end="", flush=True)
        print()
        assert answer.strip(), f"回答为空：{question}"
        