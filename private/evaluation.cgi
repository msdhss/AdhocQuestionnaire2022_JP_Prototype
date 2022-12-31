#!/usr/bin/perl
require "cgi-lib.pl";
require "jcode.pl";
&ReadParse; # $in{'name'} which are included form data
&WebQ; 
# main script
sub WebQ{
# user name ---------------------------------------------------------------------------
    $user_name = $ENV{'REMOTE_USER'};
    $dir = $user_name.".log";
    open(IN, "../../../../../user/$dir") or die "cannot open the file\n";
    <IN>;
    @data = <IN>;
    close(IN);
    $maxindex = @data - 1;
    if($data[0]){
	@subdata = split(/\t/,$data[$maxindex]);
	$id = $subdata[0];
	$find = index($id,"0");
	if($find == 0){
	    substr($id,0,1)="";
	    $find = index($id,"0");
	    if($find == 0){
		substr($id,0,1)="";
		$find = index($id,"0");
		if($find == 0){
		    substr($id,0,1)="";
		    $find = index($id,"0");
		    if($find == 0){
			substr($id,0,1)="";
			$find = index($id,"0");
			if($find == 0){
			    substr($id,0,1)="";
			}
		    }
		}
	    }
	}
	$id_answer = $id + 1;
    }else{
    $id_answer = 1;
    }
# store dir name ---------------------------------------------------------------------------
    @script_url = split(/\//,$ENV{"SCRIPT_NAME"});
    $store_region = "$script_url[3]"."$script_url[4]"."$script_url[5]"."$script_url[6]"; 
    $store_address = "$script_url[3]"."$script_url[4]"."$script_url[5]"."$script_url[6]"."$script_url[7]"; 
    open(DATA, "../servicelist_$store_region.dat") or die "cannot open the file\n";
    @data = <DATA>;
    close(DATA);
     foreach(@data){
	 chomp($_);
	 @subdata = split(/\t/, $_);
	 if($subdata[0] =~ /$store_address/){
	     $store_name = $subdata[2];
	 }
     }
# date ---------------------------------------------------------------------------
	my($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
	$year += 1900;
	$mon += 1;
	my($date) = sprintf("%04d/%02d/%02d %02d:%02d:%02d",$year,$mon,$mday,$hour,$min,$sec);
# in the case of putting ANSER  
    if($in{"answer"}){
	$id = sprintf("%06d", $id_answer);
	push(@answer,$id); #id6��
	push(@answer,$in{"a1"}); #ɾ������
	push(@answer,$store_address); #ɾ��Ź�ޥ�����
	push(@answer,$store_name); #ɾ��Ź��̾
	push(@answer,$in{"initial"}); #���Ѳ���ν�����
	push(@answer,$in{"count"}); #�ȡ�����ɾ����
	$money = $in{"a2_1"}.$in{"a2_2"}.$in{"a2_3"}.$in{"a2_4"}.$in{"a2_5"};
	$find = index($money,"0");
	if($find == 0){
	    substr($money,0,1)="";
	    $find = index($money,"0");
	    if($find == 0){
		substr($money,0,1)="";
		$find = index($money,"0");
		if($find == 0){
		    substr($money,0,1)="";
		    $find = index($money,"0");
		    if($find == 0){
			substr($money,0,1)="";
			$find = index($money,"0");
		    }
		}
	    }
	}
	push(@answer,$money);
	push(@answer,$in{"a3"});
	push(@answer,$in{"a4"});
	push(@answer,$in{"a5"});
	if($in{"a6"}){
	push(@answer,$in{"a6"});
    }else{
	push(@answer,"N/A");
    }
	push(@answer,$date);
	if(open(OFILE,">>answer.log")){
	   print OFILE join("\t",@answer)."\n";
	   close(OFILE); 
# idividual data
	   open(IND, ">>../../../../../user/$user_name.log");
	   print IND join("\t",@answer)."\n";
	   close(IND); 
			&Print_Thanks; 
		} else {
			&Print_Error("�ե�����ν���˼��Ԥ��ޤ�����");
		}
}
# How many times ---------------------------------------------------------------------------
    open(IN, "../../../../../user/$dir") or die "cannot open the file\n";
    <IN>;
    @data = <IN>;
    close(IN);
    @data = reverse @data;
    $count = 1;
    foreach(@data){
	if($_ =~ /$store_address/){
	    chomp($_);
	    @subdata = split(/\t/, $_);
	    $initial = $subdata[4];
	    $count = $subdata[5];
	    $count += 1;
	    last;
	}
    }
#--------------------------------------------------------------------------
# ���󥱡��ȥڡ����� HTML -------------------------------------------------
#--------------------------------------------------------------------------
print "Content-type: text/html\n\n";
#�����ȥ�
print qq!
<HTML>
<HEAD>
	<META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
	<TITLE>$store_name��ɾ��</TITLE>
<style>
div#container{width: 750px; margin-left: auto; margin-right: auto; font-size: 2em}
div#container td {font-size: 2em}
div#header{width: 750px; margin-left: auto; margin-right: auto; font-size: 2em}
</style>
</HEAD>
<BODY>
<div id=container>
${&UserName}
!;
    $question_num = 1;
print qq!
<CENTER>
<FORM ACTION="evaluation.cgi" METHOD="POST">
<TABLE>
<font size=4>
<tr><td><B>��$question_num��</B></td><td><b>�����ӥ�����/��������</b></td></tr>
<tr><td></td><td>
<select name="a1" style="width: 480px; font-size: 0.7em">
!;
    for($i=60;$i>0;$i--){
    $t = time;
    $t -= $i*60*60*24;
    my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($t);
    $year += 1900;
    $mon += 1;
    $list_date = sprintf("%04d/%02d/%02d", $year, $mon, $mday);
    @timerange = ('00:00-06:00','06:00-12:00','12:00-18:00','18:00-24:00');
    print  "<optgroup>\n";
    foreach $j (0 .. 3){
	print "<option value='$list_date $timerange[$j]'>$list_date $timerange[$j]</option>\n";
	}
    print  "/<optgroup>\n";
}
    $t = time;
    my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($t);
    $year += 1900;
    $mon += 1;
    $list_date_today = sprintf("%04d/%02d/%02d", $year, $mon, $mday);
    if($hour < 6){
	print "<optgroup>\n";
	print "<option value='$list_date_today $timerange[0]' selected>$list_date_today $timerange[0]</option>\n";
	print "/<optgroup>\n";
    }elsif($hour < 12){
	print "<optgroup>\n";
	print "<option value='$list_date_today $timerange[0]'>$list_date_today $timerange[0]</option>\n";
	print "<option value='$list_date_today $timerange[1]' selected>$list_date_today $timerange[1]</option>\n";
	print "/<optgroup>\n";
    }elsif($hour < 18){
	print "<optgroup>\n";
	print "<option value='$list_date_today $timerange[0]'>$list_date_today $timerange[0]</option>\n";
	print "<option value='$list_date_today $timerange[1]'>$list_date_today $timerange[1]</option>\n";
	print "<option value='$list_date_today $timerange[2]' selected>$list_date_today $timerange[2]</option>\n";
	print "/<optgroup>\n";
    }elsif($hour < 24){
	print "<optgroup>\n";
	print "<option value='$list_date_today $timerange[0]'>$list_date_today $timerange[0]</option>\n";
	print "<option value='$list_date_today $timerange[1]'>$list_date_today $timerange[1]</option>\n";
	print "<option value='$list_date_today $timerange[2]'>$list_date_today $timerange[2]</option>\n";
	print "<option value='$list_date_today $timerange[3]' selected>$list_date_today $timerange[3]</option>\n";
	print "/<optgroup>\n";
    }
print qq!    
</select></td></tr>
!;
    if($count == 1){
	$question_num += 1;
	print "<tr><td><B>��$question_num��</B></td><td><b>ɾ��Ź�ޤ����Ѳ��</b></td></tr>\n";
	print "    <tr><td></td><td>\n";
	print "    <select name='initial' style='width: 480px; font-size: 0.7em'>\n";
	print "<option value='N/A'>���򤷤Ƥ�������</option>\n";
	print "<option value='����'>����</option>\n";
	print "<option value='2-4����'>2-4����</option>\n";
	print "<option value='5-7����'>5-7����</option>\n";
	print "<option value='8-10����'>8-10����</option>\n";
	print "<option value='11���ܰʾ�'>11���ܰʾ�</option>\n";
	print "</select>\n";
	print "</td></tr>\n";
    }else{
	print "<INPUT TYPE='hidden' NAME='initial' VALUE='$initial'>\n";
    }
$question_num += 1;
print qq!    
<tr><td><B>��$question_num��</B></td><td><b>���Ѷ��</b></td></tr>
<tr><td></td><td>
!;
    for($i=1; $i<6; $i++){
	print "<select name='a2_$i' style='font-size: 0.7em'>\n";
	for($j=0; $j<10; $j++){
	    print "<option value='$j'>$j</option>\n";
	}
	print "</select>\n";
    }
print qq!
<b>��</b>
</td></tr>
!;
$question_num += 1;
print qq!    
<tr><td><B>��$question_num��</B></td><td><b>����/�������δ���</b></td></tr>
<tr><td></td><td>
<select name="a3" style='width: 480px; font-size: 0.7em'>
 <option value="N/A">���򤷤Ƥ�������</option>
<optgroup label="���˴��Ԥ��Ƥ���">
 <option value="+3">+3</option>
 <option value="+2">+2</option>
 <option value="+1">+1</option>
</optgroup>
<optgroup>
 <option value="��0">��0: �ɤ���Ȥ⤤���ʤ�</option>
</optgroup>
<optgroup>
 <option value="-1">-1</option>
 <option value="-2">-2</option>
 <option value="-3">-3</option>
</optgroup>
<optgroup label="�������Ԥ��Ƥ��ʤ��ä�">
</optgroup>
</select>
</td></tr>
!;
$question_num += 1;
print qq!    
<tr><td><B>��$question_num��</B></td><td><b>�󶡤��줿�����ӥ�</b></td></tr>
<tr><td></td><td>
<select name="a4" style='width: 480px; font-size: 0.7em'>
 <option value="N/A">���򤷤Ƥ�������</option>
<optgroup label="ͽ�ۤ����˾��ä�">
 <option value="+3">+3</option>
 <option value="+2">+2</option>
 <option value="+1">+1</option>
</optgroup>
<optgroup>
 <option value="��0">��0: ͽ���̤�</option>
</optgroup>
<optgroup>
 <option value="-1">-1</option>
 <option value="-2">-2</option>
 <option value="-3">-3</option>
</optgroup>
<optgroup label="ͽ�ۤ����˲���ä�">
</optgroup>
</select>
</td></tr>
!;
$question_num += 1;
print qq!    
<tr><td><B>��$question_num��</B></td><td><b>����/���Ѹ����­��</b></td></tr>
<tr><td></td><td>
<select name="a5" style='width: 480px; font-size: 0.7em'>
 <option value="N/A">���򤷤Ƥ�������</option>
<optgroup label="������­">
 <option value="+3">+3</option>
 <option value="+2">+2</option>
 <option value="+1">+1</option>
</optgroup>
<optgroup>
 <option value="��0">��0: �ɤ���Ȥ⤤���ʤ�</option>
</optgroup>
<optgroup>
 <option value="-1">-1</option>
 <option value="-2">-2</option>
 <option value="-3">-3</option>
</optgroup>
<optgroup label="��������">
</optgroup>
</select>
</td></tr>
!;
$question_num += 1;
print qq!
<tr><td><B>��$question_num��</B></td><td><b>������</b></td></tr>
<tr><td></td><td>
<textarea name="a6" style='width: 480px; font-size: 0.7em'></textarea>
</td></tr>
</font>
</TABLE>
<br>
	<P>
		<INPUT TYPE="hidden" NAME="count" VALUE="$count">
		<INPUT TYPE="hidden" NAME="number" VALUE="$number">
		<INPUT TYPE="submit" NAME="answer" VALUE="ɾ��������" style="font-size: 1em">
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
    print "<a href='../../../../../top.cgi'>Top</a><hr>";
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
# ��λ�ڡ�����ɽ�� ---------------------------------------------------------------------------
sub Print_Thanks
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
<b>ɾ���ǡ�������������λ���ޤ�����</b>
<br>
<b>��ưŪ��<a href="../../../../../top.cgi">Top�ڡ���</a>�����ޤ���</b>
<br>
<meta http-equiv="refresh" content=" 2 ;url= ../../../../../top.cgi"> 
</center>
		<P>
	</BODY>
	</HTML>
	!;
	exit;
}

