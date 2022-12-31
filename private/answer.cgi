#!/usr/bin/perl
require "cgi-lib.pl";
require "jcode.pl";

&ReadParse; # for cgi-lib.pl
$user_name = $ENV{'REMOTE_USER'};

# Answer
if($in{'mode'} eq "answer"){
  if($in{'id'}){ 
    $answerId = $in{'id'};
    open(IN, "./user/$user_name.log") or die "cannno open\n";
      @data = <IN>;
    close(IN);
    $i = 0;
    foreach(@data){
      chomp $_;
      @subdata = split(/\t/, $_);
      if($subdata[0] =~ /($answerId)/){
	  &Print_Questionnaire;
      }
      $i++;
    }
  }else{
  &Print_List;
  }
}elsif($in{"complete"}){
  # user name 
  $dir = $user_name.".log";
  
  open(IN, "./user/$dir") or die "cannot open the file\n";
    <IN>; # skip: face info 
  @data = <IN>;
  close(IN);

  # date 
  my($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) 
    = localtime(time);
  $year += 1900;
  $mon += 1;
  my($date) 
    = sprintf("%04d/%02d/%02d %02d:%02d:%02d",
        $year,$mon,$mday,$hour,$min,$sec);

  # Initial condition: in the case of putting complete
  $id = sprintf("%06d", $in{'id'});
  push(@answer,$id); # 0: id6��
  $in{"a1"} =~ s/[\r\n]+//g; # CR+LF��CR��LF����
  push(@answer,$in{"a1"}); # 1: �оݥ����ӥ�̾
  $in{"a2"} =~ s/[\r\n]+//g; # CR+LF��CR��LF����
  push(@answer,$in{"a2"}); # 2: ���ѳ��ϻ���
  $in{"a3"} =~ s/[\r\n]+//g; # CR+LF��CR��LF����
  push(@answer,$in{"a3"}); # 3: ���ѿͿ�
  $in{"a4"} =~ s/[\r\n]+//g; # CR+LF��CR��LF����
  push(@answer,$in{"a4"}); # 4: ���Ѳ��
  $in{"a5"} =~ s/[\r\n]+//g; # CR+LF��CR��LF����
  push(@answer,$in{"a5"}); # 5: ��������
  push(@answer,$in{"a7"}); 
  $money = $in{"a7_1"}.$in{"a7_2"}.$in{"a7_3"}.$in{"a7_4"}.$in{"a7_5"};
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
  push(@answer,$money); # 6: ���
  push(@answer,$in{"a8"}); # 7: ���ԥ���å�
  push(@answer,$in{"a9"}); # 8: ��­
  push(@answer,$in{"a10"}); # 9: �����Ѱտ�
  $in{"a11"} =~ s/[\r\n]+/<br>/g; # CR+LF��CR��LF����
  # push(@answer,$in{"a11"}); # 10: ��ͳ��
  push(@answer,$date);
  $processNumber = $in{"processNumber"};
  for($i=0;$i<=$processNumber;$i++){
    $eva = $in{"process_".$i}.":".$in{"a6_".$i};
    push(@answer,$eva); # 11 �ץ���ɾ��
  }
  if(open(OFILE,">>./answer.log")){
    # overall data
    print OFILE join("\t",@answer)."\n";
    close(OFILE); 
    # idividual data
    open(IND, ">>./answer/$user_name.log");
    print IND join("\t",@answer)."\n";
    close(IND); 
    &Print_Thanks; 
  }else{
    &Print_Error("�ե�����ν���˼��Ԥ��ޤ�����");
  }
}else{
  &Print_List;
}

