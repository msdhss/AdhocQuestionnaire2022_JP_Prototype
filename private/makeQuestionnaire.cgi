#!/usr/bin/perl
require "cgi-lib.pl";
require "jcode.pl";
&ReadParse; # $in{'name'}: included form data

&WebQ; 

# MAIN SCRIPT
sub WebQ{

# get username 
  $user_name = $ENV{'REMOTE_USER'};
  $dir = $user_name.".log";
  
  open(IN, "./user/$dir") or die "cannot open the file\n";
  @data = <IN>;
  close(IN);

  @subdata = split(/\t/,$data[0]); # tab
  $id_name = $subdata[0]; # number for his answers
  $id_communication = $subdata[1] + 1; # number for his answers
  $id_answer = $subdata[2] + 1; # number for his answers

# get current date 
  my($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) 
    = localtime(time);
  $year += 1900;
  $mon += 1;
  my($date) 
    = sprintf("%04d/%02d/%02d %02d:%02d:%02d",
        $year,$mon,$mday,$hour,$min,$sec);
  my($time) 
    = sprintf("%04d/%02d/%02d %02d:%02d",
        $year,$mon,$mday,$hour,$min);

# CONDITION: putting the ANSWER1 / AINSER2 bottons
  if($in{"question"}){
    push(@question,$id_name); # -> [0]
    $id_communication = sprintf("%06d", $id_communication); 
    push(@question,$id_communication); # -> [1]
    $service = $in{"a0-1"}; # service-name
    $service =~ s/[\r\n]+/<br>/g; # CR+LF��CR��LF�� \n �����줷���ղ�
    $process = $in{"a0-2"}; # process
    $process =~ s/[\r\n]+/<br>/g; # CR+LF��CR��LF�� \n �����줷���ղ�
    push(@question,$service); # -> [2]
    push(@question,$process); # -> [3]
    push(@question,$date); # -> [4]
    if(open(OFILE,">>./communication.log")){
      # overall data
      print OFILE join("\t",@question)."\n";
      close(OFILE); 
      # idividual data(user)
      # open(IND, ">>./user/$user_name.log");
      # print IND join("\t",@question)."\n";
      #  close(IND); 
      # idividual data(communication)
      # open(IND2, ">>./communication/$user_name.log");
      # print IND2 join("\t",@question)."\n";
      # close(IND2); 
      # ���Τ��ɤ�ľ���ơ�communication �� #id_answer �� count++����
      open(IN, "./user/$user_name.log");
      @data = <IN>;
      close(IN); 
      open(OUT, ">./user/$user_name.log");
      foreach(@data){
        if($_ =~ /$user_name/){
	  @subdata = split(/\t/,$_);
          $subdata[1] += 1;
          print OUT join("\t",@subdata)."\n";
	}else{
          print OUT $_;
	}
      }
      close(OUT); 
      &Print_Questionnaire; #SUB2
    }else{
      &Print_Error("�ե�����ν���˼��Ԥ��ޤ�����");
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
    push(@answer,$id_name); # -> [0]
    $id_answer = sprintf("%06d", $id_answer); # number for answer | 6��
    push(@answer,$id_answer); # -> [1]: id6��
    $in{"a1"} =~ s/[\r\n]+//g; # CR+LF��CR��LF����
    push(@answer,$in{"a1"}); # -> [2]: �оݥ����ӥ�̾
    $in{"a2"} =~ s/[\r\n]+//g; # CR+LF��CR��LF����
    push(@answer,$in{"a2"}); # -> [3]: ���ѳ��ϻ���
    $in{"a3"} =~ s/[\r\n]+//g; # CR+LF��CR��LF����
    push(@answer,$in{"a3"}); # -> [4]: ���ѿͿ�
    $in{"a4"} =~ s/[\r\n]+//g; # CR+LF��CR��LF����
    push(@answer,$in{"a4"}); # -> [5]: ���Ѳ��
    $in{"a5"} =~ s/[\r\n]+//g; # CR+LF��CR��LF����
    push(@answer,$in{"a5"}); # -> [6]: ��������
    $money = $in{"a7_1"}.$in{"a7_2"}.$in{"a7_3"}.$in{"a7_4"}.$in{"a7_5"}.$in{"a7_6"}; # 6 digit; JP000000, 
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
	    if($find == 0){
  	    substr($money,0,1)="";
	    $find = index($money,"0");
	    }
  	  }
        }
      }
    }
