using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Whisper.Samples;

public class StartInterview : MonoBehaviour
{
    public Transform CameraTransform;
    private Transform tr;
    public Transform chairTransform;
    public StreamingSampleMic streamingSampleMic;
    public UICanvas uiCanvas;
    // Start is called before the first frame update
    void Start()
    {
        tr = GetComponent<Transform>();
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void onClick() {
        Debug.Log("Sitting on chair");
        sitOnChair();
    }

    IEnumerator beginSitOnChair() {

        Vector3 chairFrontTransform = tr.position - CameraTransform.position + chairTransform.position + new Vector3(0.8f, 1.52f, 0);
        Vector3 chairSitTransform = tr.position - CameraTransform.position + chairTransform.position + new Vector3(0.5f, 1.15f, 0);
        Quaternion chairFrontRotation = Quaternion.Euler(0, 90, 0);

        // Move to front of chair
        while (Vector3.Distance(tr.position, chairFrontTransform) > 0.1f) {
            tr.position = Vector3.MoveTowards(tr.position, chairFrontTransform, 0.02f);
            yield return null;
        }

        // sit on chair
        while (Vector3.Distance(tr.position, chairSitTransform) > 0.1f) {
            tr.position = Vector3.MoveTowards(tr.position, chairSitTransform, 0.01f);
            yield return null;
        }

        uiCanvas.showCanvas();
        
        WaitForSeconds wait = new WaitForSeconds(3.0f);
        yield return wait;

        Debug.Log("Interview Start");
        streamingSampleMic.OnStartInterview();
    }

    IEnumerator beginStandUpFromChair() {
        Vector3 chairFrontTransform = tr.position - CameraTransform.position + chairTransform.position + new Vector3(0.8f, 1.52f, 0);

        Debug.Log("Interview Quit, Stand up from chair");
        streamingSampleMic.OnQuitInterview();

        uiCanvas.hideCanvas();

        while(Vector3.Distance(tr.position, chairFrontTransform) > 0.1f) {
            tr.position = Vector3.MoveTowards(tr.position, chairFrontTransform, 0.01f);
            yield return null;
        }
    }

    void sitOnChair() {
        StartCoroutine(beginSitOnChair());
    }

    public void standUpFromChair() {
        StartCoroutine(beginStandUpFromChair());
    }
}
