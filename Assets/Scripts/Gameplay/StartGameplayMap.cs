using UnityEngine;
using Input;

namespace Gameplay
{
    public class StartGameplayMap : MonoBehaviour
    {
        private void Start()
        {
            InputManager.Instance.EnableActionMap("Gameplay");
            Destroy(gameObject);
        }

    }
}