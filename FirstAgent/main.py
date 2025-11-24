import os
import re
from dotenv import load_dotenv

from src.llm import OpenAICompatibleClient
from src.prompt import AGENT_SYSTEM_PROMPT
from src.tools import available_tools

# Ensure secrets are loaded from .env instead of being hardcoded
load_dotenv()

# --- 1. Configure LLM client ---
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL_ID = os.getenv("MODEL_ID")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if TAVILY_API_KEY:
    # Tavily SDK reads from env by default
    os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY

llm = OpenAICompatibleClient(
    model=MODEL_ID,
    api_key=API_KEY,
    base_url=BASE_URL,
)


def run_agent(city: str) -> None:
    """Run one weather + attraction query loop for the given city."""
    user_prompt = f"你好，请帮我查询一下今天{city}的天气，然后根据天气推荐一个合适的旅游景点。"
    prompt_history = [f"用户请求: {user_prompt}"]

    print(f"\n用户输入: {user_prompt}\n" + "=" * 40)

    # Limit to avoid infinite loops
    for i in range(5):
        print(f"--- 循环 {i + 1} ---\n")

        # 3.1. Build prompt
        full_prompt = "\n".join(prompt_history)

        # 3.2. Call LLM
        llm_output = llm.generate(full_prompt, system_prompt=AGENT_SYSTEM_PROMPT)

        # The model may output extra Thought/Action pairs; keep only the first
        match = re.search(
            r"(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)",
            llm_output,
            re.DOTALL,
        )
        if match:
            truncated = match.group(1).strip()
            if truncated != llm_output.strip():
                llm_output = truncated
                print("已截断多余的 Thought-Action 段落。")
        print(f"模型输出:\n{llm_output}\n")
        prompt_history.append(llm_output)

        # 3.3. Parse and execute action
        action_match = re.search(r"Action: (.*)", llm_output, re.DOTALL)
        if not action_match:
            print("解析错误: 模型输出中未找到 Action。")
            break
        action_str = action_match.group(1).strip()

        if action_str.startswith("finish"):
            final_answer_match = re.search(r'finish\(answer="(.*)"\)', action_str)
            final_answer = final_answer_match.group(1) if final_answer_match else ""
            print(f"任务完成，最终答案: {final_answer}")
            break

        tool_name_match = re.search(r"(\w+)\(", action_str)
        args_match = re.search(r"\((.*)\)", action_str)
        if not tool_name_match or not args_match:
            print("解析错误: 无法提取工具或参数。")
            break
        tool_name = tool_name_match.group(1)
        args_str = args_match.group(1)
        kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_str))

        if tool_name in available_tools:
            observation = available_tools[tool_name](**kwargs)
        else:
            observation = f"错误: 未定义的工具 '{tool_name}'"

        # 3.4. Record observation
        observation_str = f"Observation: {observation}"
        print(f"{observation_str}\n" + "=" * 40)
        prompt_history.append(observation_str)


def main() -> None:
    while True:
        city = input("请输入要查询的城市（输入 exit 退出）：").strip()
        if not city:
            continue
        if city.lower() in {"exit", "quit"}:
            print("已退出。")
            break
        run_agent(city)


if __name__ == "__main__":
    main()
