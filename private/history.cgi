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
<TITLE>�����ӥ����Ѥ��Ф���ɾ��������: ����������</TITLE>
<style type="text/css">
table {width: 880px; font-size: 0.8em; text-align: center;}
div#container {width: 880px; margin-left: auto; margin-right: auto; font-size: 1.5em}
</style>
</HEAD>
<BODY>
<div id="container">
<div id="header">
�桼��: $user_name &nbsp;&nbsp; 
<a href='./top.cgi'>Top�ڡ���</a>&nbsp;&nbsp;
<a href='./history_delete.cgi'>�������Ƥκ��</a>
</div>
<hr>
<br>
<h3>����������</h3>
<br>
<table class="table" border="4">
 <tr><th>ˬ��Ź��̾</th><th>ˬ�����</th><th>���ѿͿ�</th><th>���Ѳ��</th><th>��������</th><th>���ԤȤΥ���å�</th><th>�����­��</th><th>��ˬ��ո�</th><th>�����ո�</th><th>���Ѷ��</th></tr>
 !;
    &Log;
    print qq!
</table>
<br>
<hr>

<div align="right">
<a href="./history-all.cgi">���Ƥβ������Ƥ�ɽ��</a>
<br>
</div> 
<br><br>
<div align="right" style="font-size:0.5em">
���������Ƥ�ȿ�Ǥ���Ƥ��ʤ����ϡ��ڡ����ι�����ԤʤäƤ���������
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
    <IN>; # 1�� �Ŀ;��󵭺���ʬ(Name)
    @data = <IN>;
    close(IN);
    @data = reverse(@data);
    if($data[0]){
    foreach(@data){
	chomp($_);
	@subdata = split(/\t/, $_);
	print "<tr><td>$subdata[2]</td><td>$subdata[3]</td><td>$subdata[4]</td><td>$subdata[5]</td><td>$subdata[6]</td><td>$subdata[8]</td><td>$subdata[9]</td><td>$subdata[10]</td><td>$subdata[11]</td><td>$subdata[7]��</td></tr>\n";
    }
}else{}
}
