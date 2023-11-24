let sendfilebtn = document.querySelector(".main__send-button");

sendfilebtn.addEventListener("click", function (e) {
    e.preventDefault();
    
    let text = document.getElementById("main__textarea").value;
    
    let formdata = new FormData();
    formdata.append('text', text);

    if (typeof text != 'undefined') {
        // document.getElementById("download").innerHTML = `
        //     <div class="img__container">
        //         <img class="img__loading" src="static/img/loading.png" alt="loading">
        //     </div>

        //     <style>
        //         .img__container {
        //             flex: 1;
        //             width: 100%;
        //             height: 100%;
        //             display: flex;
        //             align-items: center;
        //             justify-content: center;
        //         }

        //         .img__loading {
        //             width: 100px;
        //             height: 100px;
        //             animation: rotate_img 0.5s linear infinite;
        //         }

        //         @keyframes rotate_img {
        //             0% {
        //               transform: rotate(0deg);
        //             }
        //             100% {
        //               transform: rotate(360deg);
        //             }
        //           }
        //     </style>
        // `;
        

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

                var executor = data.executor;
                var group = data.group;
                var subject = data.subject;


                document.getElementById("main__result-area").innerHTML = `
                    <p class="result-text result-text_title">Исполнитель:</p>
                    <p class="result-text">` + executor + `</p>
                    <p class="result-text result-text_title">Группа тем:</p>
                    <p class="result-text">` + group + `</p>
                    <p class="result-text result-text_title">Тема:</p>
                    <p class="result-text">` + subject + `</p>

                    <style>
                    .result-text {
                        color: #ddd;
                        font-size: 16px;
                    }

                    .result-text_title {
                        color: #fff;
                        font-weight: bold;
                        margin-top: 20px;
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