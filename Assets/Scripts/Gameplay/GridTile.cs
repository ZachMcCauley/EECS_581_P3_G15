using System;
using System.Collections;
using UnityEngine;

namespace Gameplay
{
public class GridTile : MonoBehaviour
{
    public void Awake()
    {
        _currentItem = null;
    }

    public void Update()
    {
        GetItemIfIShould();
    }

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

    public Item GetItemValue()
    {
        Item toReturn = _currentItem;
        _currentItem = null;
        return toReturn;
    }

    public void GetItemIfIShould()
    {
        // If the tile is not empty, this function should do nothing
        if (_currentItem != null) return;
        
        // Otherwise, we should pull from the tile above it, or generate a new item
        GridTile t = null;
        if (GetTileAbove(ref t))
        {
            Item I = t.GetItemValue();
            if (I == null) return;
            _currentItem = I;
            I.transform.SetParent(transform);
            StartCoroutine(FallDown());
        }
        else
        {
            GameObject o = GameManager.Instance.GenerateTileItem(transform);
            _currentItem = o.GetComponent<Item>();
            _doingFallingAnimation = false;
        }
    }

    private IEnumerator FallDown()
    {
        _doingFallingAnimation = true;
        Vector3 currentPosition = _currentItem.transform.localPosition;
        Vector3 targetPosition = Vector3.back;
        for (float f = 0; f < GameManager.Instance.FallTime; f += Time.deltaTime)
        {
            _currentItem.transform.localPosition = Vector3.Lerp(currentPosition,
                targetPosition, 
                f / GameManager.Instance.FallTime
            );
            yield return null;
        }
        _currentItem.transform.localPosition = targetPosition;
        _doingFallingAnimation = false;
        yield break;
    }
    
    
    public Vector2Int location;
    private Item _currentItem;
    private bool _doingFallingAnimation;

}

}