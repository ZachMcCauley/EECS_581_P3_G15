using System;
using System.Collections;
using System.Collections.Generic;
using Input;
using UnityEngine;
using UnityEngine.InputSystem;

namespace Gameplay
{
public class GridTile : MonoBehaviour
{
    private void Awake()
    {
        _currentItem = null;
    }
    private void Start()
    {
        GenerateItem();
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
    public bool IsPartOfMatch(ref List<GridTile> match)
    {
        // Spawner tiles should never match
        if (IsSpawnerTile)
        {
            match = new List<GridTile>();
            return false;
        }
        // Detect horizontal matches
        match = new List<GridTile>();
        match.Add(this);
        // Go left
        for (int x = location.x - 1; true; x--)
        {
            Vector2Int pos =  new Vector2Int(x, location.y);
            if (!GridManager.Instance.TileDictionary.ContainsKey(pos)) break;
            GridTile t = GridManager.Instance.TileDictionary[pos];
            if (t._currentItem.ItemName != _currentItem.ItemName) break;
            match.Add(t);
        }
        // Go right
        for (int x = location.x + 1; true; x++)
        {
            Vector2Int pos =  new Vector2Int(x, location.y);
            if (!GridManager.Instance.TileDictionary.ContainsKey(pos)) break;
            GridTile t = GridManager.Instance.TileDictionary[pos];
            if (t._currentItem.ItemName != _currentItem.ItemName) break;
            match.Add(t);
        }
        // Reset if no match formed.
        if (match.Count < 3)
        {
            match.Clear();
        }
        // Detect vertical matches
        List<GridTile> vMatch = new List<GridTile>();
        vMatch.Add(this);
        // Go down
        for (int y = location.y - 1; true; y--)
        {
            Vector2Int pos =  new Vector2Int(location.x, y);
            if (!GridManager.Instance.TileDictionary.ContainsKey(pos)) break;
            GridTile t = GridManager.Instance.TileDictionary[pos];
            if (t._currentItem.ItemName != _currentItem.ItemName) break;
            vMatch.Add(t);
        }
        // Go up
        for (int y = location.y + 1; true; y++)
        {
            Vector2Int pos =  new Vector2Int(location.x, y);
            if (!GridManager.Instance.TileDictionary.ContainsKey(pos)) break;
            GridTile t = GridManager.Instance.TileDictionary[pos];
            // Spawner tiles also cannot contribute to matches
            if (IsSpawnerTile) break;
            if (t._currentItem.ItemName != _currentItem.ItemName) break;
            vMatch.Add(t);
        }

        // Reset if no match formed.
        if (vMatch.Count < 3)
        {
            vMatch.Clear();
        }
        
        // Join both lists
        match.AddRange(vMatch);
        
        // If the list is not empty, a match was formed.
        return match.Count != 0;
    }

    public bool IsPartOfSpecialMatch()
    {
        throw new System.NotImplementedException();
    }
    public void Clear()
    {
        if(_currentItem != null) Destroy(_currentItem.gameObject);
        _currentItem = null;
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
            StartCoroutine(MoveItemToCenter());
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

    private IEnumerator MoveItemToCenter()
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

    public void SwapWith(GridTile other, bool shouldValidateAfter = true)
    {
        // Invoke a coroutine
        StartCoroutine(HandleSwaps(other, shouldValidateAfter));
    }

    private void SetCurrentItem(Item item)
    {
        _currentItem = item;
        item.transform.SetParent(transform);
    }

    private IEnumerator HandleSwaps(GridTile other, bool shouldValidateAfter)
    {
        // We should disable player selection while swaps are occuring.
        InputAction select = null;
        if (!InputManager.Instance.GetAction("Gameplay.Select", ref select))
        {
            throw new Exception("Cannot find Select action to disable it!");
        }
        select.Disable();
        // Swap the items
        Item temp = _currentItem;
        SetCurrentItem(other._currentItem);
        other.SetCurrentItem(temp);
        StartCoroutine(MoveItemToCenter());
        other.StartCoroutine(other.MoveItemToCenter());
        // Wait for both coroutines to finish.
        while (_doingAnimation || other._doingAnimation) yield return null;
        // Note which tiles were swapped. If necessary, they may need to be swapped back.
        GameManager.Instance.SetMostRecentSwap(this, other);
        // Now validate the swaps if we should
        if (shouldValidateAfter) yield return GameManager.Instance.ValidateRecentSwap();
        // We must now return the player's agency
        select.Enable();
        yield break;
    }

    private bool IsSpawnerTile => !HasTileAbove();
    public Vector2Int location;
    private Item _currentItem;
    public bool DoingAnimation => _doingAnimation;
    private bool _doingAnimation;

}

}