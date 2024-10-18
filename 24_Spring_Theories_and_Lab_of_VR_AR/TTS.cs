using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

public class TTS : MonoBehaviour
{
    public TextMeshProUGUI tmp;

    private string korea = "Ko";

    private string url = "https://translate.google.com/translate_tts?ie=UTF-8&total=1&idx=0&textlen=32&client=tw-ob&q=";
    public AudioSource audioSource;

    // Start is called before the first frame update
    void Start()
    {
        audioSource = GetComponent<AudioSource>();
    }

    IEnumerator Speak(string str)
    {
        int retry = 0;
        while(retry < 3) {
            WWW www = new WWW(str);
            audioSource.clip = www.GetAudioClip(false, true, AudioType.MPEG);
            audioSource.Play();
            
            while(audioSource.isPlaying)
            {
                retry = 4;
                yield return null;
            }
        }
    }

    private string getString(string text, string stateName) {
        return text + "&tl=" + stateName + "-gb";
    }

    // Update is called once per frame
    void Update()
    {

    }

    public void OnClick()
    {
        print(tmp.text);
        StartCoroutine(Speak(url + getString(tmp.text, korea)));
    }

    public void Convert(string text) {
        StartCoroutine(Speak(url + getString(text, korea)));
    }
}