# $money = $in{"a7_1"}.$in{"a7_2"}.$in{"a7_3"}.$in{"a7_4"}.",".$in{"a7_5"}.$in{"a7_6"}; # 6 digit; EUR 0000,00
#    $find = index($money,"0");
#    if($find == 0){
#      substr($money,0,1)="";
#      $find = index($money,"0");
#      if($find == 0){
#        substr($money,0,1)="";
#        $find = index($money,"0");
#        if($find == 0){
#  	  substr($money,0,1)="";
#  	  $find = index($money,"0");
#	}
#      }
#    }
    push(@answer,$money); # -> [7]: ���
    push(@answer,$in{"a8"}); # -> [8]: ���ԥ���å�
    push(@answer,$in{"a9"}); # -> [9]: ��­
    push(@answer,$in{"a10"}); # -> [10]: �����Ѱտ�
    push(@answer,$in{"a11"}); # -> [11]: �����տ�
    $in{"a12"} =~ s/[\r\n]+//g; # CR+LF��CR��LF����
    push(@answer,$in{"a12"}); # -> [12]: �������ΤΥ�����
    push(@answer,$date); # -> [13]: ��������
    $processNumber = $in{"processNumber"};
    for($i=0;$i<=$processNumber;$i++){
      $in{"process_".$i} =~ s/:/��/g; #
      $in{"a6-2_".$i} =~ s/[\r\n]+//g; # CR+LF��CR��LF����
      $in{"a6-2_".$i} =~ s/:/��/g; # 
      $eva = $in{"process_".$i}.":".$in{"a6-1_".$i}.":".$in{"a6-2_".$i};
      push(@answer,$eva); # -> [14] �ץ���ɾ��
    }
    if(open(OFILE,">>./answer.log")){
      # overall data
      print OFILE join("\t",@answer)."\n";
      close(OFILE); 
      # idividual data
      open(IND, ">>./answer/$user_name.log");
      print IND join("\t",@answer)."\n";
      close(IND); 
      # ���Τ��ɤ�ľ���ơ�user �� #id_answer �� count++����
      open(IN, "./user/$user_name.log");
      @data = <IN>;
      close(IN); 
      open(OUT, ">./user/$user_name.log");
      foreach(@data){
        if($_ =~ /$user_name/){
	  @subdata = split(/\t/,$_);
          $subdata[2] += 1;
          print OUT join("\t",@subdata)."\n";
	}else{
          print OUT $_;
	}
      }
      close(OUT); 
      &Print_Thanks; 
    }else{
      &Print_Error("�ե�����ν���˼��Ԥ��ޤ�����");
    }
  }else{
    &Print_Communication; # SUB1
  }
}

sub Print_Communication {
# SUB1
# ���ߥ�˥�����������˴ؤ���HTML 
print "Content-type: text/html\n\n";
print qq!
<HTML>
<HEAD>
  <META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
  <TITLE>
���󥱡��Ȥ˲�������
</TITLE>

<style type="text/css">
div#container{width: 750px; 
  margin-left: auto; margin-right: auto; font-size: 1.5em}
div#container td {font-size: 1.5em; height: 55px}
div#header{width: 750px; 
  margin-left: auto; margin-right: auto; font-size: 1.3em}
span.note{font-size: 18px; line-height: 170%;}
.line-space {line-height: 170%;}
.line-space1 {line-height: 115%;}
.line-space2 {line-height: 125%;}
.line-space3 {line-height: 135%;}
.line-space4 {line-height: 145%;}
.line-space5 {line-height: 155%;}
.line-space6 {line-height: 165%;}
</style>
</HEAD>

<BODY>

<div id=container>
${&UserName}
!;

print qq!
<CENTER>
<FORM ACTION="makeQuestionnaire.cgi" METHOD="POST">
<TABLE>
<font size=4>
<h2>
���󥱡��Ȥ˲�������
</h2>
</font>
<font size=1>
!;

