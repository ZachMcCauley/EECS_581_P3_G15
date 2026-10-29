using System;
using System.Collections;
using Gameplay;
using Input;
using Misc;
using UnityEngine;
using UnityEngine.InputSystem;

namespace Gameplay
{
    [RequireComponent(typeof(SpriteRenderer))]
    public class CursorScript : MonoBehaviour
    {
        private void Awake()
        {
            _renderer = GetComponent<SpriteRenderer>();
            _hasStarted = false;
        }

        private void Start()
        {
            _hasStarted = true;
            OnEnable();
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
                    transform.position = Vector3.back * 2 + hit.collider.transform.position;
                    break;
                }
            }
            
            // Thou shalt not hover over spawner tiles
            if (_hoverOver != null && !_hoverOver.HasTileAbove()) _hoverOver = null;
            
            HideIfIShould();

            // If we are not hovering over a tile, we unselect any selected tile
            // Bear in mind that we are dealing in the context of "dragging tiles."
            if (_hoverOver == null) _selectedTile = null;
            
            // Attempt to swap two tiles
            TrySwapTile();
        }

        private void OnEnable()
        {
            if (!_hasStarted) return;
            
            InputAction action = null;
            if (InputManager.Instance.GetAction("Gameplay.Select", ref action))
            {
                action.performed += OnClick;
                action.canceled += OnUnclick;
            }
            else
            {
                throw new Exception("Selection input not found.");
            }
        }

        private void OnDisable()
        {
            if (!_hasStarted) return;
            InputAction action = null;
            if (InputManager.Instance.GetAction("Gameplay.Select", ref action))
            {
                action.performed -= OnClick;
                action.canceled -= OnUnclick;
            }
            else
            {
                throw new Exception("Selection input not found.");
            }
        }
        private void HideIfIShould()
        {
            _renderer.enabled = _hoverOver != null;
        }

        private void OnClick(InputAction.CallbackContext ctx)
        {
            _selectedTile = _hoverOver;
        }

        private void OnUnclick(InputAction.CallbackContext ctx)
        {
            _selectedTile = null;
        }

        // Attempts to swap a pair of tiles
        // Returns whether or not a swap is successful.
        private bool TrySwapTile()
        {
            // If either the selected or hovered tile is null, we cannot swap.
            if (_hoverOver == null || _selectedTile == null) return false;
            // If the tiles are not orthogonally adjacent, we shouldn't swap.
            if ((_hoverOver.location - _selectedTile.location).sqrMagnitude != 1) return false;
            // If the board state is unstable (an animation is occuring or any tile is empty),
            // The swap should fail.
            if (GridManager.Instance.IsGridUnstable()) return false;
            // Swap the items
            _hoverOver.SwapWith(_selectedTile);
            // Reset selected tile
            _selectedTile = null;
            return true;
        }
        
        private SpriteRenderer _renderer;
        private GridTile _hoverOver;
        private GridTile _selectedTile;
        private bool _hasStarted;

    }

}