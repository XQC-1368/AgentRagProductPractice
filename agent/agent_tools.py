import os
import random

from langchain_core.tools import tool

from rag.rag_service import RagSummaryService

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECORDS_PATH = os.path.join(BASE_DIR, "usage_data", "records.csv")

rag_service = RagSummaryService()

@tool(description="从向量库检索返回资料, 输入str, 输出str")
def rag_summary(question: str) -> str:
    return rag_service.get_summary(question)
    
    
@tool(description="获取天气信息") 
def weather(city: str) -> str:
    if city == "深圳":
        return "晴天"
    if city == "上海":
        return "阴天"
    if city == "北京":
        return "雨天"
    if city == "广州":
        return "雷阵雨"
    if city == "西安":
        return "雪天"
    if city == "武汉":
        return "冰雹"
    if city == "成都":
        return "雾天"
    if city == "南京":
        return "小雨"
    if city == "杭州":
        return "中雨"
    if city == "苏州":
        return "大雨"
    if city == "厦门":
        return "台风天"
    if city == "郑州":
        return "阴转小雨"
    if city == "长沙":
        return "小雨转晴"
    return "未知天气"

@tool(description="获取用户位置") 
def location() -> str:
    return random.choice(["深圳", "上海", "北京", "广州", "西安", "武汉", "成都", "南京", "杭州", "苏州", "厦门", "郑州", "长沙"])

@tool(description="获取用户id") 
def user_id() -> str:
    return "1001"

@tool(description="获取当前月份")
def month() -> str:
    month = random.randint(1, 12)
    return f"2026-{month:02d}"

@tool(description="从外部系统中获取指定用户在指定月份的使用记录,以纯字符串形式返回,没有记录返回空串,输入target_user_id(str类型,参数1)和month(str类型,参数2,如2026-01格式)")
def get_usage(target_user_id: str, month: str) -> str:
    usage_record = ""
    if os.path.exists(RECORDS_PATH):#路径下该文件存在
        with open(RECORDS_PATH, "r", encoding="utf-8") as f:
            for line in f.readlines()[1:]:
                user_id,feature,efficiency,consumables,comparison,time = line.strip().replace("\"", "").split(",")
                if user_id == target_user_id and month == time:
                    usage_record+=f"用户{user_id}在{time}被使用。清洁情况：{feature}，耗电性能：{efficiency}，消耗磨损数据：{consumables}，对比数据：{comparison}\n"
    return usage_record
        
    
@tool(description="无入参，无返回值，调用后触发中间件自动为报告生成的场景动态注入上下文信息，为后续提示词切换提供上下文信息")  
def fill_context_for_report():
    return "启用报告模板"