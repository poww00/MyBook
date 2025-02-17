function getArticleNo() {
    const location = window.location.href;
    const url = new URL(location);
    const articleNo = url.pathname.split('/')[2];

    return articleNo;
}

function displayArticle(categoryData, titleData, authorData, descData, priceData, imageURL) {
    const titleSection = document.querySelector('#article_title_div');
    const descSection = document.querySelector('#article_desc_div');
    const imageFigure = document.querySelector('#article_image_fig');

    let authToken = window.sessionStorage.getItem("authtoken");
    let userName = window.sessionStorage.getItem("username");
    // 로그인 여부, 게시물 생성자 여부 확인
    let isEdittable = authToken && username === authorData;

    let titleDiv = document.createElement('div');
    titleDiv.className = isEditable ? 'col-5' : 'col-7';
    // titleDiv.className = 'col-7':
    titleDiv.id = 'article_title';
    title = `[${categoryData}] ${titleData} - 가격 ${priceData}원`;
    titleDiv.appendChild(document.createTextNode(title));
    titleSection.appendChild(titleDiv);

    let authorDiv = document.createElement('div');
    authorDiv.className = 'col-2';
    authorDiv.style = 'text-align: center';
    authorDiv.id = 'article_author';
    authorDiv.appendChild(document.createTextNode(authorData));
    titleSection.appendChild(authorDiv);

    if (isEditable) {
        let editButtonsDiv = document.createElement('div');
        editButtonsDiv.className = 'col-2 text-center';
        const buttons = `<button type="button" class="btn btn-primary btn-sm" id="edit_button">수정</button>
        <button type="button" class="btn btn-secondary btn-sm" id="delete_button">삭제</button>`;

        editButtonsDiv.innerHTML = buttons;
        titleSection.appendChild(editButtonsDiv);

        // 수정 버튼 클릭 : 게시물 수정 페이지로 이동
        function onClickEditBtnHandler() {
            const articleNo = getArticleNo();

            let editPage = '/update_article/' + articleNo;
            window.location.replace(editPage);
        }
        // 삭제 버튼 클릭 : 게시물 삭제 실행여부 확인
        function onDeleteButtonHandler() {
            const articleNo = getArticleNo();

            // 게시물 삭제 실행, 취소 버튼 생성
            const confirmDeletionDiv = document.querySelector('#confirm_deletion_div');
            const confirmDeletionButtons = `<button type="button" class="btn btn-danger btn-sm" id="confirm_button">삭제</button>
            <button type="button" class="btn btn-primary btn-sm" id="cancel_button">취소</button>`;

            confirmDeletionDiv.innerHTML = confirmDeletionButtons;

            // 삭제 실행된 게시물을 서버에 삭제 요청
            function onConfirmDeletionHandler() {
                let headerData = new Headers();
                let authToken = sessionStorage.getItem("authtoken");
                if (authToken) {
                    headerData.set("authtoken", authToken);
                    fetch('/api/article/delete', {
                        method: 'POST',
                        headers: headerData,
                        body: formData
                    }).then((response) => {
                        return response.json();
                    }).then((resBody) => {
                        let url = '/home';
                        window.location.replace(url);
                    }).catch((error) => {
                        console.log('[Error]delete_article.onConfirmDeletionHandler:', error);     
                    });
                }
                // 삭제 취소
                function onCancelHandler() {
                    confirmDeletionDiv.innerHTML = '';
                }
                // 삭제확인, 취소 버튼 생성 및 기능 수행 함수와 연결
                const confirmButton = document.querySelector('#confirm_button');
                const cancel_button = document.querySelector('#cancel_button');
                
                confirmButton.addEventListener('click', onConfirmDeletionHandler);
                cancel_button.addEventListener('click', onCancelHandler);
            }
            // 수정, 삭제버튼 생성 및 기능 수행 함수와 연결
            const editButton = document.querySelector('#edit_button');
            const deleteButton = document.querySelector('#delete_button');

            editButton.addEventListener('click', onClickEditBtnHandler);
            deleteButton.addEventListener('click', onDeleteButtonHandler);
        }
        // 상품 내용 게시 요소 생성
        let descDiv = document.createElement('div');
        descDiv.className = 'col-9';
        descDiv.id = 'article_desc';
        descDiv.appendChild(document.createTextNode(descData));
        descSection.appendChild(descDiv);

        // 상품 이미지 게시 요소 생성
        if (imageURL) {
            let image = document.createElement('img');
            image.src = imageURL;
            image.className = 'figure-img img-fluid rounded';
            imageFigure.appendChild(image);
        }
    }

    function getArticle() {
        const articleNo = getArticleNo ();
        let formData = new FormData();
        formData.append("articleNo", articleNo);

        fetch('/api/article/display', {
            method: 'POST',
            body: formData
        }).then((response) => {
            return response.json();
        }).then((resBody) => {
            // console.log('getArticle().resBody:', resBody);
            let article = resBody["article"];
            displayArticle(article["category"], article["picture"]);

        }).catch((error) => {
            console.log('[Error]getArticle():', error);
        });
    }
    window.addEventListener('load', getArticle);
}