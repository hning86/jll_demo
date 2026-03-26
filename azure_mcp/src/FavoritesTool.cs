using System.Text.Json;
using Azure.Storage.Blobs;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Extensions.Mcp;
using static FunctionsSnippetTool.ToolsInformation;

namespace FunctionsSnippetTool;

public class FavoritesTool
{
    private const string BlobPath = "favorites/default.json";

    [Function(nameof(SaveFavoriteItem))]
    public async Task<string> SaveFavoriteItem(
        [McpToolTrigger(SaveFavoriteItemToolName, SaveFavoriteItemToolDescription)]
            ToolInvocationContext context,
        [McpToolProperty(FavoriteItemPropertyName, FavoriteItemPropertyDescription, true)]
            string item,
        [BlobInput(BlobPath)] BlobClient blobClient
    )
    {
        var list = new List<string>();
        
        if (await blobClient.ExistsAsync())
        {
            var downloadResult = await blobClient.DownloadContentAsync();
            var content = downloadResult.Value.Content.ToString();
            
            if (!string.IsNullOrEmpty(content))
            {
                try
                {
                    var existingList = JsonSerializer.Deserialize<List<string>>(content);
                    if (existingList != null)
                    {
                        list.AddRange(existingList);
                    }
                }
                catch (JsonException)
                {
                    // Fallback to legacy single item support
                    list.Add(content);
                }
            }
        }

        list.Add(item);
        
        var jsonContent = JsonSerializer.Serialize(list);
        await blobClient.UploadAsync(BinaryData.FromString(jsonContent), overwrite: true);
        
        return jsonContent;
    }

    [Function(nameof(RemoveFavoriteItem))]
    public async Task<string> RemoveFavoriteItem(
        [McpToolTrigger(RemoveFavoriteItemToolName, RemoveFavoriteItemToolDescription)]
            ToolInvocationContext context,
        [McpToolProperty(FavoriteItemPropertyName, FavoriteItemPropertyDescription, true)]
            string item,
        [BlobInput(BlobPath)] BlobClient blobClient
    )
    {
        var list = new List<string>();
        
        if (await blobClient.ExistsAsync())
        {
            var downloadResult = await blobClient.DownloadContentAsync();
            var content = downloadResult.Value.Content.ToString();
            
            if (!string.IsNullOrEmpty(content))
            {
                try
                {
                    var existingList = JsonSerializer.Deserialize<List<string>>(content);
                    if (existingList != null)
                    {
                        list.AddRange(existingList);
                    }
                }
                catch (JsonException)
                {
                    // Fallback to legacy single item support
                    list.Add(content);
                }
            }
        }

        list.RemoveAll(x => x == item);
        
        var jsonContent = JsonSerializer.Serialize(list);
        await blobClient.UploadAsync(BinaryData.FromString(jsonContent), overwrite: true);
        
        return jsonContent;
    }

    [Function(nameof(GetFavoriteItems))]
    public async Task<string> GetFavoriteItems(
        [McpToolTrigger(GetFavoriteItemsToolName, GetFavoriteItemsToolDescription)]
            ToolInvocationContext context,
        [BlobInput(BlobPath)] BlobClient blobClient
    )
    {
        if (!await blobClient.ExistsAsync())
        {
            return "[]";
        }

        var downloadResult = await blobClient.DownloadContentAsync();
        return downloadResult.Value.Content.ToString();
    }
}
