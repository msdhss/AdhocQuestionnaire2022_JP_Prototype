#!/usr/bin/perl
require "cgi-lib.pl";
require "jcode.pl";
&ReadParse; # form data �μ������ơ�$in{}�˼�Ǽ
# �Ķ��Խ��μ���
$user_name = $ENV{'REMOTE_USER'};
# Webɽ���ȥ��󥱡��Ȥ�������ʬ��
    print "Content-type: text/html\n\n";
    print qq!
    <HTML>
    <HEAD>
    <META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
    <TITLE>Dynamic Evaluation</TITLE>
    </HEAD>
    <BODY>
    <div align="left">${UserName()}</div>
    <hr>
    !;
&Print_Thanks;
    print qq!
	</BODY>
	</HTML>
    !;
	exit;
# end
##############################
### �桼���͡���
##############################
sub UserName
{
    print "�桼�� : $user_name";
    print "����<a href='./mobile_top.cgi'>Top</a>";
}
##############################
### �ǡ���ɽ��
#############################
sub Print_Thanks
{
    print qq!
<h2>���ޤǤ�ɾ��</h2>
	!;
# i file open
    $i = $user_name.".dat";
    open(IN, "./user/$i");
    <IN>; # line 1 throw
    @data = <IN>;
    close(IN);
    open(STORE, "./store_list.dat");
    @store = <STORE>;
    close(STORE);
    if(!$data[0]){ # $data[0] ��ɾ���ǡ������ʤ����
	print "�ޤ�ɾ���򤷤Ƥ��ޤ���\n";
    }else{ # $data[0] ��ɾ���ǡ�����¸�ߤ�����
	foreach(@data){
	    chomp();
	    @subdata = split(/\t/);
	    print "����Ź��̾: $subdata[0]�����Ѳ�� $subdata[1]�����Ѥ������� $subdata[2]������ $subdata[4]�����Ԥ���Τ��� $subdata[5]����­�� $subdata[6]�� ������: $subdata[7]������: $subdata[8] <br>\n";
	}
    }
}
