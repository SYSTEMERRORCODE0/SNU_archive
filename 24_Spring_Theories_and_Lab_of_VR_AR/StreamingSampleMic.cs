using System;
using System.Collections;
using UnityEngine;
using UnityEngine.UI;
using Whisper.Utils;

namespace Whisper.Samples
{
    /// <summary>
    /// Stream transcription from microphone input.
    /// </summary>
    public class StreamingSampleMic : MonoBehaviour
    {
        public WhisperManager whisper;
        public MicrophoneRecord microphoneRecord;
    
        [Header("UI")] 
        public Button button;
        public Text buttonText;
        public Text text;
        public ScrollRect scroll;
        private WhisperStream _stream;

        public Conversation conversation;

        private bool _isStartConversation = false;
        private bool _isWaitingInterviewer = false;
        private bool _isWaitingQuestion = false;
        private bool _isWaitingAnswer = false;
        public Image vadIndicatorImage;

        private async void Start()
        {
            _isStartConversation = false;
            _isWaitingInterviewer = false;
            _isWaitingQuestion = false;
            _isWaitingAnswer = false;

            _stream = await whisper.CreateStream(microphoneRecord);
            _stream.OnResultUpdated += OnResult;
            _stream.OnSegmentUpdated += OnSegmentUpdated;
            _stream.OnSegmentFinished += OnSegmentFinished;
            _stream.OnStreamFinished += OnFinished;

            microphoneRecord.OnRecordStop += OnRecordStop;
            //button.onClick.AddListener(OnButtonPressed);
        }

        public void OnStartInterview()
        {
            _isStartConversation = true;
            _isWaitingInterviewer = true;
            conversation.startInterview();
            StartCoroutine(micRecording());
            buttonText.text = "Stop";
        }

        public void OnQuitInterview()
        {
            _isStartConversation = false;
            _isWaitingInterviewer = false;
            _isWaitingQuestion = false;
            _isWaitingAnswer = false;
            buttonText.text = "Start";
            vadIndicatorImage.color = Color.white;
            microphoneRecord.StopRecord();
            print("Quit Interview");
        }

        IEnumerator micRecording() {
            if(!_isStartConversation)
                yield return null;

            WaitForSeconds wait3sec = new WaitForSeconds(3);
            WaitForSeconds wait = new WaitForSeconds(0.1f);

            // waiting for answer
            while(_isWaitingAnswer) {
                _isWaitingAnswer = false;
                _isWaitingQuestion = true;
                yield return wait3sec;
            }

            while(conversation.tts.audioSource.isPlaying)
                yield return wait;

            // waiting for question
            if(_isWaitingQuestion)
                conversation.getQuestion();
            while(_isWaitingQuestion) {
                _isWaitingQuestion = false;
                yield return wait3sec;
            }

            while(conversation.tts.audioSource.isPlaying)
                yield return wait;

            // waiting for start
            while(_isWaitingInterviewer) {
                _isWaitingInterviewer = false;
                yield return wait3sec;
            }

            while(conversation.tts.audioSource.isPlaying)
                yield return wait;

            if(_isStartConversation) {
                print("micRecording");
                //_isWaitingInterviewer = true;

                if (!microphoneRecord.IsRecording)
                {
                    _stream.StartStream();
                    microphoneRecord.StartRecord();
                }
                else
                    microphoneRecord.StopRecord();
            } else {
                print("interview quited during micRecording");
                microphoneRecord.StopRecord();
            }
        }
    
        private void OnRecordStop(AudioChunk recordedAudio)
        {
            //buttonText.text = "Record";
        }
    
        private void OnResult(string result)
        {
            //text.text = result;
            //UiUtils.ScrollDown(scroll);
        }
        
        private void OnSegmentUpdated(WhisperResult segment)
        {
            print($"Segment updated: {segment.Result}");
        }
        
        private void OnSegmentFinished(WhisperResult segment)
        {
            print($"Segment finished: {segment.Result}");
        }
        
        private void OnFinished(string finalResult)
        {
            vadIndicatorImage.color = Color.white;
            if(!_isStartConversation) {
                microphoneRecord.StopRecord();
                print("Interview quited safely.");
                return;
            }
            print("Stream finished!");
            print($"Final result: {finalResult}");
            conversation.sendAnswer(finalResult);
            _isWaitingAnswer = true;
            if(_isStartConversation)
                StartCoroutine(micRecording());
        }
    }
}
