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
<a href='./history.cgi'>Back</a>&nbsp;&nbsp;
</div>
<hr>
<br>
<h3>����������(���Ƥβ�������)</h3>
<br>
�桼��,����id,Ź��̾,��������,ˬ��Ϳ�,ˬ����,�����δ�����,���Ѷ��,�����δ��Ԥ��Ф��륮��å�,�����­��,��ˬ��ո�,�����ո�,������,��������,�ƥ��������Ȥ�����­��
<br>
 !;
    &Log;
    print qq!
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
	print "<hr>\n";
    foreach(@data){
    if($_){
        $_ =~ s/,/��/g;
        $_ =~ s/\t/,/g;
	print "$_<br><hr>\n";
    }else{}
    }
}
