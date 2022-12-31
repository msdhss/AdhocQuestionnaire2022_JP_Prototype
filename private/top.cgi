#!/usr/bin/perl
require "cgi-lib.pl";
require "jcode.pl";
&ReadParse; # $in{'var'} is included form data

# http://www.msdhss.sakura.ne.jp/adhocQuestionnaire2022_jp_prototype/private/top.cgi

# login user name: 環境変数の取得
$user_name = $ENV{'REMOTE_USER'};
$address = $user_name.".log";

# facesheet
open(IN, "./user/$address") or die "cannot open\n";
  @data = <IN>;
close(IN);
  if($data[0]){
    $face = "あり";
  }else{
    &Facesheet;
    exit;
  }

# Web表示とアンケートの送信と分析
&Print_HTML;

# HTML
sub Print_HTML
{
  print <<END;
Content-type: text/html

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">

<HTML>

<HEAD>
<META Http-Equiv="Content-Type" Content="text/html; charset=euc-jp">
<TITLE>
飲食施設におけるサービス利用に関するアンケート調査
</TITLE>
  <style type="text/css">
    div#container {width: 700px; margin-left: auto; margin-right: auto;}
    div#container td {font-size: 1.3em}
    div#header {
      width: 700px; 
        margin-left: auto; margin-right: auto; font-size: 1.3em}
    div#contents {
      width: 600px; 
        margin-left: auto; margin-right: auto; font-size: 1.3em}
    .line-space1 {line-height: 130%;}
    .line-space2 {line-height: 170%;}
  </style>
</HEAD>

<BODY>
<div id="container">

<div id='header'>
ユーザ: $user_name &nbsp;&nbsp; 
<hr>
<span class="line-space1">
飲食施設におけるサービス利用に関するアンケート調査 <br>
</span>
<hr>
</div>

<div id="contents">
<br>
<ol>
<li><b><a href='./description.cgi'>調査概要</a></b>
（最初に一読してください）<br><br>
<li><b><a href='./makeQuestionnaire.cgi'>
アンケートに回答する</a></b><br>
<br><br>
</ol>
<hr>
<font size="4">
<b><a href='./history.cgi'>
  回答内容の確認</a></b><br><br>
<b><a href='./history_delete.cgi'>
  回答内容の削除</a></b>
</font>
<hr>
</div>
<br>
<hr>
</div>

</BODY>
</HTML>
END
	exit;
}

sub Facesheet{
# user name 
$user_name = $ENV{'REMOTE_USER'};
$dir = $user_name.".log";

# date
my($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) 
  = localtime(time);
$year += 1900;
$mon += 1;
my($date) 
  = sprintf("%04d/%02d/%02d %02d:%02d",$year,$mon,$mday,$hour,$min);

# in the case of putting ANSER  
if($in{"answer"}){
    # file open
    $name = $user_name;
    $i = $name.".log";
    open(USER1, ">./log/$i");
    open(USER2, ">./user/$i");
    open(IND, ">./answer/$i");
    open(IND2, ">./post/$i");
    open(IND3, ">./pre/$i");
    # management
    print FILE "$name:$pass\n";
    print USER1 "$name:$pass\n";
    @answer = ();
    push(@answer,$name); # 0: user_name
    push(@answer,0); # 1: 回数
    push(@answer,0); # 2: 回数
    push(@answer,0); # 3: 回数
    push(@answer,0); # 4: 回数
    print USER2 join("\t",@answer)."\n";
    print IND $name."\n";
    print IND2 $name."\n";
    print IND3 $name."\n";
    # file close
    close(FILE);
    close(USER1);
    close(USER2);
    close(IND); 
    close(IND2);
    close(IND3);
    &Print_HTML_Facesheet; 
  }

#########################################################################
# Facesheet_HTML
#########################################################################
print "Content-type: text/html\n\n";
#タイトル
print qq!
<HTML>
<HEAD>
  <META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
  <TITLE>ユーザの設定</TITLE>
<style>
div#container{width: 750px; margin-left: auto; margin-right: auto; font-size: 1.3em}
div#container td {font-size: 1.3em}
div#header{width: 750px; margin-left: auto; margin-right: auto; font-size: 1.3em}
</style>
</HEAD>

<BODY>
<div id=container>
${&UserName}
<CENTER>
<FORM ACTION="top.cgi" METHOD="POST">
<br>
	<P>
		<INPUT TYPE="hidden" NAME="a4" VALUE="0">
		<INPUT TYPE="hidden" NAME="count" VALUE="$count">
		<INPUT TYPE="hidden" NAME="number" VALUE="$number">
		<INPUT TYPE="submit" NAME="answer" VALUE="ユーザを作成します" style="font-size: 1em">
	</FORM>
        <p>
		</CENTER>
</div>
</BODY>
</HTML>
!;
    }

# top bar
sub UserName
{
    print "<div id='header'>";
    print "ユーザ : $user_name　";
    print "<hr>";
    print "</div>";
}
# サービスの初回利用か、繰り返し利用可の判別
sub DivideFirst
{
    print "Content-type: text/html\n\n";
    print qq!
	<html>
	 <head>
	  <META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
	  <titel>初めての利用 or 複数の利用</title>
	 </head>
	 <body>
	  <form action="evaluation.cgi" method="post">
	  初めての利用<INPUT TYPE="submit" NAME="first" VALUE="1"><br>
	  初めてではない<INPUT TYPE="submit" NAME="first" VALUE="2"><br>
	  </form>
	 </body>
	</html>
	!;
    exit;
}
#
# エラーページの表示 
#
sub Print_Error
{
	my($error) = @_;
	print "Content-type: text/html\n\n";
	print qq!
	<HTML>
	<HEAD>
		<META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
		<TITLE>エラーが発生しました</TITLE>
	</HEAD>
	<BODY>
		<BR>
		<B>エラーが発生しました</B>
		<P>
		$error<BR>
		<P>
		サイト運営者にお問い合せ下さい。<BR>
	</BODY>
	</HTML>
	!;
	exit;
}

# 完了ページの表示 
sub Print_HTML_Facesheet
{
    print "Content-type: text/html\n\n";
    print qq!
<HTML>
<HEAD>
<META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
<TITLE>データの送信</TITLE>
</HEAD>
<BODY>
<BR>
<center>
<br>
<b>データの送信が完了しました。</b>
<br>
<b>自動的に<a href="./top.cgi">Topページ</a>へ移ります。</b>
<br>
<meta http-equiv="refresh" content=" 2 ;url= ./top.cgi"> 
</center>
		<P>
	</BODY>
	</HTML>
	!;
	exit;
}

