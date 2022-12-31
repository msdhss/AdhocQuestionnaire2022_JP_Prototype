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
    $service =~ s/[\r\n]+/<br>/g; # CR+LF／CR／LFを \n に統一して付加
    $process = $in{"a0-2"}; # process
    $process =~ s/[\r\n]+/<br>/g; # CR+LF／CR／LFを \n に統一して付加
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
      # 全体を読み直して、communication の #id_answer を count++する
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
      &Print_Error("ファイルの書込に失敗しました。");
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
    $id_answer = sprintf("%06d", $id_answer); # number for answer | 6桁
    push(@answer,$id_answer); # -> [1]: id6桁
    $in{"a1"} =~ s/[\r\n]+//g; # CR+LF／CR／LFを削除
    push(@answer,$in{"a1"}); # -> [2]: 対象サービス名
    $in{"a2"} =~ s/[\r\n]+//g; # CR+LF／CR／LFを削除
    push(@answer,$in{"a2"}); # -> [3]: 利用開始時間
    $in{"a3"} =~ s/[\r\n]+//g; # CR+LF／CR／LFを削除
    push(@answer,$in{"a3"}); # -> [4]: 利用人数
    $in{"a4"} =~ s/[\r\n]+//g; # CR+LF／CR／LFを削除
    push(@answer,$in{"a4"}); # -> [5]: 利用回数
    $in{"a5"} =~ s/[\r\n]+//g; # CR+LF／CR／LFを削除
    push(@answer,$in{"a5"}); # -> [6]: 事前期待
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
    push(@answer,$money); # -> [7]: 金額
    push(@answer,$in{"a8"}); # -> [8]: 期待ギャップ
    push(@answer,$in{"a9"}); # -> [9]: 満足
    push(@answer,$in{"a10"}); # -> [10]: 再利用意図
    push(@answer,$in{"a11"}); # -> [11]: 推薦意図
    $in{"a12"} =~ s/[\r\n]+//g; # CR+LF／CR／LFを削除
    push(@answer,$in{"a12"}); # -> [12]: 利用全体のコメント
    push(@answer,$date); # -> [13]: 回答日時
    $processNumber = $in{"processNumber"};
    for($i=0;$i<=$processNumber;$i++){
      $in{"process_".$i} =~ s/:/：/g; #
      $in{"a6-2_".$i} =~ s/[\r\n]+//g; # CR+LF／CR／LFを削除
      $in{"a6-2_".$i} =~ s/:/：/g; # 
      $eva = $in{"process_".$i}.":".$in{"a6-1_".$i}.":".$in{"a6-2_".$i};
      push(@answer,$eva); # -> [14] プロセス評価
    }
    if(open(OFILE,">>./answer.log")){
      # overall data
      print OFILE join("\t",@answer)."\n";
      close(OFILE); 
      # idividual data
      open(IND, ">>./answer/$user_name.log");
      print IND join("\t",@answer)."\n";
      close(IND); 
      # 全体を読み直して、user の #id_answer を count++する
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
      &Print_Error("ファイルの書込に失敗しました。");
    }
  }else{
    &Print_Communication; # SUB1
  }
}

sub Print_Communication {
# SUB1
# コミュニケーション手順書に関するHTML 
print "Content-type: text/html\n\n";
print qq!
<HTML>
<HEAD>
  <META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
  <TITLE>
アンケートに回答する
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
アンケートに回答する
</h2>
</font>
<font size=1>
!;

$question_num += 1; # Communication 手順
print qq!
<tr><td><b>
【$question_num】</b></td><td><b>利用した店舗名を記入する</b></td></tr>
<tr><td></td><td>
  <textarea name="a0-1" 
     style='width: 550px; height: 2em; font-size: 1em'>
</textarea>
</td></tr>
!;

$question_num += 1; # Communication 手順
print qq!
<tr><td><b>
  【$question_num】</b></td><td><b>利用した店舗での個々の行動を記入する</b></td></tr>
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
		<INPUT TYPE="submit" NAME="question" VALUE="店舗名と行動を登録する" style="font-size: 1em">
	</FORM>
        <p>
</CENTER>
<hr>
<span class="note">
* 【１】と【２】の記入後、『店舗名と行動を登録する』ボタンをクリックしてください<br>
* ボタンが押されることで、サービス利用に関するアンケートが始まります<br>
* 【２】の記述形式は以下の通りです。<font color="red">必ず、各行動毎に、"改行"をして記入してください</font><br>
　　　　(1行目) 行動1<br>
　　　　(2行目) 行動2<br>
　　　　(3行目) 行動3<br>
　　　　・・・<br>
</span>
<hr>
</div>
</BODY>
</HTML>
!;
}

