using System.Collections.Generic;
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
                
                GameObject O = Instantiate(_tilePrefab, _tileObjectContainer.transform);
                O.transform.position = (Vector3Int)cellPosition + _grid.gameObject.transform.position;
                GridTile tileScript = O.GetComponent<GridTile>();
                tileScript.location = cellPosition;
                
                _tileDictionary.Add(new Vector2Int(x, y), tileScript);
            }
        }
        
    }

    public bool IsGridUnstable()
    {
        foreach (GridTile tile in _tileDictionary.Values)
        {
            if (tile.DoingAnimation || !tile.HasItemValue()) return true;
        }
        return false;
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