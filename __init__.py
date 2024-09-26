import os
import google.generativeai as genai
from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from nonebot.rule import to_me
from nonebot.plugin import PluginMetadata
# 设置 Google Generative AI 的 API Key
# XXXXXXXXXXXXXXXXXXXXXXXXXXX 修改为你的 API Key
os.environ['API_KEY'] = 'XXXXXXXXXXXXXXXXXXXXXXXXX'
genai.configure(api_key=os.environ['API_KEY'])

# 插件的基本信息
# __zx_plugin_name__ = "GoogleAI"
# __plugin_usage__ = """
# usage：
#     GoogleAI
#     指令：
#        @机器人 你的问题
# """.strip()
# __plugin_des__ = "使用 Google Generative AI 的 Nonebot 插件"
# __plugin_cmd__ = ["@机器人"]
# __plugin_version__ = 0.1
# __plugin_author__ = 'Shouzi'
# __plugin_settings__ = {
#     "level": 5,
#     "default_status": True,
#     "limit_superuser": False,
#     "cmd": ["@机器人"],
# }


__plugin_meta__ = PluginMetadata(
    name="Google_Gemini_AI",
    description="使用 Google Generative AI 的 Nonebot 插件",
    usage="""
    @机器人 你的问题
    示例: @机器人 你的问题
    """.strip(),
    extra=PluginExtraData(
        author="shouzi",
        version="0.1",
        # configs=[
        #     RegisterConfig(
        #         key="WITHDRAW_COS_MESSAGE",
        #         value=(0, 1),
        #         help="自动撤回，参1：延迟撤回色图时间(秒)，0 为关闭 | 参2：监控聊天类型，0(私聊) 1(群聊) 2(群聊+私聊)",
        #         default_value=(0, 1),
        #         type=Tuple[int, int],
        #     ),
        # ],
    ).dict(),
)

# 初始化消息处理器，优先级设为100
google_ai = on_message(rule=to_me(), priority=100)

@google_ai.handle()
async def handle_message(bot: Bot, event: MessageEvent):
    user_input = str(event.message).strip()  # 获取并去除消息的首尾空格
    if not user_input:
        return

    # 调用 Google Generative AI 生成内容
    answer = generate_content(user_input)
    await google_ai.finish(answer)

def generate_content(prompt):
    # 初始化模型
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 生成内容
    response = model.generate_content(prompt+",并使用中文回答我!")
    
    # 返回生成的文本内容
    return response.text