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
        _tileDictionary = new Dictionary<Vector2Int, GameObject>();
        // Trim bounds of grid. This keeps bounds as small as possible to avoid creating unnessecary tiles.
        grid.CompressBounds();
        // Create tiles objects for each grid space.
        BoundsInt bounds = grid.cellBounds;
        /*
         * Iterate through all tile x/y positions
         * Theoretically, we can iterate through the Z-positions if necessary, but I see no
         * compelling reason to do so.
         */
        for (int x = bounds.min.x; x < bounds.max.x; x++)
        {
            for (int y = bounds.min.y; y < bounds.max.y; y++)
            {
                Vector3Int cellPosition = new Vector3Int(x, y, 0);
                
                GameObject O = Instantiate(tilePrefab, tileObjectContainer.transform);
                O.transform.position = cellPosition;
                GridTile tileScript = O.GetComponent<GridTile>();
                tileScript.location = cellPosition;
            }
        }
    }

    public static GridManager Instance => _instance;
    private static GridManager _instance;

    public Tilemap grid;
    public GameObject tileObjectContainer;
    public GameObject tilePrefab;

    public Dictionary<Vector2Int, GameObject> TileDictionary => _tileDictionary;
    private Dictionary<Vector2Int, GameObject> _tileDictionary;

}

}