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
  push(@answer,$id); # 0: id6桁
  $in{"a1"} =~ s/[\r\n]+//g; # CR+LF／CR／LFを削除
  push(@answer,$in{"a1"}); # 1: 対象サービス名
  $in{"a2"} =~ s/[\r\n]+//g; # CR+LF／CR／LFを削除
  push(@answer,$in{"a2"}); # 2: 利用開始時間
  $in{"a3"} =~ s/[\r\n]+//g; # CR+LF／CR／LFを削除
  push(@answer,$in{"a3"}); # 3: 利用人数
  $in{"a4"} =~ s/[\r\n]+//g; # CR+LF／CR／LFを削除
  push(@answer,$in{"a4"}); # 4: 利用回数
  $in{"a5"} =~ s/[\r\n]+//g; # CR+LF／CR／LFを削除
  push(@answer,$in{"a5"}); # 5: 事前期待
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
  push(@answer,$money); # 6: 金額
  push(@answer,$in{"a8"}); # 7: 期待ギャップ
  push(@answer,$in{"a9"}); # 8: 満足
  push(@answer,$in{"a10"}); # 9: 再利用意図
  $in{"a11"} =~ s/[\r\n]+/<br>/g; # CR+LF／CR／LFを削除
  # push(@answer,$in{"a11"}); # 10: 自由欄
  push(@answer,$date);
  $processNumber = $in{"processNumber"};
  for($i=0;$i<=$processNumber;$i++){
    $eva = $in{"process_".$i}.":".$in{"a6_".$i};
    push(@answer,$eva); # 11 プロセス評価
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
    &Print_Error("ファイルの書込に失敗しました。");
  }
}else{
  &Print_List;
}

# 事前設計のList
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
  飲食店のサービス利用に対するアンケート評価サイト: 訪問前準備の評価
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
ユーザ: $user_name &nbsp;&nbsp; 
<a href='./top.cgi'>Topページ</a> &nbsp;&nbsp; 
<a href='./history-post_modify.cgi'>訪問後での訪問前準備の修正</a> &nbsp;&nbsp; 
</div>

<hr>

<form action="answer.cgi" method="POST">
<div align="left">
<br>
<p>
<input type="hidden" name="mode" value="answer">
<input type="radio" name="id" value="" checked="checked" style="display:none;">
<input type="submit" value="チェックした訪問前準備の評価をする" 
  style="font-size: 1.0em">
</p>
<br>
</div>

<table class="table" border="4">
 <tr><th>　　</th><th>訪問予定店舗名</th><th>訪問予定時刻</th><th>利用人数</th><th>利用回数</th><th>事前期待</th><th>事前チェック項目</th></tr>
 !;

  open(IN, "./user/$user_name.log") or die "Cannot open file\n";
  <IN>; # 1行 個人情報記載部分
    @data = <IN>;
  close(IN);

  open(IN2, "./answer/$user_name.log") or die "Cannot open file\n";
  <IN2>; # 1行 個人情報記載部分
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
※入力内容が反映されていない場合は、ページの更新を行なってください。
</div>
</div>
</BODY>
</HTML>
	!;
	exit;
}

