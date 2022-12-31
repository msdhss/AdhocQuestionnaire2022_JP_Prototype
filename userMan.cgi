#!/usr/bin/perl

# .../adhocQuestionnaire2022_JP_prototype/userMan.cgi
# .../adhocQuestionnaire2022_JP_prototype/login.cgi
# .../adhocQuestionnaire2022_JP_prototype/table.cgi
# test    1111

#########################################################################
# 初期化の手順(サーバー): 
#########################################################################
# 1. .usrs の中身を消去
# 2. user.csv の消去
# 3. private/userの中身を消去
# 4. private/answerの中身を消去
# 5. private/logの中身を消去
# ユーザの作成: 
# 1. user.csvの準備
# 確認箇所: 
# .usersの1行目に改行コードが入っているとtableが出せない
########################################################################

require "cgi-lib.pl";
require "jcode.pl";

&ReadParse; # related to cgi-lib.pl

&Print_Thanks;

sub Print_Thanks
{
    print "Content-type: text/html\n\n";
    print qq!
<HTML>
<HEAD>
<META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
<TITLE>サービス利用に対するアンケートサイト: ユーザー登録ページ</TITLE>
<style type="text/css">
table {width: 880px; font-size: 0.8em; text-align: center;}
div#container {width: 880px; margin-left: auto; margin-right: auto; font-size: 1.5em}
</style>
</HEAD>
<BODY>

<div id="container">
<hr>
user.csv file のアップロード<br>

<form action="./upload.cgi" method="POST" ENCTYPE="multipart/form-data">

<p>file <input type="file" name="uploadFile"></p>

<p><input type="submit" value="user.csvファイルのアップロード"></p>
</form>

<hr>

<br>
<h3>アップロードしたファイル内容</h3>
<br>
<table class="table" border="4">
 <tr><th>ユーザ名</th><th>パスワード</th></tr>
 !;
    Log();
    print qq!
</table>

<hr>

<h3>アップロードしたファイル内容でユーザ登録を行う</h3>
<FORM ACTION="./registration.cgi" METHOD="GET">
<INPUT TYPE="submit" VALUE="ユーザの登録">

<br>

<hr>

<br>

アンケート調査の<a href="./login.cgi">ログインページ</a>へ

</div>
</BODY>
</HTML>
	!;
	exit;
}

sub Log
{
    open(IN, "./user.csv") or die "Cannot open file\n";
      @data = <IN>;
    close(IN);
    if($data[0]){
    foreach(@data){
	chomp($_);
	@subdata = split(/,/, $_);
	print "<tr><td>$subdata[0]</td><td>$subdata[1]</td></tr>\n";
    }
}else{}
}
