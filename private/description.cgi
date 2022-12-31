#!/usr/bin/perl
require "cgi-lib.pl";
require "jcode.pl";
&ReadParse; # $in{'var'} is included form data

# http://www.msdhss.sakura.ne.jp/adhocQuestionnaire/private/top.cgi

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
<TITLE>調査概要</TITLE>
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
    .line-space2 {line-height: 115%;}
  </style>
</HEAD>

<BODY>
<div id="container">

<div id='header'>
ユーザ: $user_name &nbsp;&nbsp;<a href='./top.cgi'>Topページ</a>
<hr>
調査概要
<hr>
</div>

<div id="contents">
<p><span class="line-space1">
今回の調査は、皆様のサービス利用に関する行動の満足度を聴取することで、より良いサービス提案に繋げることを目的としております。
</span></p>
<p><span class="line-space1">
そこで、皆様には調査期間中に「xxxxx」のいずれかの店舗を、<font color="red">３店舗以上</font>利用していただきます。そして、利用した店舗で発生した行動をご自身で評価していただきます。
</span></p>
<p><span class="line-space1">
発生した行動に関して例を挙げて説明すると、例えば、カレー屋さんで食事をした際に発生する行動は･･･
</span></p>
発生した行動：　<br>
<br>
<span class="line-space1">
　　　　　　お店に入る<br>
　　　　　　席に着く<br>
　　　　　　サラダとカレーを注文する<br>
　　　　　　本を読みながら、注文を待つ<br>
　　　　　　サラダが運ばれてくる<br>
　　　　　　水を飲む<br>
　　　　　　サラダにドレッシングをかける<br>
　　　　　　サラダを食べる<br>
　　　　　　カレーが運ばれる<br>
　　　　　　カレーを食べる<br>
　　　　　　食べ終わり、水を飲む<br>
　　　　　　レジに向かう<br>
　　　　　　お会計をする<br>
　　　　　　お店を出る<br>
</span>
<p><span class="line-space1">
上記のような項目が考えられます。
</span></p>
<p><span class="line-space1">
このような項目を、ログイン後画面の「アンケートに回答する」内の専用のフォーマットにご記入いただき、その評価・コメントをしていただきます。
</span></p>
<p><span class="line-space1">
もし、サービス利用において<font color="blue">なにか満足した体験</font>や、<font color="green">なにか不満足な体験</font>といったものがありましたら、特にその体験が表現される様に行動のご記入をお願いいたします。
</span></p>
<p><span class="line-space1">
特筆すべき事項がなかったサービス体験項目の場合は、無理に評価やコメントをする必要はありません。率直なご回答をお願いいたします。
</span></p>
<p><span class="line-space1">
今回の調査では、皆様に「xxxx」のいずれかの店舗を、３回以上利用していただきます。すべて同じ業種・業態や、また、個人経営店舗でも大型店でも構いません。<u>ただ調査回数としては、かならず<font color="red">３店舗以上</font>の回答をお願いいたします。</u>
</span></p>
<p><span class="line-space1">
調査期間内であれば、回答内容の削除・再投稿は何度でも可能です。アンケートページの操作方法が分からない場合は、試験的に回答して、その回答内容を削除することも可能です。ただ基本的に、実際に訪問した店舗の評価の回答だけを、提出する回答として残すようにしてください。
</span></p>
</div>
<hr>
<font size="4">
<b><a href='./top.cgi'>
  トップページへ戻る</a></b><br><br>
</font>
<br>
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