sub Print_Questionnaire {
#########################################################################
# アンケートページ
#########################################################################
print "Content-type: text/html\n\n";
print qq!
<HTML>
<HEAD>
  <META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
  <TITLE>訪問後評価(チェック項目の評価)</TITLE>

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
ユーザ: $user_name &nbsp;&nbsp; 
<a href='./top.cgi'>Topページ</a> &nbsp;&nbsp; 
<a href='./history-post_modify.cgi'>訪問後での訪問前準備の修正</a>
<hr>
</div>

<CENTER>
<FORM ACTION="answer.cgi" METHOD="POST">
<TABLE>
<font size=4>
<br>
<h2>訪問後評価(チェック項目の評価)</h2>
<br>
!;

$question_num = 1; # 設問1
print qq!
<tr><td><B>
 【$question_num】
  </B></td><td><b>訪問した店舗名</b></td></tr>
<tr><td></td><td>
  <textarea name="a1" 
     style='width: 480px; height: 3.0em; font-size: 0.7em'>$subdata[1]</textarea><br>
<span class="note">* 利用したサービスの名称・店舗名の記入</span>
</td></tr>
!;

$question_num += 1; # 設問2
print qq!
<tr><td><B>
  【$question_num】</B></td><td><b>訪問した時刻</b></td></tr>
<tr><td></td><td>
  <textarea name="a2" 
     style='width: 480px; height: 3.0em; font-size: 0.7em'>$subdata[2]</textarea>
</td></tr>
!;

$question_num += 1;  # 設問3
print qq!    
<tr><td><B>
   【$question_num】</B></td><td><b>訪問した人数</b></td></tr>
<tr><td></td><td>
  <textarea name="a3" 
     style='width: 480px; height: 3.0em; font-size: 0.7em'>$subdata[3]</textarea>
</td></tr>
!;

$question_num += 1;  # 設問4
print qq!    
<tr><td><B>
   【$question_num】</B></td><td><b>対象店舗の利用回数</b></td></tr>
<tr><td></td><td>
  <textarea name="a4" 
     style='width: 480px; height: 3.0em; font-size: 0.7em'>$subdata[4]</textarea>
</td></tr>
!;

$question_num += 1; # 設問5
print qq!    
<tr><td><B>
   【$question_num】</B></td><td><b>対象店舗への事前の期待度</b></td></tr>
<tr><td></td><td>
  <textarea name="a5" 
     style='width: 480px; height: 3.0em; font-size: 0.7em' readonly>$subdata[5]</textarea><br>
<span class="note">* 事前の評価のため変更不可</span>
</td></tr>
!;

$question_num += 1; # 設問6
print qq!
<tr><td><B>
  【$question_num】</B></td><td><b>
事前チェック項目の満足度<br></b></td></tr>
!;
@process = split(/<br>/,$subdata[6]);
for($i=0;$i<=$#process;$i++){
  print "<tr><td></td><td>\n";
  print "<span class='note'><b>$process[$i]</b> に対する満足度</span><br>\n";
  print "<select name='a6_$i' style='width: 480px; font-size: 0.7em'>\n";
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
    for($i=1; $i<6; $i++){
	print "<select name='a7_$i' style='font-size: 0.7em'>\n";
	for($j=0; $j<10; $j++){
	    print "<option value='$j'>$j</option>\n";
	}
	print "</select>\n";
    }
print qq!
<b>円</b>
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
</optgroup>
</select>
</td></tr>
!;

$question_num += 1; # 設問9
print qq!    
<tr><td><B>【$question_num】</B></td><td><b>利用後の全体的な満足度</b></td></tr>
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

$question_num += 1; # 設問10
print qq!
<tr><td><B>【$question_num】</B></td><td><b>これから先の再利用意向</b></td></tr>
<tr><td></td><td>
<select name="a10" style='width: 480px; font-size: 0.7em'>
<optgroup label="また利用したい">
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
<optgroup label="もう利用したくない">
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
     <INPUT TYPE="submit" NAME="complete" VALUE="訪問後評価を送信" style="font-size: 1em">
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
  print "ユーザ : $user_name　";
  print "<a href='./top.cgi'>Topページ</a>";
  print "<hr>";
  print "</div>";
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

# 完了ページの表示 
sub Print_Thanks
{
    print "Content-type: text/html\n\n";
    print qq!
<HTML>
<HEAD>
<META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
<TITLE>訪問後評価の送信</TITLE>
</HEAD>
<BODY>
<BR>
<center>
<br>
<b>訪問後評価の送信が完了しました。</b>
<br>
<b>自動的に<a href="./top.cgi">Topページ</a>へ戻ります。</b>
<br>
<meta http-equiv="refresh" content=" 2 ;url= ./top.cgi"> 
</center>
		<P>
	</BODY>
	</HTML>
	!;
	exit;
}


