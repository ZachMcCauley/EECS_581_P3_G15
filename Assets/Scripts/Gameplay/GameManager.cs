using UnityEngine;

namespace Gameplay
{
    internal enum TileIcons
    {
        CLOCK,
        FOLDER,
        MAIL,
        NOTE,
        SAVE,
        STICKY
    }
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

        }

        private void Update()
        {

        }

        public static GameManager Instance => _instance;
        private static GameManager _instance;
    }

}