$question_num += 1; # Communication ���
print qq!
<tr><td><b>
��$question_num��</b></td><td><b>���Ѥ���Ź��̾��������</b></td></tr>
<tr><td></td><td>
  <textarea name="a0-1" 
     style='width: 550px; height: 2em; font-size: 1em'>
</textarea>
</td></tr>
!;

$question_num += 1; # Communication ���
print qq!
<tr><td><b>
  ��$question_num��</b></td><td><b>���Ѥ���Ź�ޤǤθġ��ι�ư��������</b></td></tr>
<tr><td></td><td>
  <textarea name="a0-2" 
     style='width: 550px; height: 10em; font-size: 1em'>
</textarea>
</td></tr>
!;

print qq!
</font>
</TABLE>
<br>
	<P>
		<INPUT TYPE="hidden" NAME="count" VALUE="$count">
		<INPUT TYPE="hidden" NAME="number" VALUE="$number">
		<INPUT TYPE="submit" NAME="question" VALUE="Ź��̾�ȹ�ư����Ͽ����" style="font-size: 1em">
	</FORM>
        <p>
</CENTER>
<hr>
<span class="note">
* �ڣ��ۤȡڣ��ۤε����塢��Ź��̾�ȹ�ư����Ͽ����٥ܥ���򥯥�å����Ƥ�������<br>
* �ܥ��󤬲�����뤳�Ȥǡ������ӥ����Ѥ˴ؤ��륢�󥱡��Ȥ��Ϥޤ�ޤ�<br>
* �ڣ��ۤε��ҷ����ϰʲ����̤�Ǥ���<font color="red">ɬ�����ƹ�ư��ˡ�"����"�򤷤Ƶ������Ƥ�������</font><br>
��������(1����) ��ư1<br>
��������(2����) ��ư2<br>
��������(3����) ��ư3<br>
��������������<br>
</span>
<hr>
</div>
</BODY>
</HTML>
!;
}

sub Print_Questionnaire {
# SUB2
# ���󥱡��ȥڡ���
print "Content-type: text/html\n\n";
print qq!
<HTML>
<HEAD>
  <META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
  <TITLE>
���󥱡��Ȥ˲�������
</TITLE>

<style type="text/css">
div#container{width: 750px; 
  margin-left: auto; margin-right: auto; font-size: 2em}
div#container td {font-size: 2.0em; height: 55px}
div#header{width: 750px; 
  margin-left: auto; margin-right: auto; font-size: 0.7em}
span.note{font-size: 14px; line-height: 150%}
.line-space {line-height: 150%;}
.line-space1 {line-height: 115%;}
.line-space2 {line-height: 125%;}
.line-space3 {line-height: 135%;}
.line-space4 {line-height: 145%;}
.line-space5 {line-height: 155%;}
.line-space6 {line-height: 165%;}
.line-space7 {line-height: 175%;}
</style>
</HEAD>

<BODY>
<div id=container>

<div id="header">
�桼��: $user_name &nbsp;&nbsp; 
<a href='./top.cgi'>Top�ڡ���</a> &nbsp;&nbsp; 
<hr>
</div>

<CENTER>
<FORM ACTION="makeQuestionnaire.cgi" METHOD="POST">
<TABLE>
<font size=4>
<h2>
<span class="line-space">
���󥱡��Ȥ˲������� <br>
</span></h2>
<br>
!;

$service =~ s/<br>/ /g;
$question_num = 1; # ����1
print qq!
<tr><td><B>
 ��$question_num��
  </B></td><td><b>ˬ�䤷��Ź��̾</b></td></tr>
<tr><td></td><td>
  <textarea name="a1" 
     style='width: 480px; height: 3.0em; font-size: 0.7em'>$service</textarea><br>
<span class="note">* ���Ѥ��������ӥ���̾�Ρ�Ź��̾�򤴵�����������</span>
</td></tr>
!;

$question_num += 1; # ����2
# get current date 
  my($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) 
    = localtime(time);
  $year += 1900;
  $mon += 1;
  $weekday = &GetWeekDay($year, $mon, $mday, 1);
  my($date) 
    = sprintf("%04d/%02d/%02d %02d:%02d:%02d",
        $year,$mon,$mday,$hour,$min,$sec);
  my($time) 
    = sprintf("%04d/%02d/%02d (%s) %02d:%02d",
        $year,$mon,$mday,$weekday,$hour,$min);

