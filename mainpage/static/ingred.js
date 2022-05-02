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