# �����߷פ�List
sub Print_List {
  print "Content-type: text/html\n\n";
  print qq!
<HTML>
<HEAD>
<META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Cache-Control" content="no-cache">
<meta http-equiv="Expires" content="Thu, 01 Dec 1994 16:00:00 GMT">
<TITLE>
  ����Ź�Υ����ӥ����Ѥ��Ф��륢�󥱡���ɾ��������: ˬ����������ɾ��
</TITLE>
<style type="text/css">
a {color: #017acd}
table {width: 800px; font-size: 0.8 em; text-align: center;}
div#container {width: 880px; 
  margin-left: auto; margin-right: auto; font-size: 1.5em}
input[type="radio"]
{font-size:100%;height:30px;width:30px;margin:20px;}
</style>
</HEAD>

<BODY>
<div id="container">

<div id="header">
�桼��: $user_name &nbsp;&nbsp; 
<a href='./top.cgi'>Top�ڡ���</a> &nbsp;&nbsp; 
<a href='./history-post_modify.cgi'>ˬ���Ǥ�ˬ���������ν���</a> &nbsp;&nbsp; 
</div>

<hr>

<form action="answer.cgi" method="POST">
<div align="left">
<br>
<p>
<input type="hidden" name="mode" value="answer">
<input type="radio" name="id" value="" checked="checked" style="display:none;">
<input type="submit" value="�����å�����ˬ����������ɾ���򤹤�" 
  style="font-size: 1.0em">
</p>
<br>
</div>

<table class="table" border="4">
 <tr><th>����</th><th>ˬ��ͽ��Ź��̾</th><th>ˬ��ͽ�����</th><th>���ѿͿ�</th><th>���Ѳ��</th><th>��������</th><th>���������å�����</th></tr>
 !;

  open(IN, "./user/$user_name.log") or die "Cannot open file\n";
  <IN>; # 1�� �Ŀ;��󵭺���ʬ
    @data = <IN>;
  close(IN);

  open(IN2, "./answer/$user_name.log") or die "Cannot open file\n";
  <IN2>; # 1�� �Ŀ;��󵭺���ʬ
    @answer = <IN2>;
  close(IN2);

  $i = 1; 
  foreach(@answer){
    chomp($_);
    @subanswer = split(/\t/, $_);
    $same_id[$i] = $subanswer[0];
    $i++
  }
  $count = $i;
  @data = reverse(@data);
  
  foreach(@data){
    $done = 0;
    chomp($_);
    @subdata = split(/\t/, $_);
    for($i=1;$i<=$count;$i++){
      if($subdata[0] eq $same_id[$i]){
	  $done = 1;
      }
    }
    if($done == 1){
    print "<tr>
      <td>DONE</td>
      <td>$subdata[1]</td>
      <td>$subdata[2]</td>
      <td>$subdata[3]</td>
      <td>$subdata[4]</td>
      <td>$subdata[5]</td>
      <td>$subdata[6]</td>
      </tr>\n"
    }else{
    print "<tr>
      <td>
         <input type='radio' 
            name='id' 
              value='$subdata[0]' style='width: 35pt; height: 35pt'></td>
      <td>$subdata[1]</td>
      <td>$subdata[2]</td>
      <td>$subdata[3]</td>
      <td>$subdata[4]</td>
      <td>$subdata[5]</td>
      <td>$subdata[6]</td>
      </tr>\n"
    }
    }
    print qq!
</form>
</table>
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

sub Print_Questionnaire {
#########################################################################
# ���󥱡��ȥڡ���
#########################################################################
print "Content-type: text/html\n\n";
print qq!
<HTML>
<HEAD>
  <META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
  <TITLE>ˬ���ɾ��(�����å����ܤ�ɾ��)</TITLE>

<style type="text/css">
div#container{width: 750px; 
  margin-left: auto; margin-right: auto; font-size: 2em}
div#container td {font-size: 2.0em; height: 55px}
div#header{width: 750px; 
  margin-left: auto; margin-right: auto; font-size: 0.7em}
span.note{font-size: 14px;}
</style>
</HEAD>

<BODY>
<div id=container>

<div id="header">
�桼��: $user_name &nbsp;&nbsp; 
<a href='./top.cgi'>Top�ڡ���</a> &nbsp;&nbsp; 
<a href='./history-post_modify.cgi'>ˬ���Ǥ�ˬ���������ν���</a>
<hr>
</div>

