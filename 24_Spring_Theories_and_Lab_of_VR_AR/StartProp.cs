using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class StartProp : MonoBehaviour
{
    public CharacterController characterController;
    public RawImage warmSaying;
    public RawImage coldSaying;
    public RawImage moderateSaying;
    // Start is called before the first frame update
    void Start()
    {
        characterController.skinWidth = 0.01f;
        characterController.stepOffset = 0.5f;
        characterController.slopeLimit = 45.0f;
        characterController.center = new Vector3(0, 0.76072f, 0);
        characterController.radius = 0.1f;
        characterController.height = 1.52144f;
        warmSaying.gameObject.SetActive(false);
        coldSaying.gameObject.SetActive(false);
        moderateSaying.gameObject.SetActive(false);
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
