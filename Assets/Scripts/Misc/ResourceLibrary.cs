using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public class ResourceLibrary : MonoBehaviour
{
    private void Awake()
    {
        if (_instance != null && _instance != this)
        {
            Destroy(this.gameObject);
            return;
        }

        _instance = this;
        LoadAssets();
    }

    private void LoadAssets()
    {
        GetTileTextures();
    }
    private void GetTileTextures()
    {
        _tileTextures = new Dictionary<string, Sprite>();
        Sprite[] textures = Resources.LoadAll<Sprite>(_tileTexturePath);
        foreach (Sprite texture in textures)
        {
            Debug.Log("Loaded " +  texture.name);
            _tileTextures[texture.name.ToUpper()] = texture;
        }
    }

    public Sprite GetTexture(string key)
    {
        return  _tileTextures[key];
    }

    public string[] AllTileKeys()
    {
        return  _tileTextures.Keys.ToArray();
    }

    public static ResourceLibrary Instance => _instance;
    private static ResourceLibrary _instance;
    
    [SerializeField]
    private string _tileTexturePath;
    private Dictionary<string, Sprite> _tileTextures;
}
