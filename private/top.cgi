#!/usr/bin/perl
require "cgi-lib.pl";
require "jcode.pl";
&ReadParse; # $in{'var'} is included form data

# http://www.msdhss.sakura.ne.jp/adhocQuestionnaire2022_jp_prototype/private/top.cgi

# login user name: �Ķ��ѿ��μ���
$user_name = $ENV{'REMOTE_USER'};
$address = $user_name.".log";

# facesheet
open(IN, "./user/$address") or die "cannot open\n";
  @data = <IN>;
close(IN);
  if($data[0]){
    $face = "����";
  }else{
    &Facesheet;
    exit;
  }

# Webɽ���ȥ��󥱡��Ȥ�������ʬ��
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
�������ߤˤ����륵���ӥ����Ѥ˴ؤ��륢�󥱡���Ĵ��
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
�桼��: $user_name &nbsp;&nbsp; 
<hr>
<span class="line-space1">
�������ߤˤ����륵���ӥ����Ѥ˴ؤ��륢�󥱡���Ĵ�� <br>
</span>
<hr>
</div>

<div id="contents">
<br>
<ol>
<li><b><a href='./description.cgi'>Ĵ������</a></b>
�ʺǽ�˰��ɤ��Ƥ���������<br><br>
<li><b><a href='./makeQuestionnaire.cgi'>
���󥱡��Ȥ˲�������</a></b><br>
<br><br>
</ol>
<hr>
<font size="4">
<b><a href='./history.cgi'>
  �������Ƥγ�ǧ</a></b><br><br>
<b><a href='./history_delete.cgi'>
  �������Ƥκ��</a></b>
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
    push(@answer,0); # 1: ���
    push(@answer,0); # 2: ���
    push(@answer,0); # 3: ���
    push(@answer,0); # 4: ���
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
#�����ȥ�
print qq!
<HTML>
<HEAD>
  <META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
  <TITLE>�桼��������</TITLE>
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
		<INPUT TYPE="submit" NAME="answer" VALUE="�桼����������ޤ�" style="font-size: 1em">
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
    print "�桼�� : $user_name��";
    print "<hr>";
    print "</div>";
}
# �����ӥ��ν�����Ѥ��������֤����ѲĤ�Ƚ��
sub DivideFirst
{
    print "Content-type: text/html\n\n";
    print qq!
	<html>
	 <head>
	  <META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
	  <titel>���Ƥ����� or ʣ��������</title>
	 </head>
	 <body>
	  <form action="evaluation.cgi" method="post">
	  ���Ƥ�����<INPUT TYPE="submit" NAME="first" VALUE="1"><br>
	  ���ƤǤϤʤ�<INPUT TYPE="submit" NAME="first" VALUE="2"><br>
	  </form>
	 </body>
	</html>
	!;
    exit;
}
#
# ���顼�ڡ�����ɽ�� 
#
sub Print_Error
{
	my($error) = @_;
	print "Content-type: text/html\n\n";
	print qq!
	<HTML>
	<HEAD>
		<META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
		<TITLE>���顼��ȯ�����ޤ���</TITLE>
	</HEAD>
	<BODY>
		<BR>
		<B>���顼��ȯ�����ޤ���</B>
		<P>
		$error<BR>
		<P>
		�����ȱ��ļԤˤ��䤤�礻��������<BR>
	</BODY>
	</HTML>
	!;
	exit;
}

# ��λ�ڡ�����ɽ�� 
sub Print_HTML_Facesheet
{
    print "Content-type: text/html\n\n";
    print qq!
<HTML>
<HEAD>
<META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
<TITLE>�ǡ���������</TITLE>
</HEAD>
<BODY>
<BR>
<center>
<br>
<b>�ǡ�������������λ���ޤ�����</b>
<br>
<b>��ưŪ��<a href="./top.cgi">Top�ڡ���</a>�ذܤ�ޤ���</b>
<br>
<meta http-equiv="refresh" content=" 2 ;url= ./top.cgi"> 
</center>
		<P>
	</BODY>
	</HTML>
	!;
	exit;
}

