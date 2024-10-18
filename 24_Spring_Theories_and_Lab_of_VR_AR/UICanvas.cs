using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class UICanvas : MonoBehaviour
{
    GameObject canvas;
    // Start is called before the first frame update
    void Start()
    {
        canvas = this.gameObject;
        canvas.SetActive(false);
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void showCanvas() {
        canvas.SetActive(true);
    }

    public void hideCanvas() {
        canvas.SetActive(false);
    }
}
