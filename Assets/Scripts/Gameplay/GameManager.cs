using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using Random = UnityEngine.Random;

namespace Gameplay
{
    public class GameManager : MonoBehaviour
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
            _validTiles = ResourceLibrary.Instance.AllTileKeys().ToList();
        }

        public GameObject GenerateTileItem(GameObject parent)
        {
            return GenerateTileItem(parent.transform);
        }

        public GameObject GenerateTileItem(Transform parent)
        {
            GameObject toReturn = Instantiate(_itemPrefab, parent);
            // Get the sprite
            SpriteRenderer r = toReturn.GetComponent<SpriteRenderer>();
            if (_validTiles.Count == 0) throw new Exception("There are no valid tiles to choose from!");
            int index =  Random.Range(0, _validTiles.Count);
            string itemName =  _validTiles[index];
            r.sprite = ResourceLibrary.Instance.GetTexture(itemName);
            // Assign the name to the item for match detection
            Item I = toReturn.GetComponent<Item>();
            I.AssignItemName(itemName);
            // Make sure item is positioned to be visible.
            toReturn.transform.localPosition = Vector3.back;
            return toReturn;
        }

        public GameObject GenerateTileItem(Vector2Int position)
        {
            return GenerateTileItem(GridManager.Instance.TileDictionary[position].transform);
        }

        public void SetMostRecentSwap(GridTile tile, GridTile other)
        {
            _mostRecentSwap = Tuple.Create(tile, other);
        }

        public IEnumerator ValidateRecentSwap()
        {
            // If this changes, then we should check for matches
            List<GridTile> matchTiles = null;
            bool didMatch = _mostRecentSwap.Item1.IsPartOfMatch(ref matchTiles);
            foreach (GridTile t in matchTiles)
            {
                t.Clear();
            }
            // Also check for the other component
            didMatch = didMatch || _mostRecentSwap.Item2.IsPartOfMatch(ref matchTiles);
            foreach (GridTile t in matchTiles)
            {
                t.Clear();
            }

            if (didMatch)
            {
                List<GridTile> remainingMatches = new List<GridTile>();
                while (GridManager.Instance.IsGridUnstable() || GridManager.Instance.BoardContainsMatch(ref remainingMatches))
                {
                    foreach (GridTile t in remainingMatches)
                    {
                        t.Clear();
                    }
                    remainingMatches.Clear();
                    yield return null;
                }
            }
            // If no match is created, we swap the tiles back.
            else
            {
                _mostRecentSwap.Item1.SwapWith(_mostRecentSwap.Item2, false);
            }

            yield break;
        }

        [Range(0.1f, 0.4f)]
        public float FallTime;
        public static GameManager Instance => _instance;
        private static GameManager _instance;
        private List<string> _validTiles;
        [SerializeField]
        private GameObject _itemPrefab;
        private Tuple<GridTile, GridTile> _mostRecentSwap;
    }

}