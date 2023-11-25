let sendfilebtn = document.querySelector(".main__send-button");

sendfilebtn.addEventListener("click", function (e) {
    e.preventDefault();
    
    let text = document.getElementById("main__textarea").value;
    
    let formdata = new FormData();
    formdata.append('text', text);

    if (typeof text != 'undefined') {
        document.getElementById("main__result-area").innerHTML = `
            <div class="img__container">
                <img class="img__loading" src="static/img/loading.png" alt="loading">
            </div>

            <style>
                .img__container {
                    flex: 1;
                    width: 100%;
                    height: 100%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }

                .img__loading {
                    width: 100px;
                    height: 100px;
                    animation: rotate_img 0.5s linear infinite;
                }

                @keyframes rotate_img {
                    0% {
                      transform: rotate(0deg);
                    }
                    100% {
                      transform: rotate(360deg);
                    }
                  }
            </style>
        `;
        

        fetch("/api/text",
        {
            method: "POST",
            body: formdata,
            /*headers: {
                'Content-Type': 'multipart/form-data'
            }*/
        })
        .then( response => {
            response.json().then(function(data) {

                var encodedImage = data.image_url;
                var decodedImage = atob(encodedImage);
                var byteCharacters = decodedImage.split('').map(char => char.charCodeAt(0));
                var byteArray = new Uint8Array(byteCharacters);
                var imageType = 'image/jpeg';
                var blob = new Blob([byteArray], { type: imageType });
                var imageUrl = URL.createObjectURL(blob);


                var group = data.group;
                var topic = data.topic;
                var executor = data.executor;
                var spell = data.spell;
                var summarization = data.summarization;
                var loc = data.loc;

                

                // var executor = data.executor;
                // var group = data.group;
                // var subject = data.subject;
                // var corrected = data.corrected;
                // var main = data.main;
                // var location = data.location;


                document.getElementById("main__result-area").innerHTML = `
                    <p class="result-text result-text_title">Исполнитель:</p>
                    <p class="result-text">` + executor + `</p>
                    <p class="result-text result-text_title">Группа тем:</p>
                    <p class="result-text">` + group + `</p>
                    <p class="result-text result-text_title">Тема:</p>
                    <p class="result-text">` + topic + `</p>

                    <div class="result-partition"></div>

                    <p class="result-text result-text_title">Локация:</p>
                    <p class="result-text">` + loc + `</p>
                    <p class="result-text result-text_title">Главная мысль:</p>
                    <p class="result-text">` + summarization + `</p>
                    <p class="result-text result-text_title">Исправленный текст:</p>
                    <p class="result-text">` + spell + `</p>

                    <div class="result-partition"></div>
                    
                    <p class="result-text result-text_title">Облако тэгов:</p>
                    <img class="result-img" src=` + imageUrl + ` alt="Изображение">

                    <style>
                    .result-text {
                        color: #ddd;
                        font-size: 16px;
                    }

                    .result-text_title {
                        color: #eee;
                        font-weight: bold;
                        margin-top: 20px;
                    }

                    .result-partition {
                        width: 100%;
                        border-bottom: 1px solid #eee;
                        margin: 10px 0 30px 0;
                    }

                    .result-img {
                        width: 90%;
                        margin: 20px 5% 0 5%;
                    }
                    </style>
                `;  

            });
        })
        .catch( error => {
            alert(error);
            console.error('error:', error);
        });
        
    }
    else {
        
    }
});