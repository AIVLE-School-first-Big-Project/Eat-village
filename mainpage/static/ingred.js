/* 반응형 사이트에서 작은 화면 일때 메뉴 버튼 클릭 시 메뉴 리스트가 나옴*/
const togglebtn = document.querySelector('.navbar_togglebtn');
const menu = document.querySelector('.navbar_menu');
const search = document.querySelector('.navbar_right');

togglebtn.addEventListener('click', () => {
    menu.classList.toggle('active');
    search.classList.toggle('active');
});

/* 버튼 클릭 시 카메라 접근 후 영상 촬영 */
function cameraAccess() {
    var video = document.querySelector("#videoElement");
     
    if (navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
          video.srcObject = stream;
        })
        .catch(function (err0r) {
          console.log("카메라 접근이 안되거나 없습니다!");
        });
    }
}

/* 재료 수정 페이지에서 재료 추가, 삭제 기능 */
const ingredInput = document.querySelector('.ingred-input');
const ingredList = document.querySelector('.ingred-list');

let ingreds = [];

const setIngreds = (newIngreds) => {
  ingreds = newIngreds;
}

const getAllIngreds = () => {
  return ingreds;
}

const appendIngreds = (text) => {
  const newIngreds = getAllIngreds().concat({content: text});
  setIngreds(newIngreds);
  paintIngreds();
}

const deleteIngred = (ingredContent) => {
    const newIngreds = getAllIngreds().filter(ingred => ingred.content !== ingredContent);
    setIngreds(newIngreds);
    paintIngreds();
}

const paintIngreds = () => {
  ingredList.innerHTML = null;
  const allIngreds = getAllIngreds();

  allIngreds.forEach(ingred => {
    const ingredItem = document.createElement('li');
    ingredItem.classList.add('ingred-item');

    const ingredName = document.createElement('div');
    ingredName.classList.add('ingred');
    ingredName.innerText = ingred.content;

    const delBtn = document.createElement('button');
    delBtn.classList.add('delbtn');
    delBtn.addEventListener('click', () => deleteIngred(ingred.content));
    delBtn.innerHTML = 'X';

    ingredItem.appendChild(ingredName);
    ingredItem.appendChild(delBtn);
    ingredList.appendChild(ingredItem);
  })
}

const init = () => {
  ingredInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      appendIngreds(e.target.value);
      ingredInput.value = '';
    }
  })
}

init();