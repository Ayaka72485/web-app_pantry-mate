// ハンバーガーメニューをトグルする関数
function toggleMenu() {
    const menu = document.getElementById('side-menu');
    if (menu.style.display === 'block') {
        menu.style.display = 'none'; // メニューを非表示にする
    } else {
        menu.style.display = 'block'; // メニューを表示する
    }
    document.querySelector('.menu-btn').addEventListener('click', function() {
        document.querySelector('.side-menu').classList.toggle('open');
    });
    
}
