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
	push(@answer,$id); #id6桁
	push(@answer,$in{"a1"}); #評価時点
	push(@answer,$store_address); #評価店舗コード
	push(@answer,$store_name); #評価店舗名
	push(@answer,$in{"initial"}); #利用回数の初期条件
	push(@answer,$in{"count"}); #トータル評価数
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
			&Print_Error("ファイルの書込に失敗しました。");
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
# アンケートページの HTML -------------------------------------------------
#--------------------------------------------------------------------------
print "Content-type: text/html\n\n";
#タイトル
print qq!
<HTML>
<HEAD>
	<META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
	<TITLE>$store_nameの評価</TITLE>
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
<tr><td><B>【$question_num】</B></td><td><b>サービス利用/使用日時</b></td></tr>
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
	print "<tr><td><B>【$question_num】</B></td><td><b>評価店舗の利用回数</b></td></tr>\n";
	print "    <tr><td></td><td>\n";
	print "    <select name='initial' style='width: 480px; font-size: 0.7em'>\n";
	print "<option value='N/A'>選択してください</option>\n";
	print "<option value='初めて'>初めて</option>\n";
	print "<option value='2-4回目'>2-4回目</option>\n";
	print "<option value='5-7回目'>5-7回目</option>\n";
	print "<option value='8-10回目'>8-10回目</option>\n";
	print "<option value='11回目以上'>11回目以上</option>\n";
	print "</select>\n";
	print "</td></tr>\n";
    }else{
	print "<INPUT TYPE='hidden' NAME='initial' VALUE='$initial'>\n";
    }
$question_num += 1;
print qq!    
<tr><td><B>【$question_num】</B></td><td><b>使用金額</b></td></tr>
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
<b>円</b>
</td></tr>
!;
$question_num += 1;
print qq!    
<tr><td><B>【$question_num】</B></td><td><b>利用/使用前の期待</b></td></tr>
<tr><td></td><td>
<select name="a3" style='width: 480px; font-size: 0.7em'>
 <option value="N/A">選択してください</option>
<optgroup label="非常に期待していた">
 <option value="+3">+3</option>
 <option value="+2">+2</option>
 <option value="+1">+1</option>
</optgroup>
<optgroup>
 <option value="±0">±0: どちらともいえない</option>
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
$question_num += 1;
print qq!    
<tr><td><B>【$question_num】</B></td><td><b>提供されたサービス</b></td></tr>
<tr><td></td><td>
<select name="a4" style='width: 480px; font-size: 0.7em'>
 <option value="N/A">選択してください</option>
<optgroup label="予想を非常に上回った">
 <option value="+3">+3</option>
 <option value="+2">+2</option>
 <option value="+1">+1</option>
</optgroup>
<optgroup>
 <option value="±0">±0: 予想通り</option>
</optgroup>
<optgroup>
 <option value="-1">-1</option>
 <option value="-2">-2</option>
 <option value="-3">-3</option>
</optgroup>
<optgroup label="予想を非常に下回った">
</optgroup>
</select>
</td></tr>
!;
$question_num += 1;
print qq!    
<tr><td><B>【$question_num】</B></td><td><b>利用/使用後の満足度</b></td></tr>
<tr><td></td><td>
<select name="a5" style='width: 480px; font-size: 0.7em'>
 <option value="N/A">選択してください</option>
<optgroup label="非常に満足">
 <option value="+3">+3</option>
 <option value="+2">+2</option>
 <option value="+1">+1</option>
</optgroup>
<optgroup>
 <option value="±0">±0: どちらともいえない</option>
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
$question_num += 1;
print qq!
<tr><td><B>【$question_num】</B></td><td><b>コメント</b></td></tr>
<tr><td></td><td>
<textarea name="a6" style='width: 480px; font-size: 0.7em'></textarea>
</td></tr>
</font>
</TABLE>
<br>
	<P>
		<INPUT TYPE="hidden" NAME="count" VALUE="$count">
		<INPUT TYPE="hidden" NAME="number" VALUE="$number">
		<INPUT TYPE="submit" NAME="answer" VALUE="評価を送信" style="font-size: 1em">
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
    print "ユーザ : $user_name　";
    print "<a href='../../../../../top.cgi'>Top</a><hr>";
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
	  <form action="evaluation.cgi" method="post">
	  初めての利用<INPUT TYPE="submit" NAME="first" VALUE="1"><br>
	  初めてではない<INPUT TYPE="submit" NAME="first" VALUE="2"><br>
	  </form>
	 </body>
	</html>
	!;
    exit;
}
#
# エラーページの表示 
#
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
# 完了ページの表示 ---------------------------------------------------------------------------
sub Print_Thanks
{
    print "Content-type: text/html\n\n";
    print qq!
<HTML>
<HEAD>
<META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
<TITLE>データの送信</TITLE>
</HEAD>
<BODY>
<BR>
<center>
<br>
<b>評価データの送信が完了しました。</b>
<br>
<b>自動的に<a href="../../../../../top.cgi">Topページ</a>へ戻ります。</b>
<br>
<meta http-equiv="refresh" content=" 2 ;url= ../../../../../top.cgi"> 
</center>
		<P>
	</BODY>
	</HTML>
	!;
	exit;
}

