# Gemini CLI Demo Ideas: Multi-Cloud MCP Property Agent

Here are four high-impact, 5-minute demo scripts to showcase the power of Gemini CLI.

## 1. The "Zero-to-Documentation" (Discovery & Visualization)
**The Hook:** Instantly map and document a complex, multi-language codebase you've never seen before.
*   **Prompt:** `"Read the project files and create a comprehensive README.md. Include an architecture diagram using Mermaid that shows how the Azure server, GCP server, and Property Agent interact."`
*   **Expected Outcome:** Gemini scans the directories, reads the C# and Python source files, and generates a structured `README.md`. It synthesizes a Mermaid flowchart showing the relationship between the components without being told how they connect.
*   **Why it's powerful:** It showcases **Discovery**. Gemini autonomously explores the file tree, understands the relationship between C# and Python services, and synthesizes a visual mental model (the diagram) without any manual explanation.

## 2. The "Feature Sprint" (Cross-File/Cross-Language Logic)
**The Hook:** Add a new business capability across the entire multi-cloud stack in 60 seconds.
*   **Prompt:** `"Add a 'Search by District' tool to the GCP server, and then update the Property Agent's instructions so it knows how to use this new tool to help users find properties in specific areas."`
*   **Expected Outcome:** Gemini adds the `search_properties_by_district` function to the Python GCP server and simultaneously updates the Agent's system prompt in a completely different directory to include "district" as a valid search parameter.
*   **Why it's powerful:** Gemini will simultaneously modify `gcp_mcp/server.py` (Python logic) and `property_agent/property_agent/agent.py` (Agent brain). It demonstrates that the CLI understands the **dependency** between the tool provider and the tool consumer across different programming languages.

## 3. The "AI Security & Hardening" Audit
**The Hook:** Instantly secure an AI Agent against modern LLM threats (Prompt Injection and Data Poisoning).
*   **Prompt:** `"Perform a security audit on the Agent's system instructions in property_agent/agent.py. Harden it against prompt injection and ensure it applies the principle of least privilege regarding the data it saves to the Azure database."`
*   **Expected Outcome:** Gemini rewrites the Agent's core instructions to include strict "Safety Boundaries," preventing the Agent from revealing its internal prompt or saving non-standard data (like URLs or scripts) to the favorites database.
*   **Why it's powerful:** It proves the CLI understands the unique, modern security threats associated with LLM applications. Gemini will rewrite the Agent's core instructions to include strict boundaries, preventing users from tricking the agent into saving malicious text or revealing its internal configuration.

## 4. The "Test Architect" (Zero-to-Verified)
**The Hook:** Generate and run tests for two different languages and frameworks in one go.
*   **Prompt:** `"Write a unit test for the C# FavoritesTool using xUnit, and then write a Python test using pytest to verify that the GCP server's 'search_properties_by_type' tool returns correct JSON structure. Run the Python test to verify."`
*   **Expected Outcome:** Gemini creates a C# test file using xUnit patterns and a Python test file using `pytest` logic. It then attempts to run the Python tests using the local environment tools (`uv` or `python`) and provides the output.
*   **Why it's powerful:** It demonstrates the **Action -> Validation** loop. It shows Gemini can switch contexts between NuGet/dotnet and pip/uv flawlessly, ensuring the code it writes actually works.

---

### 💡 Pro-Tip for your Demo Flow (3 Minutes):
1.  **Show:** Open the `README.md` to show the architecture diagram (Result of Idea #1).
2.  **Act:** Run the "Feature Sprint" prompt (Idea #2).
3.  **Result:** Show the side-by-side diff: The Python server got a new function, and the Agent's system prompt was updated to mention "districts."
4.  **Punchline:** *"I just refactored a multi-cloud system across two languages and an AI orchestrator with one sentence."*
