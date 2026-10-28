using UnityEngine;

public class Item : MonoBehaviour
{
    private void Awake()
    {
        
    }

    private void Start()
    {
        
    }

    private void Update()
    {
        
    }

    public void AssignItemName(string itemName)
    {
        _itemName = itemName;
    }

    private string _itemName;
    private ScriptableObject _powerupInfo;
}
