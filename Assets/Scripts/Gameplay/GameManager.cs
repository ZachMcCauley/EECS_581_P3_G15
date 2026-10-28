using System;
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

        [Range(0.5f, 2)]
        public float FallTime;
        public static GameManager Instance => _instance;
        private static GameManager _instance;
        private List<string> _validTiles;
        [SerializeField]
        private GameObject _itemPrefab;
    }

}