function audio() {
    document.getElementById('btn_audio').currentTime = 0; //連続クリックに対応
    document.getElementById('btn_audio').play();
}

const startBtn = document.querySelector('#start-btn');
const stopBtn = document.querySelector('#stop-btn');
const resultDiv = document.querySelector('#result-div');
const responseDiv = document.querySelector('#response-div');

// 評価実験用
// const descriptionBtn = document.querySelector('#description-btn');
// const answerBtn = document.querySelector('#answer-btn');

// const eventDiv = document.querySelector('#event-div');

// descriptionBtn.onclick = () => {
//     let description_text = 'こんにちは。私は、地域情報音声アシスタントアプリ、「ノノ」です。私は地域情報を提供し、みなさんの生活をサポートします。何か知りたいことはありますか？';
//     const uttr = new SpeechSynthesisUtterance(description_text);
//     speechSynthesis.speak(uttr);
// }

// answerBtn.onclick = () => {
//     const uttr = new SpeechSynthesisUtterance(responseDiv.innerHTML.replace(/<br>/g, "。"));
//     speechSynthesis.speak(uttr);
// }
// 

const SpeechRecognition = webkitSpeechRecognition || SpeechRecognition;
let recognition = new SpeechRecognition();

recognition.lang = 'ja-JP';
recognition.interimResults = true;
recognition.continuous = true;

let finalTranscript = ''; // 確定した(黒の)認識結果
let count = 1;
let isFinal_flag = false;
recognition.onresult = (event) => {
    // console.log('eventの中身:', event);
    let interimTranscript = ''; // 暫定(灰色)の認識結果
    for (let i = event.resultIndex; i < event.results.length; i++) {
        let transcript = event.results[i][0].transcript;

        // eventDiv.innerHTML += count + ':' + transcript + '<br>' + event.results[i].isFinal + '<br><br>';

        if (count == 1 && event.results[i].isFinal) {
            isFinal_flag = true;
        }
        if (isFinal_flag) {
            finalTranscript = transcript;
        } else if (event.results[i].isFinal) {
            finalTranscript += transcript;
        } else {
            interimTranscript = transcript;
        }
    }
    resultDiv.innerHTML = finalTranscript + '<i style="color:#ddd;">' + interimTranscript + '</i>';
    count += 1;
}

startBtn.onclick = () => {
    // 前回のやりとりをリセット
    finalTranscript = '';
    resultDiv.innerHTML = '';
    responseDiv.innerHTML = '';
    audio();
    recognition.start();
}

const csrfToken = document.getElementById('csrf-token').value;

stopBtn.onclick = () => {
    recognition.stop();

    setTimeout(function () {
        console.log('送信するテキスト:', finalTranscript);

        // finalTranscriptを送信
        fetch('/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken  // DjangoのCSRFトークンを設定
            },
            body: JSON.stringify({ speech_text: finalTranscript })
        })
            .then(response => {
                // レスポンスがJSONでない場合のエラーハンドリング
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('サーバーからの応答:', data);
                // 返答を表示
                responseDiv.innerHTML = data.response_text;

                const uttr = new SpeechSynthesisUtterance(data.response_text.replace(/<br>/g, "。"));
                speechSynthesis.speak(uttr);
            })
            .catch(error => {
                console.error('エラー:', error);
            });
    }, 1000);
}

resultDiv.addEventListener('input', () => {
    finalTranscript = resultDiv.innerText;
});

const clickBtn = document.getElementById('click-btn');
const popupWrapper = document.getElementById('popup-wrapper');
const close = document.getElementById('close');

// ボタンをクリックしたときにポップアップを表示させる
clickBtn.addEventListener('click', () => {
    popupWrapper.style.display = "block";
    document.body.style.overflow = 'hidden'; // 背景のスクロールを無効化
});

// ポップアップの外側又は「x」のマークをクリックしたときポップアップを閉じる
popupWrapper.addEventListener('click', e => {
    if (e.target.id === popupWrapper.id || e.target.id === close.id) {
        popupWrapper.style.display = 'none';
        document.body.style.overflow = 'auto'; // 背景のスクロールを再度有効化
    }
});