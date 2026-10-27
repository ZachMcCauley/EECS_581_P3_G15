using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;

namespace Input
{
    public class InputManager : MonoBehaviour
    {
        private void Awake()
        {
            if (_instance != null && _instance != this)
            {
                Destroy(gameObject);
                return;
            }

            _instance = this;
            DontDestroyOnLoad(gameObject);
            SetupInputDictionary();
        }

        private void SetupInputDictionary()
        {
            _actions = new Dictionary<string, InputAction>();
            _maps = new Dictionary<string, InputActionMap>();
            foreach (InputActionMap map in _inputs.actionMaps)
            {
                string mapName = map.name;
                foreach (InputAction action in map.actions)
                {
                    string actionName = action.name;
                    action.Enable();
                    string key = mapName + "." + actionName;
                    _actions.Add(key, action);
                    Debug.Log("Added action: " + key + "!");
                }

                _maps.Add(mapName, map);
                map.Disable();
            }
        }

        public void EnableActionMap(string mapName)
        {
            _maps[mapName].Enable();
        }

        public void DisableActionMap(string mapName)
        {
            _maps[mapName].Disable();
        }

        public bool GetAction(string actionName, ref InputAction returnedValue)
        {
            if (!_actions.ContainsKey(actionName))
            {
                returnedValue = _actions[actionName];
            }
            else
            {
                returnedValue = null;
            }

            return returnedValue != null;
        }

        // A function overload, if this is more reasonable for you.
        public bool GetAction(string mapName, string actionName, ref InputAction returnedValue)
        {
            return GetAction(mapName + "." + actionName, ref returnedValue);
        }

        public static InputManager Instance => _instance;
        private static InputManager _instance;

        private Dictionary<string, InputAction> _actions;
        private Dictionary<string, InputActionMap> _maps;

        [SerializeField] private InputActionAsset _inputs;
    }

}