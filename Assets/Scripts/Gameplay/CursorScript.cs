using System;
using Gameplay;
using Misc;
using UnityEngine;

namespace Gameplay
{
    [RequireComponent(typeof(SpriteRenderer))]
    public class CursorScript : MonoBehaviour
    {
        private void Awake()
        {
            _renderer = GetComponent<SpriteRenderer>();
        }

        private void Update()
        {
            // Reset the hover over tile. If we are still hovering over it,
            // We should be able to find it again.
            _hoverOver = null;
            
            // Find the tile we are hovering over using a raycast.
            
            RaycastHit2D[] mouseOn = Physics2D.RaycastAll(
                CameraManager.Instance.GetMouseWorldPosition(),
                Vector2.zero
            );

            foreach (RaycastHit2D hit in mouseOn)
            {
                // Check if this is a tile
                if (hit.collider.CompareTag("Tile"))
                {
                    _hoverOver = hit.collider.GetComponent<GridTile>();
                    transform.position = Vector3.back + hit.collider.transform.position;
                    break;
                }
            }
            
            HideIfIShould();
        }

        private void HideIfIShould()
        {
            _renderer.enabled = _hoverOver != null;
        }
        
        private SpriteRenderer _renderer;
        private GridTile _hoverOver;

    }

}