print qq!
<tr><td><B>
  ��$question_num��</B></td>
<td><b>ˬ�����</b></td></tr>
<tr><td></td><td>
<span class="note">
* ���ߤλ���: $time</span>
<br>
<select name="a2" style="width: 480px; font-size: 0.7em">
!;
  # previous
  for($i=7;$i>0;$i--){
    $t = time;
    $t -= $i*60*60*24;
    my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) 
      = localtime($t);
    $year += 1900;
    $mon += 1;
    $weekday = &GetWeekDay($year, $mon, $mday, 1);
    $list_date = sprintf("%04d/%02d/%02d (%s) ", $year, $mon, $mday, $weekday );
      @timerange 
         = ('00:00-03:00','03:00-06:00','06:00-09:00','09:00-12:00',
              '12:00-15:00','15:00-18:00','18:00-21:00','21:00-24:00');
    print  "<optgroup>\n";
    foreach $j (0 .. 7){
      print "<option value='$list_date $timerange[$j]'>
                $list_date  $timerange[$j]
                   </option>\n";
    }
    print  "</optgroup>\n";
  }
  # Today
  $t = time;
  my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) 
    = localtime($t);
  $year += 1900;
  $mon += 1;
  $weekday = &GetWeekDay($year, $mon, $mday, 1);
  $list_date_today = sprintf("%04d/%02d/%02d (%s) ", $year, $mon, $mday, $weekday);
  if($hour < 3){
    print "<optgroup>\n";
    print "<option value='$list_date_today $timerange[0]' selected>
              $list_date_today $timerange[0]</option>\n";
    print "</optgroup>\n";
  }elsif($hour < 6){
    print "<optgroup>\n";
    print "<option value='$list_date_today $timerange[0]'>
              $list_date_today $timerange[0]</option>\n";
    print "<option value='$list_date_today $timerange[1]' selected>
              $list_date_today $timerange[1]</option>\n";
    print "</optgroup>\n";
  }elsif($hour < 9){
    print "<optgroup>\n";
    print "<option value='$list_date_today $timerange[0]'>
              $list_date_today $timerange[0]</option>\n";
    print "<option value='$list_date_today $timerange[1]'>
              $list_date_today $timerange[1]</option>\n";
    print "<option value='$list_date_today $timerange[2]' selected>
              $list_date_today $timerange[2]</option>\n";
    print "</optgroup>\n";
  }elsif($hour < 12){
    print "<optgroup>\n";
    print "<option value='$list_date_today $timerange[0]'>
              $list_date_today $timerange[0]</option>\n";
    print "<option value='$list_date_today $timerange[1]'>
              $list_date_today $timerange[1]</option>\n";
    print "<option value='$list_date_today $timerange[2]'>
              $list_date_today $timerange[2]</option>\n";
    print "<option value='$list_date_today $timerange[3]' selected>
              $list_date_today $timerange[3]</option>\n";
    print "</optgroup>\n";
  }elsif($hour < 15){
    print "<optgroup>\n";
    print "<option value='$list_date_today $timerange[0]'>
              $list_date_today $timerange[0]</option>\n";
    print "<option value='$list_date_today $timerange[1]'>
              $list_date_today $timerange[1]</option>\n";
    print "<option value='$list_date_today $timerange[2]'>
              $list_date_today $timerange[2]</option>\n";
    print "<option value='$list_date_today $timerange[3]'>
              $list_date_today $timerange[3]</option>\n";
    print "<option value='$list_date_today $timerange[4]' selected>
              $list_date_today $timerange[4]</option>\n";
    print "</optgroup>\n";
  }elsif($hour < 18){
    print "<optgroup>\n";
    print "<option value='$list_date_today $timerange[0]'>
              $list_date_today $timerange[0]</option>\n";
    print "<option value='$list_date_today $timerange[1]'>
              $list_date_today $timerange[1]</option>\n";
    print "<option value='$list_date_today $timerange[2]'>
              $list_date_today $timerange[2]</option>\n";
    print "<option value='$list_date_today $timerange[3]'>
              $list_date_today $timerange[3]</option>\n";
    print "<option value='$list_date_today $timerange[4]'>
              $list_date_today $timerange[4]</option>\n";
    print "<option value='$list_date_today $timerange[5]' selected>
              $list_date_today $timerange[5]</option>\n";
    print "</optgroup>\n";
  }elsif($hour < 21){
    print "<optgroup>\n";
    print "<option value='$list_date_today $timerange[0]'>
              $list_date_today $timerange[0]</option>\n";
    print "<option value='$list_date_today $timerange[1]'>
              $list_date_today $timerange[1]</option>\n";
    print "<option value='$list_date_today $timerange[2]'>
              $list_date_today $timerange[2]</option>\n";
    print "<option value='$list_date_today $timerange[3]'>
              $list_date_today $timerange[3]</option>\n";
    print "<option value='$list_date_today $timerange[4]'>
              $list_date_today $timerange[4]</option>\n";
    print "<option value='$list_date_today $timerange[5]'>
              $list_date_today $timerange[5]</option>\n";
    print "<option value='$list_date_today $timerange[6]' selected>
              $list_date_today $timerange[6]</option>\n";
    print "</optgroup>\n";
  }elsif($hour < 24){
    print "<optgroup>\n";
    print "<option value='$list_date_today $timerange[0]'>
              $list_date_today $timerange[0]</option>\n";
    print "<option value='$list_date_today $timerange[1]'>
              $list_date_today $timerange[1]</option>\n";
    print "<option value='$list_date_today $timerange[2]'>
              $list_date_today $timerange[2]</option>\n";
    print "<option value='$list_date_today $timerange[3]'>
              $list_date_today $timerange[3]</option>\n";
    print "<option value='$list_date_today $timerange[4]'>
              $list_date_today $timerange[4]</option>\n";
    print "<option value='$list_date_today $timerange[5]'>
              $list_date_today $timerange[5]</option>\n";
    print "<option value='$list_date_today $timerange[6]'>
              $list_date_today $timerange[6]</option>\n";
    print "<option value='$list_date_today $timerange[7]' selected>
              $list_date_today $timerange[7]</option>\n";
    print "</optgroup>\n";
  }
  # forward
  #for($i=1;$i<10;$i++){
  #  $t = time;
  #  $t += $i*60*60*24;
  #  my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) 
  #    = localtime($t);
  #  $year += 1900;
  #  $mon += 1;
  #  $list_date = sprintf("%04d/%02d/%02d", $year, $mon, $mday);
  #    @timerange 
  #       = ('00:00-06:00','06:00-12:00','12:00-18:00','18:00-24:00');
  #  print  "<optgroup>\n";
  #  foreach $j (0 .. 3){
  #    print "<option value='$list_date $timerange[$j]'>
  #              $list_date $timerange[$j]
  #                 </option>\n";
  #  
  #  print  "</optgroup>\n";
  #}

