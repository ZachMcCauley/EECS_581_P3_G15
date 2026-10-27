using UnityEngine;

namespace Gameplay
{
public class GridTile : MonoBehaviour
{
    // Assigns the tile above (or null if no such tile exists) to the variable returnedTile
    // Returns whether there was a tile above to write into returnedTile
    public bool GetTileAbove(ref GridTile returnedTile)
    {
        if (!HasTileAbove())
        {
            returnedTile = null;
            return false;
        }
        
        returnedTile = GridManager.Instance.TileDictionary[location + Vector2Int.up];
        return true;
    }
    // Returns whether there is a tile above this one.
    public bool HasTileAbove()
    {
        if (GridManager.Instance == null || GridManager.Instance.TileDictionary == null)
        {
            Debug.LogWarning("There should be a GridManager set up by this point!");
            return false;
        }

        return GridManager.Instance.TileDictionary.ContainsKey(location + Vector2Int.up);
    }
    public bool IsPartOfMatch()
    {
        throw new System.NotImplementedException();
    }

    public bool IsPartOfSpecialMatch()
    {
        throw new System.NotImplementedException();
    }
    public void Clear()
    {
        throw new System.NotImplementedException();
    }

    public void CreatePowerupHere()
    {
        throw new System.NotImplementedException();
    }
    
    public Vector2Int location;

}

}