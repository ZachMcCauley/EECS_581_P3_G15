using UnityEngine;
using UnityEngine.InputSystem;

namespace Misc
{

    [RequireComponent(typeof(Camera))]
    public class CameraManager : MonoBehaviour
    {
        private void Awake()
        {
            if (_instance != null && _instance != this)
            {
                Destroy(this.gameObject);
                return;
            }

            _instance = this;
            _cam = GetComponent<Camera>();
        }

        public Vector2 GetMouseWorldPosition()
        {
            // Get mouse position
            Vector3 mousePos = Mouse.current.position.ReadValue();
            // Get the true location the mouse is at in the game engine
            Vector3 trueWorldPos = _cam.ScreenToWorldPoint(mousePos);
            // Remove the z-component.
            Vector2 flattenedWorldPos = new Vector2(trueWorldPos.x, trueWorldPos.y);
            return flattenedWorldPos;
        }

        public static CameraManager Instance => _instance;
        private static CameraManager _instance;
        private Camera _cam;
    }

}