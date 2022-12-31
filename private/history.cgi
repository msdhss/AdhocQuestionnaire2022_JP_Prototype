#!/usr/bin/perl
require "cgi-lib.pl";
require "jcode.pl";
&ReadParse; # related to cgi-lib.pl

$user_name = $ENV{'REMOTE_USER'};
&Print_Thanks;

sub Print_Thanks
{
    print "Content-type: text/html\n\n";
    print qq!
<HTML>
<HEAD>
<META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Cache-Control" content="no-cache">
<meta http-equiv="Expires" content="Thu, 01 Dec 1994 16:00:00 GMT">
<TITLE>サービス利用に対する評価サイト: 回答の履歴</TITLE>
<style type="text/css">
table {width: 880px; font-size: 0.8em; text-align: center;}
div#container {width: 880px; margin-left: auto; margin-right: auto; font-size: 1.5em}
</style>
</HEAD>
<BODY>
<div id="container">
<div id="header">
ユーザ: $user_name &nbsp;&nbsp; 
<a href='./top.cgi'>Topページ</a>&nbsp;&nbsp;
<a href='./history_delete.cgi'>回答内容の削除</a>
</div>
<hr>
<br>
<h3>回答の履歴</h3>
<br>
<table class="table" border="4">
 <tr><th>訪問店舗名</th><th>訪問時刻</th><th>利用人数</th><th>利用回数</th><th>事前期待</th><th>期待とのギャップ</th><th>総合満足度</th><th>再訪問意向</th><th>推薦意向</th><th>使用金額</th></tr>
 !;
    &Log;
    print qq!
</table>
<br>
<hr>

<div align="right">
<a href="./history-all.cgi">全ての回答内容の表示</a>
<br>
</div> 
<br><br>
<div align="right" style="font-size:0.5em">
※入力内容が反映されていない場合は、ページの更新を行なってください。
</div>

</div>
</BODY>
</HTML>
	!;
	exit;
}

#
# StoreSort
#
sub Log
{
    open(IN, "./answer/$user_name.log") or die "Cannot open file\n";
    <IN>; # 1行 個人情報記載部分(Name)
    @data = <IN>;
    close(IN);
    @data = reverse(@data);
    if($data[0]){
    foreach(@data){
	chomp($_);
	@subdata = split(/\t/, $_);
	print "<tr><td>$subdata[2]</td><td>$subdata[3]</td><td>$subdata[4]</td><td>$subdata[5]</td><td>$subdata[6]</td><td>$subdata[8]</td><td>$subdata[9]</td><td>$subdata[10]</td><td>$subdata[11]</td><td>$subdata[7]円</td></tr>\n";
    }
}else{}
}
