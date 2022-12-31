#!/usr/bin/perl

# .../adhocQuestionnaire2022_JP_prototype/userMan.cgi
# .../adhocQuestionnaire2022_JP_prototype/login.cgi
# .../adhocQuestionnaire2022_JP_prototype/table.cgi
# test    1111

#########################################################################
# ������μ��(�����С�): 
#########################################################################
# 1. .usrs ����Ȥ�õ�
# 2. user.csv �ξõ�
# 3. private/user����Ȥ�õ�
# 4. private/answer����Ȥ�õ�
# 5. private/log����Ȥ�õ�
# �桼���κ���: 
# 1. user.csv�ν���
# ��ǧ�ս�: 
# .users��1���ܤ˲��ԥ����ɤ����äƤ����table���Ф��ʤ�
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
<TITLE>�����ӥ����Ѥ��Ф��륢�󥱡��ȥ�����: �桼������Ͽ�ڡ���</TITLE>
<style type="text/css">
table {width: 880px; font-size: 0.8em; text-align: center;}
div#container {width: 880px; margin-left: auto; margin-right: auto; font-size: 1.5em}
</style>
</HEAD>
<BODY>

<div id="container">
<hr>
user.csv file �Υ��åץ���<br>

<form action="./upload.cgi" method="POST" ENCTYPE="multipart/form-data">

<p>file <input type="file" name="uploadFile"></p>

<p><input type="submit" value="user.csv�ե�����Υ��åץ���"></p>
</form>

<hr>

<br>
<h3>���åץ��ɤ����ե���������</h3>
<br>
<table class="table" border="4">
 <tr><th>�桼��̾</th><th>�ѥ����</th></tr>
 !;
    Log();
    print qq!
</table>

<hr>

<h3>���åץ��ɤ����ե��������Ƥǥ桼����Ͽ��Ԥ�</h3>
<FORM ACTION="./registration.cgi" METHOD="GET">
<INPUT TYPE="submit" VALUE="�桼������Ͽ">

<br>

<hr>

<br>

���󥱡���Ĵ����<a href="./login.cgi">������ڡ���</a>��

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
