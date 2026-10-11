# main.py
import asyncio
import os
from dotenv import load_dotenv

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from src.agent.agent import StudyAgent

load_dotenv()


async def main():
    # 1. Cấu hình thông số khởi chạy MCP Server qua subprocess stdio
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "-m", "src.mcp.server"],
        env=os.environ.copy(),
    )

    print("=== T3 Learning Assistant Agent CLI ===")
    print("Đang kết nối tới MCP Server qua stdio...")

    # 2. Khởi tạo kết nối Stdio Client
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Khởi tạo session MCP
            await session.initialize()
            print("Đã kết nối thành công tới MCP Server!")

            # Khởi tạo StudyAgent với MCP Session
            agent = StudyAgent(mcp_session=session)

            print("\nHệ thống đã sẵn sàng. Nhập 'exit' hoặc 'quit' để thoát.\n")

            while True:
                try:
                    user_query = input("Sinh viên: ").strip()
                    if not user_query:
                        continue
                    if user_query.lower() in ("exit", "quit"):
                        print("Tạm biệt!")
                        break

                    print("\n[Agent đang xử lý...]")
                    response = await agent.ask(user_query)
                    print(f"\nAssistant: {response}\n")
                    print("-" * 50)

                except (KeyboardInterrupt, EOFError):
                    print("\nĐã hủy lệnh. Tạm biệt!")
                    break
                except Exception as exc:
                    print(f"\n[Lỗi hệ thống]: {exc}\n")


if __name__ == "__main__":
    asyncio.run(main())