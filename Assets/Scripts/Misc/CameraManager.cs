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

        public void SetCameraPosition(Vector2 position)
        {
            transform.position = new Vector3(position.x, position.y, transform.position.z);
        }

        public void AdjustSize(Vector2 minWorldSize)
        {
            float accomodateHeight = minWorldSize.y / 2f;
            float accomodateWidth = minWorldSize.x / _cam.aspect / 2f;
            _cam.orthographicSize = Mathf.Max(accomodateHeight, accomodateWidth) / _whitespace;
        }

        public static CameraManager Instance => _instance;
        private static CameraManager _instance;
        private Camera _cam;
        [SerializeField]
        [Tooltip("The amount the camera will zoom out. Closer to 1 = more zoomed in.")]
        [Range(0.6f, 1f)]
        private float _whitespace;
    }

}