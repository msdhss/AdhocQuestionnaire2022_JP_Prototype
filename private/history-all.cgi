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
<a href='./history.cgi'>Back</a>&nbsp;&nbsp;
</div>
<hr>
<br>
<h3>回答の履歴(全ての回答内容)</h3>
<br>
ユーザ,回答id,店舗名,利用日時,訪問人数,訪問回数,事前の期待度,使用金額,事前の期待に対するギャップ,総合満足度,再訪問意向,推薦意向,コメント,入力日時,各アクションとその満足度
<br>
 !;
    &Log;
    print qq!
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
	print "<hr>\n";
    foreach(@data){
    if($_){
        $_ =~ s/,/，/g;
        $_ =~ s/\t/,/g;
	print "$_<br><hr>\n";
    }else{}
    }
}
