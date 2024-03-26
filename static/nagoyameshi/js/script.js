
// ページが読み込み完了したときに発動
//restaurant\detail.htmlの予約日時選定
window.addEventListener("load" , () => {

    const today   = new Date();
    const year    = String(today.getFullYear());
    const month   = ("0" + String(today.getMonth() + 1) ).slice(-2);
    const day     = ("0" + String(today.getDate()) ).slice(-2);
    const hour    = ("0" + String(today.getHours()) ).slice(-2);
    //const minute  = ("0" + String(today.getMinutes()) ).slice(-2);

    const date    = year + "-" + month + "-" + day + " " + hour + ":00";


    const config  = { 
        enableTime: true,
        dateFormat: "Y-m-d H:i",
        locale: "ja",
        defaultDate: date,
    }
    // f 第一引数：発動させたい要素、第二引数：設定
    flatpickr(".flatpickr_datetime_form", config);

//DjangoMessageFrameWorkの削除機能 (素のJavaScriptに書き換え。)
const notify_deletes    = document.querySelectorAll(".notify_message_delete");
for (let notify_delete of notify_deletes ){
    // クリックされたとき、その要素の親要素.notify_messageを削除する。
    notify_delete.addEventListener("click", (event) => {
        // クリックされたバツボタンの親要素を削除する。
        event.currentTarget.closest(".notify_message").remove();
    });
}

//5秒経ったら自動的に消す。
setTimeout( () => {
    const messages  = document.querySelectorAll(".notify_message");
    for (let message of messages){
        message.remove();
    }
}, "5000");


});

//contact.htmlの送信ボタンクリック後
window.onload = function() {
const button = document.getElementById('button');

button.addEventListener('click',()=>{
    const result = window.confirm('送信してもよろしいですか？');

    if ( result ){
        console.log('送信しました');
    }

    else{
        console.log('問い合わせ内容を再度ご確認ください');
    }

});
};

