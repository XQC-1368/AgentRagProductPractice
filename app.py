import streamlit as st  # 导入 Streamlit 库,用于构建聊天式 Web 界面

from agent.react_agent import ReactAgent  # 导入 ReactAgent,封装大模型与工具调用的对话逻辑

SIDEBAR_QUESTIONS = [  # 侧边栏默认展示的推荐问题列表
    "滤芯多久更换一次？",  # 推荐问题:滤芯更换周期
    "扫地机器人吸力变小了怎么办？",  # 推荐问题:吸力变小的处理方式
    "帮我生成我 2026-10 月的使用报告",  # 推荐问题:生成使用报告(会触发工具调用)
]

QUESTION_POOL = [  # 备用问题池,侧边栏问题被点掉后从中补位
    "扫地机器人适合在什么环境下使用？",  # 备用问题:适用使用环境
    "电池怎么保养？",  # 备用问题:电池保养方法
    "机器人在工作中突然停止怎么办？",  # 备用问题:工作中突然停机
    "边刷多久需要更换一次？",  # 备用问题:边刷更换周期
]


def init_session_state():  # 初始化 Streamlit 会话状态
    if "messages" not in st.session_state:  # 若聊天记录尚未创建
        st.session_state.messages = []  # 创建空的聊天记录列表
    if "agent" not in st.session_state:  # 若智能体实例尚未创建
        st.session_state.agent = ReactAgent()  # 创建 ReactAgent 并缓存在会话中
    if "sidebar_questions" not in st.session_state:  # 若侧边栏问题尚未初始化
        st.session_state.sidebar_questions = SIDEBAR_QUESTIONS.copy()  # 用默认问题列表的浅拷贝初始化
    if "question_pool" not in st.session_state:  # 若备用问题池尚未初始化
        st.session_state.question_pool = QUESTION_POOL.copy()  # 用备用问题池的浅拷贝初始化


def replace_sidebar_question(question: str):  # 把侧边栏中刚被点击的问题替换成新问题
    st.session_state.sidebar_questions.remove(question)  # 从侧边栏移除被点击的问题
    if st.session_state.question_pool:  # 若备用问题池还剩余问题
        st.session_state.sidebar_questions.append(st.session_state.question_pool.pop(0))  # 取出池中第一个问题补到侧边栏


def with_sidebar():  # 渲染侧边栏区域
    with st.sidebar:  # 进入侧边栏上下文
        st.header("可能想问的问题")  # 显示侧边栏标题
        for question in st.session_state.sidebar_questions:  # 遍历所有侧边栏问题
            if st.button(question, key=f"sidebar-question-{question}", width="stretch"):  # 每题渲染为按钮并铺满宽度,点击返回 True
                st.session_state.pending_question = {  # 记录本次点击待处理的问题
                    "question": question,  # 问题文本
                    "source": "sidebar",  # 来源标记为侧边栏
                }


def handle_user_input(question: str, source: str):  # 统一处理用户提问并流式展示回答
    if source == "sidebar":  # 若问题来自侧边栏按钮
        replace_sidebar_question(question)  # 用备用问题替换被点掉的侧边栏问题

    st.session_state.messages.append({"role": "user", "content": question})  # 把用户消息追加进聊天记录
    with st.chat_message("user"):  # 进入用户消息气泡
        st.markdown(question)  # 显示用户问题

    answer = ""  # 累积流式返回的答案文本
    with st.chat_message("assistant"):  # 进入助手消息气泡
        placeholder = st.empty()  # 创建占位符,用于实时刷新答案
        for chunk in st.session_state.agent.execute_stream(question):  # 逐块读取智能体的流式输出
            answer += chunk  # 拼接当前片段
            placeholder.markdown(answer)  # 用累计文本刷新显示
    st.session_state.messages.append({"role": "assistant", "content": answer})  # 把完整答案追加进聊天记录


def main():  # 应用入口
    st.set_page_config(page_title="扫地机器人智能客服", layout="centered")  # 设置页面标题与居中布局
    init_session_state()  # 初始化会话状态

    st.title("扫地机器人智能客服")  # 显示页面主标题
    with_sidebar()  # 渲染侧边栏

    for message in st.session_state.messages:  # 重放历史聊天记录
        with st.chat_message(message["role"]):  # 按消息角色显示对应气泡
            st.markdown(message["content"])  # 显示消息内容
    #输入来源：侧边栏
    pending_question = st.session_state.pop("pending_question", None)  # 取出并清空待处理的侧边栏问题
    if pending_question:  # 若存在待处理问题
        handle_user_input(pending_question["question"], pending_question["source"])  # 处理该问题
        st.rerun()  # 重跑脚本刷新界面
    #输入来源：用户输入
    prompt = st.chat_input("请输入您的问题")  # 底部聊天输入框,提交后返回输入文本
    if prompt:  # 若用户提交了输入
        handle_user_input(prompt, "user_input")  # 按普通用户输入处理


if __name__ == "__main__":  # 仅当脚本被直接运行时
    main()  # 启动应用