<CENTER>
<FORM ACTION="answer.cgi" METHOD="POST">
<TABLE>
<font size=4>
<br>
<h2>ˬ���ɾ��(�����å����ܤ�ɾ��)</h2>
<br>
!;

$question_num = 1; # ����1
print qq!
<tr><td><B>
 ��$question_num��
  </B></td><td><b>ˬ�䤷��Ź��̾</b></td></tr>
<tr><td></td><td>
  <textarea name="a1" 
     style='width: 480px; height: 3.0em; font-size: 0.7em'>$subdata[1]</textarea><br>
<span class="note">* ���Ѥ��������ӥ���̾�Ρ�Ź��̾�ε���</span>
</td></tr>
!;

$question_num += 1; # ����2
print qq!
<tr><td><B>
  ��$question_num��</B></td><td><b>ˬ�䤷������</b></td></tr>
<tr><td></td><td>
  <textarea name="a2" 
     style='width: 480px; height: 3.0em; font-size: 0.7em'>$subdata[2]</textarea>
</td></tr>
!;

$question_num += 1;  # ����3
print qq!    
<tr><td><B>
   ��$question_num��</B></td><td><b>ˬ�䤷���Ϳ�</b></td></tr>
<tr><td></td><td>
  <textarea name="a3" 
     style='width: 480px; height: 3.0em; font-size: 0.7em'>$subdata[3]</textarea>
</td></tr>
!;

$question_num += 1;  # ����4
print qq!    
<tr><td><B>
   ��$question_num��</B></td><td><b>�о�Ź�ޤ����Ѳ��</b></td></tr>
<tr><td></td><td>
  <textarea name="a4" 
     style='width: 480px; height: 3.0em; font-size: 0.7em'>$subdata[4]</textarea>
</td></tr>
!;

$question_num += 1; # ����5
print qq!    
<tr><td><B>
   ��$question_num��</B></td><td><b>�о�Ź�ޤؤλ����δ�����</b></td></tr>
<tr><td></td><td>
  <textarea name="a5" 
     style='width: 480px; height: 3.0em; font-size: 0.7em' readonly>$subdata[5]</textarea><br>
<span class="note">* ������ɾ���Τ����ѹ��Բ�</span>
</td></tr>
!;

$question_num += 1; # ����6
print qq!
<tr><td><B>
  ��$question_num��</B></td><td><b>
���������å����ܤ���­��<br></b></td></tr>
!;
@process = split(/<br>/,$subdata[6]);
for($i=0;$i<=$#process;$i++){
  print "<tr><td></td><td>\n";
  print "<span class='note'><b>$process[$i]</b> ���Ф�����­��</span><br>\n";
  print "<select name='a6_$i' style='width: 480px; font-size: 0.7em'>\n";
  print "<optgroup label='������­'>\n";
  print " <option value='+3'>+3</option>\n";
  print " <option value='+2'>+2</option>\n";
  print " <option value='+1'>+1</option>\n";
  print "</optgroup>\n";
  print "<optgroup>\n";
  print " <option value='��0' selected>��0: �ɤ���Ȥ⤤���ʤ�</option>\n";
  print "</optgroup>\n";
  print "<optgroup>\n";
  print " <option value='-1'>-1</option>\n";
  print " <option value='-2'>-2</option>\n";
  print " <option value='-3'>-3</option>\n";
  print "</optgroup>\n";
  print "<optgroup label='��������'>\n";
  print "</optgroup>\n";
  print "</select>\n";
  print "</td></tr>\n";
}
print qq!    
</td></tr>
!;
print "<INPUT TYPE='hidden' NAME='processNumber' VALUE='$#process'>\n";
for($i=0;$i<=$#process;$i++){
  print "<INPUT TYPE='hidden' NAME='process_$i' VALUE='$process[$i]'>\n";
  }