$question_num += 1;  # ����3
print qq!    
</select>
</td></tr>
!;
  print "<tr><td><B>
          ��$question_num��</B></td><td><b>
              ˬ�䤷���Ϳ�</b></td></tr>\n";
  print "<tr><td></td><td>\n";
  print "<select 
            name='a3' style='width: 480px; font-size: 0.7em'>\n";
  print "<option value='1'>1��</option>\n";
  print "<option value='2'>2��</option>\n";
  print "<option value='3'>3��</option>\n";
  print "<option value='4-6'>4-6��</option>\n";
  print "<option value='7-9'>7-9��</option>\n";
  print "<option value='10�Ͱʾ�'>10�Ͱʾ�</option>\n";
  print "</select>\n";
  print "</td></tr>\n";

$question_num += 1;  # ����4
print qq!    
</select>
</td></tr>
!;
  print "<tr><td><B>
          ��$question_num��</B></td><td><b>
              �о�Ź�ޤ����Ѳ��</b></td></tr>\n";
  print "<tr><td></td><td>\n";
  print "<select 
            name='a4' style='width: 480px; font-size: 0.7em'>\n";
  print "<option value='����'>����</option>\n";
  print "<option value='2����'>2����</option>\n";
  print "<option value='3����'>3����</option>\n";
  print "<option value='4-6����'>4-6����</option>\n";
  print "<option value='7-9����'>7-9����</option>\n";
  print "<option value='10���ܰʾ�'>10���ܰʾ�</option>\n";
  print "</select>\n";
  print "</td></tr>\n";

