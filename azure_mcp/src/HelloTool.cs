using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Extensions.Mcp;
using Microsoft.Extensions.Logging;
using static FunctionsSnippetTool.ToolsInformation;

namespace FunctionsSnippetTool;
// https://learn.microsoft.com/en-us/azure/azure-functions/scenario-custom-remote-mcp-server?tabs=linux&pivots=programming-language-csharp

public class HelloTool(ILogger<HelloTool> logger)
{
    [Function(nameof(SayHello))]
    public string SayHello(
        [McpToolTrigger(HelloToolName, HelloToolDescription)] ToolInvocationContext context
    )
    {
        logger.LogInformation("Saying hello");
        return "Hello JLL (all the way from Azure)!";
    }
}
