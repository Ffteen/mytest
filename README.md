# mytest
花椒刷棒棒糖开挂
先充好值

用chrome浏览器 打开花椒直播相应的直播间

按F12

点Console标签

把下面的代码贴进去  回车


``` javascript
function giveGifts(num){
    if (num > 0){
        $("li[data-gid='1705318793']").click();
        $("#gift-bar > div.gift-operate.js-operate > div > button").click();
        var n = num - 1;
        console.log(n);
        window.setTimeout("giveGifts(" + n.toString() + ")", 10);  // 10毫秒一个 每秒100个
    } 
};
giveGifts(2333);  //括号里填多少就刷多少
```