$question_num += 1; # ����5
print qq!    
<tr><td><B>��$question_num��</B></td><td><b>�о�Ź�ޤؤλ����δ�����</b></td></tr>
<tr><td></td><td>
<select name="a5" style='width: 480px; font-size: 0.7em'>
<optgroup label="���˴��Ԥ��Ƥ���">
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
<optgroup label="�������Ԥ��Ƥ��ʤ��ä�">
</optgroup>
</select>
</td></tr>
!;

$question_num += 1; # ����6
print qq!
<tr><td><B>
  ��$question_num��</B></td><td><b>
ȯ��������ư����­�٤ȥ�����<br></b></tr>
<tr><td></td><td>
<span class="note"> * �ʤˤ�<b>��­������ư</b>�����ä���硢<b>�⤤ɾ��</b>���դ��Ƥ�������<br>
<span class="note"> * �ʤˤ�<b>����­�ʹ�ư</b>�����ä���硢<b>�㤤ɾ��</b>���դ��Ƥ�������<br>
<span class="note"> * �⤷����ɾ���˴ؤ��Ƥʤˤ�<b>��ͳ</b>��������ϡ�<b><u>������ͳ�⵭��</u></b>���Ƥ�������<br>
* <b>��ɮ���٤������ʤ����</b>��̵����ɾ���������Ȥ򤹤�ɬ�פϤ���ޤ���<br>������򤽤Τޤޤˤ��Ƽ��ι��ܤ˰ܤäƤ���������<br></span>
<span class="note">��</span>
</td></tr>
!;

