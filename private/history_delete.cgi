#!/usr/bin/perl
require "cgi-lib.pl";
require "jcode.pl";

&ReadParse; # related to cgi-lib.pl
$user_name = $ENV{'REMOTE_USER'};

# Delete
if($in{'mode'} eq "del"){
    if($in{'id'}){ 
    $delid = $in{'id'};
    open(IN, "./answer/$user_name.log") or die "cannot open\n";
    @data = <IN>;
    close(IN);
    $i = 0;
    foreach(@data){
	chomp $_;
	@subdata = split(/\t/, $_);
	$id_data[$i] = $subdata[1];
	$i++;
    }
    open(IN, "./answer/$user_name.log") or die "cannot open\n";
      @data = <IN>;
    close(IN);
    open(OUT, ">./answer/$user_name.log");
    $i = 0;
    foreach(@data){
	if($id_data[$i] =~ /($delid)/){
	    $i++;
	}else{
	print OUT $_;
	$i++;
    }
    }
    close(OUT);
    &Print_Thanks;
}
}
&Print_List;
# 
sub Print_List
{
    print "Content-type: text/html\n\n";
    print qq!
<HTML>
<HEAD>
<META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
<TITLE>�������ܤκ��</TITLE>
<style type="text/css">
a {color: #017acd}
table {width: 800px; font-size: 0.8 em; text-align: center;}
div#container {width: 880px; margin-left: auto; margin-right: auto; font-size: 1.5em}
</style>
</HEAD>

<BODY>
<div id="container">
<div id="header">
�桼��: $user_name &nbsp;&nbsp; 
<a href='./top.cgi'>Top�ڡ���</a>&nbsp;&nbsp;  
<a href='./history.cgi'>�������Ƥγ�ǧ</a>
</div>
<hr>
<form action="history_delete.cgi" method="POST">

<div align="left">
<br>
<p>
<input type="hidden" name="mode" value="del">
<input type="submit" value="�����å��������ܤ�������" style="font-size: 1.0em">
</p>
<br>
</div>

<table class="table" border="4">
 <tr><th>��</th><th>ˬ��Ź��̾</th><th>ˬ�����</th><th>���ѿͿ�</th><th>���Ѳ��</th><th>��������</th><th>���ԤȤΥ���å�</th><th>�����­��</th><th>��ˬ��ո�</th><th>�����ո�</th><th>���Ѷ��</th></tr>
 !;
    open(IN, "./answer/$user_name.log") or die "Cannot open file\n";
    <IN>; # 1�� �Ŀ;��󵭺���ʬ
    @data = <IN>;
    close(IN);
    @data = reverse(@data);
    foreach(@data){
	chomp($_);
	@subdata = split(/\t/, $_);
	print "<tr><td><input type='radio' name='id' value='$subdata[1]' style='width: 35pt; height: 35pt'></td><td>$subdata[2]</td><td>$subdata[3]</td><td>$subdata[4]</td><td>$subdata[5]</td><td>$subdata[6]</td><td>$subdata[8]</td><td>$subdata[9]</td><td>$subdata[10]</td><td>$subdata[11]</td><td>$subdata[7]��</td></tr>\n";
    }
    print qq!
</form>
</table>
<br>
<hr>
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

# ��λ�ڡ�����ɽ�� 
sub Print_Thanks
{
    print "Content-type: text/html\n\n";
    print qq!
<HTML>
<HEAD>
<META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
<TITLE>�������ܤκ��</TITLE>
<style type="text/css">
  div#container{width: 750px; 
    margin-left: auto; margin-right: auto; font-size: 1.5em}
  div#container td {font-size: 1.5em; height: 55px}
  div#header{width: 750px; 
    margin-left: auto; margin-right: auto; font-size: 1.3em}
  span.note{font-size: 18px; line-height: 140%;}
  .line-space {line-height: 170%;}
</style>
</HEAD>
<BODY>
<BR>
<center>
<br>
<span class="line-space">
<b>�����å������������ܤκ������λ���ޤ�����</b><br>
<b>��ưŪ��<a href="./history_delete.cgi">�������ܤκ���ڡ���</a>�����ޤ���</b><br>
</span>
<meta http-equiv="refresh" content=" 2 ;url= ./history_delete.cgi"> 
</center>
		<P>
	</BODY>
	</HTML>
	!;
	exit;
}