sub Print_Questionnaire {
# SUB2
# アンケートページ
print "Content-type: text/html\n\n";
print qq!
<HTML>
<HEAD>
  <META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
  <TITLE>
アンケートに回答する
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
ユーザ: $user_name &nbsp;&nbsp; 
<a href='./top.cgi'>Topページ</a> &nbsp;&nbsp; 
<hr>
</div>

<CENTER>
<FORM ACTION="makeQuestionnaire.cgi" METHOD="POST">
<TABLE>
<font size=4>
<h2>
<span class="line-space">
アンケートに回答する <br>
</span></h2>
<br>
!;

$service =~ s/<br>/ /g;
$question_num = 1; # 設問1
print qq!
<tr><td><B>
 【$question_num】
  </B></td><td><b>訪問した店舗名</b></td></tr>
<tr><td></td><td>
  <textarea name="a1" 
     style='width: 480px; height: 3.0em; font-size: 0.7em'>$service</textarea><br>
<span class="note">* 利用したサービスの名称・店舗名をご記入ください</span>
</td></tr>
!;

$question_num += 1; # 設問2
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
  【$question_num】</B></td>
<td><b>訪問時刻</b></td></tr>
<tr><td></td><td>
<span class="note">
* 現在の時刻: $time</span>
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

$question_num += 1;  # 設問3
print qq!    
</select>
</td></tr>
!;
  print "<tr><td><B>
          【$question_num】</B></td><td><b>
              訪問した人数</b></td></tr>\n";
  print "<tr><td></td><td>\n";
  print "<select 
            name='a3' style='width: 480px; font-size: 0.7em'>\n";
  print "<option value='1'>1人</option>\n";
  print "<option value='2'>2人</option>\n";
  print "<option value='3'>3人</option>\n";
  print "<option value='4-6'>4-6人</option>\n";
  print "<option value='7-9'>7-9人</option>\n";
  print "<option value='10人以上'>10人以上</option>\n";
  print "</select>\n";
  print "</td></tr>\n";

$question_num += 1;  # 設問4
print qq!    
</select>
</td></tr>
!;
  print "<tr><td><B>
          【$question_num】</B></td><td><b>
              対象店舗の利用回数</b></td></tr>\n";
  print "<tr><td></td><td>\n";
  print "<select 
            name='a4' style='width: 480px; font-size: 0.7em'>\n";
  print "<option value='初めて'>初めて</option>\n";
  print "<option value='2回目'>2回目</option>\n";
  print "<option value='3回目'>3回目</option>\n";
  print "<option value='4-6回目'>4-6回目</option>\n";
  print "<option value='7-9回目'>7-9回目</option>\n";
  print "<option value='10回目以上'>10回目以上</option>\n";
  print "</select>\n";
  print "</td></tr>\n";

$question_num += 1; # 設問5
print qq!    
<tr><td><B>【$question_num】</B></td><td><b>対象店舗への事前の期待度</b></td></tr>
<tr><td></td><td>
<select name="a5" style='width: 480px; font-size: 0.7em'>
<optgroup label="非常に期待していた">
 <option value="+3">+3</option>
 <option value="+2">+2</option>
 <option value="+1">+1</option>
</optgroup>
<optgroup>
 <option value="±0" selected>±0: どちらともいえない</option>
</optgroup>
<optgroup>
 <option value="-1">-1</option>
 <option value="-2">-2</option>
 <option value="-3">-3</option>
</optgroup>
<optgroup label="全く期待していなかった">
</optgroup>
</select>
</td></tr>
!;

$question_num += 1; # 設問6
print qq!
<tr><td><B>
  【$question_num】</B></td><td><b>
発生した行動の満足度とコメント<br></b></tr>
<tr><td></td><td>
<span class="note"> * なにか<b>満足した行動</b>があった場合、<b>高い評価</b>を付けてください<br>
<span class="note"> * なにか<b>不満足な行動</b>があった場合、<b>低い評価</b>を付けてください<br>
<span class="note"> * もしその評価に関してなにか<b>理由</b>がある場合は、<b><u>その理由も記載</u></b>してください<br>
* <b>特筆すべき点がない場合</b>は無理に評価・コメントをする必要はありません。<br>回答欄をそのままにして次の項目に移ってください。<br></span>
<span class="note">　</span>
</td></tr>
!;

@process = split(/<br>/,$process);
for($i=0;$i<=$#process;$i++){
  print "<tr><td></td><td>\n";
  print "<span class='note'><b>$process[$i]</b> に対する満足度とコメント</span><br>\n";
  print "<select name='a6-1_$i' style='width: 480px; font-size: 0.7em'>\n";
  print "<optgroup label='非常に満足'>\n";
  print " <option value='+3'>+3</option>\n";
  print " <option value='+2'>+2</option>\n";
  print " <option value='+1'>+1</option>\n";
  print "</optgroup>\n";
  print "<optgroup>\n";
  print " <option value='±0' selected>±0: どちらともいえない</option>\n";
  print "</optgroup>\n";
  print "<optgroup>\n";
  print " <option value='-1'>-1</option>\n";
  print " <option value='-2'>-2</option>\n";
  print " <option value='-3'>-3</option>\n";
  print "</optgroup>\n";
  print "<optgroup label='非常に不満'>\n";
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

$question_num += 1; # 設問7
print qq!
<tr><td><B>【$question_num】</B></td><td><b>使用金額</b></td></tr>
<tr><td></td><td>
!;
# 円: 000000
#    for($i=1; $i<7; $i++){
#	print "<select name='a7_$i' style='font-size: 0.7em'>\n";
#	for($j=0; $j<10; $j++){
#	    print "<option value='$j'>$j</option>\n";
#	}
#	print "</select>\n";
#    }
# print qq!
#<b>円</b><br>
# 円: 000,000
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
<b>円</b><br>
<span class="note"> * 飲食業: 1人当たり(平均)</span>
</td></tr>
!;

$question_num += 1; # 設問8
print qq!    
<tr><td><B>【$question_num】</B></td><td><b>事前の期待に対する利用後の評価</b></td></tr>
<tr><td></td><td>
<select name="a8" style='width: 480px; font-size: 0.7em'>
<optgroup label="想定を上回るサービス提供">
 <option value="+3">+3</option>
 <option value="+2">+2</option>
 <option value="+1">+1</option>
</optgroup>
<optgroup>
 <option value="±0" selected>±0: 想定通りのサービス提供</option>
</optgroup>
<optgroup>
 <option value="-1">-1</option>
 <option value="-2">-2</option>
 <option value="-3">-3</option>
</optgroup>
<optgroup label="想定を下回るサービス提供">
 <option value="わからない">わからない(評価できない)</option>
</optgroup>
</select>
</td></tr>
!;

$question_num += 1; # 設問9, V-a9
print qq!    
<tr><td><B>【$question_num】</B></td><td><b>利用全体の総合満足度</b>
</td></tr>
<tr><td></td><td>
<select name="a9" style='width: 480px; font-size: 0.7em'>
<optgroup label="非常に満足">
 <option value="+3">+3</option>
 <option value="+2">+2</option>
 <option value="+1">+1</option>
</optgroup>
<optgroup>
 <option value="±0" selected>±0: どちらともいえない</option>
</optgroup>
<optgroup>
 <option value="-1">-1</option>
 <option value="-2">-2</option>
 <option value="-3">-3</option>
</optgroup>
<optgroup label="非常に不満">
</optgroup>
</select>
</td></tr>
!;
# <br><span class="note">* 全体的に友人や同僚に勧められるぐらい満足した場合に、高い評価を付けてください。</span><br>
# <span class="note">* 全体的に友人や同僚に勧められないぐらい不満足だった場合に、低い評価を付けてください。</span>

$question_num += 1; # 設問10, Var: a10
print qq!
<tr><td><B>【$question_num】</B></td><td><b>今後の再訪問意向</b></td></tr>
<tr><td></td><td>
<select name="a10" style='width: 480px; font-size: 0.7em'>
<optgroup label="このサービスはまた利用したい">
 <option value="+3">+3</option>
 <option value="+2">+2</option>
 <option value="+1">+1</option>
</optgroup>
<optgroup>
 <option value="±0" selected>±0: どちらともいえない</option>
</optgroup>
<optgroup>
 <option value="-1">-1</option>
 <option value="-2">-2</option>
 <option value="-3">-3</option>
</optgroup>
<optgroup label="このサービスはもう利用したくない">
</optgroup>
</select>
</td></tr>
!;

$question_num += 1; # 設問11, Var-a11
print qq!
<tr><td><B>【$question_num】</B></td><td><b>友人・知人への推薦意向</b></td></tr>
<tr><td></td><td>
<select name="a11" style='width: 480px; font-size: 0.7em'>
<optgroup label="このサービスの利用を友人・知人に推薦したい">
 <option value="+3">+3</option>
 <option value="+2">+2</option>
 <option value="+1">+1</option>
</optgroup>
<optgroup>
 <option value="±0" selected>±0: どちらともいえない</option>
</optgroup>
<optgroup>
 <option value="-1">-1</option>
 <option value="-2">-2</option>
 <option value="-3">-3</option>
</optgroup>
<optgroup label="このサービスの利用を友人・知人に推薦したくない">
</optgroup>
</select>
</td></tr>
!;

$question_num += 1; # 設問12
print qq!
<tr><td><B>
 【$question_num】
  </B></td><td><b>利用全体に関するコメント</b><br>
</td></tr>
<tr><td></td><td>
  <textarea name="a12" 
     style='width: 480px; height: 3.0em; font-size: 0.7em'></textarea><br><span class="note">* 今回のサービス利用全体に関してなにかコメントがあればご記入ください</span>
</td></tr>
!;

print qq!
</font>
</TABLE>
<br>
   <P>
     <INPUT TYPE="hidden" NAME="count" VALUE="$count">
     <INPUT TYPE="hidden" NAME="number" VALUE="$number">
     <INPUT TYPE="submit" NAME="complete" VALUE="回答内容を送信" style="font-size: 1em">
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
    print "ユーザ : $user_name &nbsp;&nbsp;";
    print "<a href='./top.cgi'>Topページ</a><hr>";
    print "</div>";
}

# サービスの初回利用か、繰り返し利用可の判別
sub DivideFirst
{
    print "Content-type: text/html\n\n";
    print qq!
	<html>
	 <head>
	  <META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
	  <titel>初めての利用 or 複数の利用</title>
	 </head>
	 <body>
	  <form action="makeQuestionnaire.cgi" method="post">
	  初めての利用<INPUT TYPE="submit" NAME="first" VALUE="1"><br>
	  初めてではない<INPUT TYPE="submit" NAME="first" VALUE="2"><br>
	  </form>
	 </body>
	</html>
	!;
    exit;
}

# エラーページの表示 
sub Print_Error
{
	my($error) = @_;
	print "Content-type: text/html\n\n";
	print qq!
	<HTML>
	<HEAD>
		<META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
		<TITLE>エラーが発生しました</TITLE>
	</HEAD>
	<BODY>
		<BR>
		<B>エラーが発生しました</B>
		<P>
		$error<BR>
		<P>
		サイト運営者にお問い合せ下さい。<BR>
	</BODY>
	</HTML>
	!;
	exit;
}

#########################################################################
# 完了ページの表示 
#########################################################################
sub Print_Thanks
{
    print "Content-type: text/html\n\n";
    print qq!
<HTML>
<HEAD>
<META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
<TITLE>アンケート回答のデータ送信</TITLE>
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
<b>アンケート回答のデータ送信が完了しました。</b><br>
<b>自動的に<a href="./top.cgi">Topページ</a>へ戻ります。</b><br>
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
        my @map = ('日', '月', '火', '水', '木', '金', '土');
        return $map[$week];
    } else {
        return $week;
    }
 }
#########################################################################
