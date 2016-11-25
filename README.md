# mytest
刷屏
建议用谷歌浏览器 打开花椒直播
按F12
点Console标签
把下面的代码贴进去  回车

``` javascript
function mysend(){
	// 想说的好话
	var say = [" 我好喜欢你哦","最美","真棒","是花椒最美主播"," 我太喜欢你了","是我女神"," 我真的好喜欢你哟"," 么么哒"]; 
	var real_say = new Array();
	for(var i = 0; i< say.length; i++) {
		// 加上当前主播名字
		real_say.push($("div#author-info h3:first").text() + say[i]);
	}
	//加上场控的话
	real_say.push("欢迎来到~央音琵琶专业~直播间❤❤");
	// 随机选一条
	var text = real_say[Math.floor(Math.random() * real_say.length)];
	// 填到输入框
	$("input[name='message']").val(text);
	// 发送
	$(".tt-type-submit").click();
	// 等1000-1200 毫秒 再次发送
	var num = Math.random() * 200 + 1000;
	window.setTimeout("mysend()", num); 
};
mysend();
```
