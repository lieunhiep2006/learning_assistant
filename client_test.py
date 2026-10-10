
import asyncio
import os
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    # Khai báo cách chạy MCP Server
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["src/mcp/server.py"],
        env=os.environ.copy(),
    )

    # Mở kết nối stdio giữa client và server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Khởi tạo phiên MCP
            await session.initialize()

            # Tự động khám phá các tool do server công bố
            result = await session.list_tools()

            print("=== DANH SÁCH TOOL ===")
            for tool in result.tools:
                print(f"- {tool.name}: {tool.description}")

            print(f"\nTổng số tool: {len(result.tools)}")

            # Gọi tool search_lessons
            result = await session.call_tool(
                "search_lessons",
                {"query": "đánh giá kết quả rèn luyện sinh viên"},
            )

            print("\n=== KẾT QUẢ SEARCH ===")
            for item in result.content:
                if hasattr(item, "text"):
                    print(item.text)


            result = await session.call_tool(
                "get_course_plan",
                {"course_id": "CA101"},
)

            print("\n=== KẾT QUẢ COURSE PLAN ===")
            for item in result.content:
                if hasattr(item, "text"):
                    print(item.text)


            result = await session.call_tool(
                "create_study_request",
                {
                "student_id": "SV001",
                "course_id": "CA101",
                "request_content": "Tôi cần hỗ trợ ôn tập tuần 1",
    },
)

            print("\n=== KẾT QUẢ TẠO YÊU CẦU ===")
            for item in result.content:
                if hasattr(item, "text"):
                    print(item.text)

            result = await session.call_tool(
                "get_study_request",
                {"request_id": "REQ0001"},
)

            print("\n=== KẾT QUẢ ĐỌC LẠI YÊU CẦU ===")
            for item in result.content:
                if hasattr(item, "text"):
                    print(item.text)


if __name__ == "__main__":
    asyncio.run(main())
