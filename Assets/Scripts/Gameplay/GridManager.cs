using System.Collections.Generic;
using Misc;
using UnityEngine;
using UnityEngine.Tilemaps;

namespace Gameplay
{
public class GridManager : MonoBehaviour
{
    private void Awake()
    {
        if (_instance != null && _instance != this)
        {
            Destroy(this.gameObject);
            return;
        }

        _instance = this;
    }

    private void Start()
    {
        SetupTilemap();
    }

    private void SetupTilemap()
    {
        _tileDictionary = new Dictionary<Vector2Int, GridTile>();
        // Trim bounds of grid. This keeps bounds as small as possible to avoid creating unnessecary tiles.
        _grid.CompressBounds();
        // Move camera & adjust size
        AdjustCameraPosition();
        // Create tiles objects for each grid space.
        BoundsInt bounds = _grid.cellBounds;
        /*
         * Iterate through all tile x/y positions
         * Theoretically, we can iterate through the Z-positions if necessary, but I see no
         * compelling reason to do so.
         */
        for (int x = bounds.min.x; x < bounds.max.x; x++)
        {
            for (int y = bounds.min.y; y < bounds.max.y; y++)
            {
                Vector2Int cellPosition = new Vector2Int(x, y);
                if (_grid.GetTile(new Vector3Int(x, y)) == null) continue;
                
                AddGridTile(cellPosition);
                AddGridTile(cellPosition + Vector2Int.up);
                
            }
        }
        
        SetupSpriteMask();
        
    }

    private void AddGridTile(Vector2Int position)
    {
        if (_tileDictionary.ContainsKey(position)) return;
        
        GameObject O = Instantiate(_tilePrefab, _tileObjectContainer.transform);
        O.transform.position = (Vector3Int)position + _grid.gameObject.transform.position;
        GridTile tileScript = O.GetComponent<GridTile>();
        tileScript.location = position;
                
        _tileDictionary.Add(position, tileScript);
    }
    private void SetupSpriteMask()
    {
        // Create a texture from the grid.
        BoundsInt bounds = _grid.cellBounds;
        Vector2Int size = new Vector2Int(Mathf.RoundToInt(bounds.size.x), Mathf.RoundToInt(bounds.size.y));
        Texture2D img =  new Texture2D(size.x, size.y);
        for (int x = 0; x < size.x; x++)
        {
            for (int y = 0; y < size.y; y++)
            {
                Vector2Int pos =  new Vector2Int(x + bounds.xMin, y + bounds.yMin);
                img.SetPixel(x,
                    y,
                    _tileDictionary.ContainsKey(pos) ? Color.white : Color.clear
                );
            }
        }
        img.filterMode = FilterMode.Point;
        img.Apply();
        // Create a sprite from the texture
        Sprite spr = Sprite.Create(
            img,
            new Rect(0, 0, size.x, size.y),
            new Vector2(
                -1 * (float)bounds.xMin / size.x,
                -1 * (float)bounds.yMin / size.y
            ),
            1f
        );
        
        _tileObjectContainer.GetComponent<SpriteMask>().sprite = spr;
    }

    private void AdjustCameraPosition()
    {
        // Adjust position
        BoundsInt bounds = _grid.cellBounds;
        Vector2 pos = bounds.center;
        CameraManager.Instance.SetCameraPosition(pos);
        
        // Adjust zoom
        Vector2 worldSize = new Vector2(bounds.size.x, bounds.size.y);
        CameraManager.Instance.AdjustSize(worldSize);
    }

    public bool IsGridUnstable()
    {
        foreach (GridTile tile in _tileDictionary.Values)
        {
            if (tile.DoingAnimation || !tile.HasItemValue()) return true;
        }
        return false;
    }

    public bool BoardContainsMatch(ref List<GridTile> matchingTiles)
    {
        matchingTiles = new List<GridTile>();
        List<GridTile> matchTiles = new List<GridTile>();
        foreach (GridTile tile in _tileDictionary.Values)
        {
            tile.IsPartOfMatch(ref matchTiles);
            matchingTiles.AddRange(matchTiles);
        }
        return matchingTiles.Count > 0;
    }

    public static GridManager Instance => _instance;
    private static GridManager _instance;

    [SerializeField]
    private Tilemap _grid;
    [SerializeField]
    private GameObject _tileObjectContainer;
    [SerializeField]
    private GameObject _tilePrefab;

    public Dictionary<Vector2Int, GridTile> TileDictionary => _tileDictionary;
    private Dictionary<Vector2Int, GridTile> _tileDictionary;

}

}