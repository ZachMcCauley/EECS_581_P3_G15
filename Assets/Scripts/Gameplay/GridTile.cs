using System;
using System.Collections;
using UnityEngine;

namespace Gameplay
{
public class GridTile : MonoBehaviour
{
    private void Awake()
    {
        _currentItem = null;
    }

    private void Update()
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

    public bool HasItemValue()
    {
        return _currentItem != null;
    }
    public bool GetItemValue(ref Item returnLoc)
    {
        // If doing falling animation, item is unavailable
        if (_doingAnimation) return false;
        // Otherwise, we can just get the item
        bool toReturn = _currentItem != null;
        returnLoc = _currentItem;
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
            Item I = null;
            if (!t.GetItemValue(ref I)) return;
            SetCurrentItem(I);
            StartCoroutine(FallDown());
        }
        else
        {
            GenerateItem();
        }
    }

    private void GenerateItem()
    {
        GameObject o = GameManager.Instance.GenerateTileItem(transform);
        _currentItem = o.GetComponent<Item>();
        _doingAnimation = false;
    }

    private IEnumerator FallDown()
    {
        _doingAnimation = true;
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
        _doingAnimation = false;
        yield break;
    }

    public void SwapWith(GridTile other)
    {
        // Swap the items
        Item temp = _currentItem;
        SetCurrentItem(other._currentItem);
        other.SetCurrentItem(temp);
        StartCoroutine(FallDown());
        other.StartCoroutine(other.FallDown());
    }

    private void SetCurrentItem(Item item)
    {
        _currentItem = item;
        item.transform.SetParent(transform);
    }
    
    public Vector2Int location;
    private Item _currentItem;
    public bool DoingAnimation => _doingAnimation;
    private bool _doingAnimation;

}

}