# client_test.py
import asyncio
import json
import os
from dotenv import load_dotenv

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from src.agent.agent import StudyAgent

load_dotenv()


async def run_e2e_test():
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "-m", "src.mcp.server"],
        env=os.environ.copy(),
    )

    print("=== KHỞI CHẠY KIỂM THỬ END-TO-END (E2E) SV2 ===")

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            agent = StudyAgent(mcp_session=session)

            # -------------------------------------------------------------
            # TEST 1: Truy vấn tra cứu RAG / Knowledge
            # -------------------------------------------------------------
            print("\n--- Test 1: Tra cứu thông tin môn học (RAG) ---")
            query_1 = "Kế hoạch môn học HTRL gồm những nội dung gì?"
            print(f"User Query: {query_1}")
            res_1 = await agent.ask(query_1)
            print(f"Agent Response:\n{res_1}")

            # -------------------------------------------------------------
            # TEST 2: Action Write & Read-back Verification (Thành công)
            # -------------------------------------------------------------
            print("\n--- Test 2: Tạo Study Request + Read-Back Verification ---")
            query_2 = (
                "Tôi là sinh viên mã SV2026, cần hỗ trợ gấp về phần hàm đệ quy trong môn CS101."
            )
            print(f"User Query: {query_2}")
            res_2 = await agent.ask(query_2)
            print(f"Agent Response:\n{res_2}")

            # -------------------------------------------------------------
            # TEST 3: Đảm bảo Guardrail khi thiếu student_id
            # -------------------------------------------------------------
            print("\n--- Test 3: Tạo Request nhưng CHƯA đưa student_id ---")
            query_3 = "Tạo giúp tôi một yêu cầu hỗ trợ môn CS102 về mảng 2 chiều."
            print(f"User Query: {query_3}")
            res_3 = await agent.ask(query_3)
            print(f"Agent Response:\n{res_3}")

    print("\n=== HOÀN THÀNH KIỂM THỬ E2E ===")


if __name__ == "__main__":
    asyncio.run(run_e2e_test())