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
        
        DontDestroyOnLoad(gameObject);
        LoadAssets();
    }

    private void LoadAssets()
    {
        GetTileTextures();
    }
    private void GetTileTextures()
    {
        _tileTextures = Resources.LoadAll<Texture2D>(_tileTexturePath);
    }

    public Texture2D GetTexture(int index)
    {
        return  _tileTextures[index];
    }

    public static ResourceLibrary Instance => _instance;
    private static ResourceLibrary _instance;
    
    [SerializeField]
    private string _tileTexturePath;
    private Texture2D[] _tileTextures;
}
