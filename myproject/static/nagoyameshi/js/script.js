
// ページが読み込み完了したときに発動
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


});


