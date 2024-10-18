using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;
using Whisper.Utils;

public class Conversation : MonoBehaviour
{
    public class Interviewer
    {
        public string role;
        public string content;
    }

    private enum ConversationState
    {
        Start,
        Question,
        Answer
    }
    
    public Text answerTextBox;
    public ScrollRect answerScrollRect;
    public Text questionTextBox;
    public ScrollRect questionScrollRect;

    private string url = "http://3.35.4.203:8000/";
    private Interviewer resultJson;
    public RawImage warmSaying;
    public RawImage coldSaying;
    public RawImage moderateSaying;

    public TTS tts;

    // Start is called before the first frame update
    void Start()
    {
        //audioSource = GetComponent<AudioSource>();
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    IEnumerator GetConversation(ConversationState type, string url, string text = "")
    {
        int retry = 0;
        while(retry < 3) {
            UnityWebRequest www;
            if(type == ConversationState.Question)
                www = UnityWebRequest.Get(url);
            else if(type == ConversationState.Answer) {
                //var inputString = JsonUtility.ToJson(text);
                //print("inputString : " + inputString);
                www = UnityWebRequest.Post(url, '"' + text + '"', "application/json");
            }
            else // type == ConversationState.Start
                www = UnityWebRequest.Post(url, "", "application/json");
            
            yield return www.SendWebRequest();
            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.Log(www.error);
                retry++;
                WaitForSeconds wait = new WaitForSeconds(1.0f); // retry after 1 second
                yield return wait;
                continue;
            }
            else
            {
                var result = www.downloadHandler.text;
                print(result);

                if(type == ConversationState.Answer) {
                    answerTextBox.text = result + "\n로 답하는 것이 더 좋을 것 같습니다.";
                    UiUtils.ScrollDown(answerScrollRect);
                    //tts.Convert(result + "로 답하는 것이 더 좋을 것 같습니다.");
                } else {
                    resultJson = JsonUtility.FromJson<Interviewer>(result);
                    questionTextBox.text = resultJson.content;
                    UiUtils.ScrollDown(questionScrollRect);
                    print("role : " + resultJson.role + "\ntext : " + resultJson.content);
                    if(resultJson.role == "warm") {
                        warmSaying.gameObject.SetActive(true);
                    } else if(resultJson.role == "cold") {
                        coldSaying.gameObject.SetActive(true);
                    } else if(resultJson.role == "moderator") {
                        moderateSaying.gameObject.SetActive(true);
                    }
                    StartCoroutine(sayingIconInvisible());
                    tts.Convert(resultJson.content);
                }
                break;
            }
        }
    }

    public void startInterview() {
        print("start interview");
        StartCoroutine(GetConversation(ConversationState.Start, url + "start"));
    }

    public void getQuestion() {
        print("get question");
        StartCoroutine(GetConversation(ConversationState.Question, url + "question"));
    }

    public void sendAnswer(string answer) {
        print("send answer");
        StartCoroutine(GetConversation(ConversationState.Answer, url + "answer", answer));
    }

    IEnumerator sayingIconInvisible() {
        Debug.Log("sayingIconInvisible");
        WaitForSeconds wait = new WaitForSeconds(7.0f);
        yield return wait;
        Debug.Log("wait end");
        warmSaying.gameObject.SetActive(false);
        coldSaying.gameObject.SetActive(false);
        moderateSaying.gameObject.SetActive(false);
    }
}
