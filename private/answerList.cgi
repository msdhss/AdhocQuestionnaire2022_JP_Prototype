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
<TITLE>�����ӥ����Ф��륢�󥱡���Ĵ��������: ɾ������</TITLE>
<style type="text/css">
table {width: 880px; font-size: 0.8em; text-align: center;}
div#container {width: 880px; margin-left: auto; margin-right: auto; font-size: 1.5em}
</style>
</HEAD>
<BODY>
<div id="container">
<div id="header">
�桼��: $user_name &nbsp;&nbsp; 
<a href='../top.cgi'>Top</a> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<a href='./answerModify.cgi'>��������</a>
</div>
<hr>
$user_name ��ɾ������
<hr>
<table class="table" border="4">
 <tr><th>id</th><th>Ź��̾</th><th>��������</th><th>���Ѳ��</th><th>��������</th><th>�ץ���</th><th>���ϻ���</th></tr>
 !;
    &Log;
    print qq!
</table>
<hr>
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
    open(IN, "./user/$user_name.log") or die "Cannot open file\n";
    <IN>; # 1�� �Ŀ;��󵭺���ʬ
    @data = <IN>;
    close(IN);
    @data = reverse(@data);
    if($data[0]){
    foreach(@data){
	chomp($_);
	@subdata = split(/\t/, $_);
	print "<tr><td>$subdata[0]</td><td>$subdata[1]</td><td>$subdata[2]</td><td>$subdata[3]</td><td>$subdata[4]</td><td>$subdata[5]</td><td>$subdata[6]</td></tr>\n";
    }
}else{}
}