@process = split(/<br>/,$process);
for($i=0;$i<=$#process;$i++){
  print "<tr><td></td><td>\n";
  print "<span class='note'><b>$process[$i]</b> ���Ф�����­�٤ȥ�����</span><br>\n";
  print "<select name='a6-1_$i' style='width: 480px; font-size: 0.7em'>\n";
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
  print "<span class='line-space2'>&nbsp;</span>\n";
  print "<textarea name='a6-2_$i' style='width: 480px; height: 1.5em; font-size: 0.7em'></textarea>\n";
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
# ��: 000000
#    for($i=1; $i<7; $i++){
#	print "<select name='a7_$i' style='font-size: 0.7em'>\n";
#	for($j=0; $j<10; $j++){
#	    print "<option value='$j'>$j</option>\n";
#	}
#	print "</select>\n";
#    }
# print qq!
#<b>��</b><br>
# ��: 000,000
# EUR: 0000,00
    for($i=1; $i<7; $i++){
	print "<select name='a7_$i' style='font-size: 0.7em'>\n";
	for($j=0; $j<10; $j++){
	    print "<option value='$j'>$j</option>\n";
	  }
	if($i == 3){
	  print "</select>\n"; # comma
	}else{
	  print "</select>\n";
	}
    }
print qq!
<b>��</b><br>
<span class="note"> * ������: 1��������(ʿ��)</span>
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
 <option value="�狼��ʤ�">�狼��ʤ�(ɾ���Ǥ��ʤ�)</option>
</optgroup>
</select>
</td></tr>
!;

$question_num += 1; # ����9, V-a9
print qq!    
<tr><td><B>��$question_num��</B></td><td><b>�������Τ������­��</b>
</td></tr>
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
# <br><span class="note">* ����Ū��ͧ�ͤ�Ʊν�˴�����뤰�餤��­�������ˡ��⤤ɾ�����դ��Ƥ���������</span><br>
# <span class="note">* ����Ū��ͧ�ͤ�Ʊν�˴�����ʤ����餤����­���ä����ˡ��㤤ɾ�����դ��Ƥ���������</span>

$question_num += 1; # ����10, Var: a10
print qq!
<tr><td><B>��$question_num��</B></td><td><b>����κ�ˬ��ո�</b></td></tr>
<tr><td></td><td>
<select name="a10" style='width: 480px; font-size: 0.7em'>
<optgroup label="���Υ����ӥ��Ϥޤ����Ѥ�����">
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
<optgroup label="���Υ����ӥ��Ϥ⤦���Ѥ������ʤ�">
</optgroup>
</select>
</td></tr>
!;

$question_num += 1; # ����11, Var-a11
print qq!
<tr><td><B>��$question_num��</B></td><td><b>ͧ�͡��οͤؤο����ո�</b></td></tr>
<tr><td></td><td>
<select name="a11" style='width: 480px; font-size: 0.7em'>
<optgroup label="���Υ����ӥ������Ѥ�ͧ�͡��οͤ˿���������">
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
<optgroup label="���Υ����ӥ������Ѥ�ͧ�͡��οͤ˿����������ʤ�">
</optgroup>
</select>
</td></tr>
!;

$question_num += 1; # ����12
print qq!
<tr><td><B>
 ��$question_num��
  </B></td><td><b>�������Τ˴ؤ��륳����</b><br>
</td></tr>
<tr><td></td><td>
  <textarea name="a12" 
     style='width: 480px; height: 3.0em; font-size: 0.7em'></textarea><br><span class="note">* ����Υ����ӥ��������Τ˴ؤ��Ƥʤˤ������Ȥ�����Ф�������������</span>
</td></tr>
!;

print qq!
</font>
</TABLE>
<br>
   <P>
     <INPUT TYPE="hidden" NAME="count" VALUE="$count">
     <INPUT TYPE="hidden" NAME="number" VALUE="$number">
     <INPUT TYPE="submit" NAME="complete" VALUE="�������Ƥ�����" style="font-size: 1em">
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
    print "�桼�� : $user_name &nbsp;&nbsp;";
    print "<a href='./top.cgi'>Top�ڡ���</a><hr>";
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
	  <form action="makeQuestionnaire.cgi" method="post">
	  ���Ƥ�����<INPUT TYPE="submit" NAME="first" VALUE="1"><br>
	  ���ƤǤϤʤ�<INPUT TYPE="submit" NAME="first" VALUE="2"><br>
	  </form>
	 </body>
	</html>
	!;
    exit;
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

#########################################################################
# ��λ�ڡ�����ɽ�� 
#########################################################################
sub Print_Thanks
{
    print "Content-type: text/html\n\n";
    print qq!
<HTML>
<HEAD>
<META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
<TITLE>���󥱡��Ȳ����Υǡ�������</TITLE>
<style type="text/css">
  div#container{width: 750px; 
    margin-left: auto; margin-right: auto; font-size: 1.5em}
  div#container td {font-size: 1.5em; height: 55px}
  div#header{width: 750px; 
    margin-left: auto; margin-right: auto; font-size: 1.3em}
  span.note{font-size: 18px; line-height: 140%;}
  .line-space {line-height: 170%;}
.line-space1 {line-height: 115%;}
.line-space2 {line-height: 125%;}
.line-space3 {line-height: 135%;}
.line-space4 {line-height: 145%;}
.line-space5 {line-height: 155%;}
.line-space6 {line-height: 165%;}
</style>
</HEAD>
<BODY>
<BR>
<center>
<br>
<span class="line-space">
<b>���󥱡��Ȳ����Υǡ�����������λ���ޤ�����</b><br>
<b>��ưŪ��<a href="./top.cgi">Top�ڡ���</a>�����ޤ���</b><br>
</span>
<meta http-equiv="refresh" content=" 2 ;url= ./top.cgi"> 
</center>
		<P>
	</BODY>
	</HTML>
	!;
	exit;
}

#########################################################################
# Subroutine: GatWeekDay
#########################################################################
sub GetWeekDay {
    my($year, $mon, $day, $flag) = @_;
    if($year == 1582) {
        if($mon < 10) {
            return -1;
        } elsif($mon == 10) {
            if($day < 15) {
                return -1;
            }
        }
    } elsif($year < 1582) {
        return -1;
    }
    if($mon == 1 || $mon == 2) {
        $year --;
        $mon += 12;
    }
    my $week = ($year + int($year/4) - int($year/100) + int($year/400) + int((13*$mon+8)/5) + $day) % 7;
    if($flag) {
        my @map = ('��', '��', '��', '��', '��', '��', '��');
        return $map[$week];
    } else {
        return $week;
    }
 }
#########################################################################
