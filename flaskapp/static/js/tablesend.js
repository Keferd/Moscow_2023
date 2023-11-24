let sendfilebtn = document.querySelector(".table__send-button");

sendfilebtn.addEventListener("click", function (e) {
    e.preventDefault();

    let input = document.getElementById("file");
    let file = input.files[0];
    
    let formdata = new FormData();
    formdata.append('file', file);
    formdata.append('test', 'test is work');

    if (typeof file != 'undefined') {

        document.getElementById("main__area").innerHTML = `
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




        fetch("/api/table",
        {
            method: "POST",
            body: formdata,
            /*headers: {
                'Content-Type': 'multipart/form-data'
            }*/
        })
        .then( response => {
            response.json().then(function(tabledata) {

                var table = new Tabulator("#main__area", {
                    data:tabledata,           //load row data from array
                    layout: "fitDataFill",
                    // layout: "fitColumns",     //fit columns to width of table
                    responsiveLayout:"false",  //hide columns that don't fit on the table
                    addRowPos:"top",          //when adding a new row, add it to the top of the table
                    history:true,             //allow undo and redo actions on the table
                    pagination:"local",       //paginate the data
                    paginationSize:20,         //allow 7 rows per page of data
                    paginationCounter:"rows", //display count of paginated rows in footer
                    // movableColumns:false,      //allow column order to be changed
                    // resizableRows: true, // Разрешить изменение высоты строк
                    // wordWrap: false, // Разрешить перенос текста в ячейках
                    columns:[                 //define the table columns
                        {title:"Исполнитель", field:"executor", width: "10%", formatter:"textarea",  editor:true},
                        {title:"Группа тем", field:"group", width: "10%", formatter:"textarea", editor:true},
                        {title:"Текст инцидента", field:"text", width: "60%", formatter:"textarea", editor:true},
                        {title:"Тема", field:"subject", width: "20%", formatter:"textarea", editor:true},
                    ],
                });
            
                
                document.getElementById("download-csv").addEventListener("click", function() {
                    table.download("csv", "data.csv");
                });

                document.getElementById("download-csv").disabled = false;
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