$question_num += 1; # ����7
print qq!
<tr><td><B>��$question_num��</B></td><td><b>���Ѷ��</b></td></tr>
<tr><td></td><td>
!;
    for($i=1; $i<6; $i++){
	print "<select name='a7_$i' style='font-size: 0.7em'>\n";
	for($j=0; $j<10; $j++){
	    print "<option value='$j'>$j</option>\n";
	}
	print "</select>\n";
    }
print qq!
<b>��</b>
</td></tr>
!;

$question_num += 1; # ����8
print qq!    
<tr><td><B>��$question_num��</B></td><td><b>�����δ��Ԥ��Ф������Ѹ��ɾ��</b></td></tr>
<tr><td></td><td>
<select name="a8" style='width: 480px; font-size: 0.7em'>
<optgroup label="�������륵���ӥ���">
 <option value="+3">+3</option>
 <option value="+2">+2</option>
 <option value="+1">+1</option>
</optgroup>
<optgroup>
 <option value="��0" selected>��0: �����̤�Υ����ӥ���</option>
</optgroup>
<optgroup>
 <option value="-1">-1</option>
 <option value="-2">-2</option>
 <option value="-3">-3</option>
</optgroup>
<optgroup label="����򲼲�륵���ӥ���">
</optgroup>
</select>
</td></tr>
!;

$question_num += 1; # ����9
print qq!    
<tr><td><B>��$question_num��</B></td><td><b>���Ѹ������Ū����­��</b></td></tr>
<tr><td></td><td>
<select name="a9" style='width: 480px; font-size: 0.7em'>
<optgroup label="������­">
 <option value="+3">+3</option>
 <option value="+2">+2</option>
 <option value="+1">+1</option>
</optgroup>
<optgroup>
 <option value="��0" selected>��0: �ɤ���Ȥ⤤���ʤ�</option>
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

$question_num += 1; # ����10
print qq!
<tr><td><B>��$question_num��</B></td><td><b>���줫����κ����Ѱո�</b></td></tr>
<tr><td></td><td>
<select name="a10" style='width: 480px; font-size: 0.7em'>
<optgroup label="�ޤ����Ѥ�����">
 <option value="+3">+3</option>
 <option value="+2">+2</option>
 <option value="+1">+1</option>
</optgroup>
<optgroup>
 <option value="��0" selected>��0: �ɤ���Ȥ⤤���ʤ�</option>
</optgroup>
<optgroup>
 <option value="-1">-1</option>
 <option value="-2">-2</option>
 <option value="-3">-3</option>
</optgroup>
<optgroup label="�⤦���Ѥ������ʤ�">
</optgroup>
</select>
</td></tr>
!;

print qq!
</font>
</TABLE>
<br>
   <P>
     <INPUT TYPE="hidden" NAME="count" VALUE="$count">
     <INPUT TYPE="hidden" NAME="number" VALUE="$number">
     <INPUT TYPE="hidden" NAME="id" VALUE="$subdata[0]">
     <INPUT TYPE="submit" NAME="complete" VALUE="ˬ���ɾ��������" style="font-size: 1em">
	</FORM>
        <p>
		</CENTER>
</div>
</BODY>
</HTML>
!;
    }
# top bar
sub UserName {
  print "<div id='header'>";
  print "�桼�� : $user_name��";
  print "<a href='./top.cgi'>Top�ڡ���</a>";
  print "<hr>";
  print "</div>";
}

# ���顼�ڡ�����ɽ�� 
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
sub Print_Thanks
{
    print "Content-type: text/html\n\n";
    print qq!
<HTML>
<HEAD>
<META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
<TITLE>ˬ���ɾ��������</TITLE>
</HEAD>
<BODY>
<BR>
<center>
<br>
<b>ˬ���ɾ������������λ���ޤ�����</b>
<br>
<b>��ưŪ��<a href="./top.cgi">Top�ڡ���</a>�����ޤ���</b>
<br>
<meta http-equiv="refresh" content=" 2 ;url= ./top.cgi"> 
</center>
		<P>
	</BODY>
	</HTML>
	!;
	exit;
}


