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
    @data = <IN>;
    close(IN);
    if($data[0] =~ /1/){
	$maxindex = @data - 1;
	@subdata = split(/\t/,$data[$maxindex]);
	$id_answer = $subdata[0] + 1;
    }else{
    $id_answer = 1;
    }
# store dir name ---------------------------------------------------------------------------
    @script_url = split(/\//,$ENV{"SCRIPT_NAME"});
    $store_region = $script_url[3].$script_url[4].$script_url[5].$script_url[6]; 
    $store_address = $script_url[3].$script_url[4].$script_url[5].$script_url[6].$script_url[7]; 
    open(DATA, "../storelist_$store_region.dat") or die "cannot open the file\n";
    @data = <DATA>;
    close(DATA);
     foreach(@data){
	 chomp($_);
	 @subdata = split(/\t/, $_);
	 if($subdata[0] =~ /$store_address/){
	     $store_name = $subdata[3];
	 }
     }
# date ---------------------------------------------------------------------------
	my($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
	$year += 1900;
	$mon += 1;
	my($date) = sprintf("%04d/%02d/%02d %02d:%02d:%02d",$year,$mon,$mday,$hour,$min,$sec);
# first time or more than 2nd time? -----------------------------------------------
    unless($in{'first'}=="3"){
    $i = $user_name.".dat";
    open(DATE, "../../../../../user/$i") or die "can not open file\n";
    @data = <DATE>;
    close(DATE);
    $count = 0; # first or not
    foreach(@data){
	chomp($_);
	@subdata = split(/\t/,$_);
	if($subdata[0] =~ /$store_address/){
	    $count += 1;
	}else{
	    $count += 0;
	}
    }
# in the case of first evaluation, 対象店舗の利用が初めてか、そうでないかを判別
    if($count == 10){#こちらに流さない
	if($in{'first'}=="1"){
	    $count = 0;
	}elsif($in{'first'}=="2"){
	    $count = 1;
	}else{
	&DivideFirst();
        }
    }else{}
}
# in the case of putting ANSER  
    if($in{"answer"}){
	push(@answer,$id_answer);
	push(@answer,$in{"a1"});
	push(@answer,$store_name);
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
	push(@answer,$date);
	if(open(OFILE,">>answer.log")){
	   print OFILE join("\t",@answer)."\n";
	   close(OFILE); 
# idividual data
	   open(IND, ">>../../../../../user/$user_name.log");
	   print IND join("\t",@answer)."\n";
	   close(IND); 
# transform char to num
			&ToNum; #アンケートの結果をデータファイルに変換(evaluation_number.dat)
			&SubData; #数字に置換したデータを利用回数ごとに区分(data_$i.dat)
			&MeanVariance; #利用回数区分データ(data_$i.dat)の平均と分散をとり同一ファイル(data_figure.gp)にまとめる
			system "/home/msdhss/bin/gnuplot 'figure.gp'"; # gnuplotのbatchファイルの実行gnuplotの場所を絶対パスで指定
			&Print_Thanks; #アンケートの完了ページの出力でプログラムの終了	
		} else {
			&Print_Error("ファイルの書込に失敗しました。");
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
div#container{width: 750px; margin-left: auto; margin-right: auto; font-size: 2.5em}
div#container td {font-size: 3.5em}
div#header{width: 750px; margin-left: auto; margin-right: auto; font-size: 2.8em}
</style>
</HEAD>
<BODY>
<div id=container>
${&UserName}
<CENTER>
<FORM ACTION="evaluation.cgi" METHOD="POST">
<TABLE>
<font size=4>
<tr><td><B>【1】</B></td><td><b>利用日時</b></td></tr>
<tr><td></td><td>
<select name="a1" style="width: 400px; font-size: 0.7em">
!;
    for($i=60;$i>0;$i--){
    $t = time;
    $t -= $i*60*60*24;
    my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($t);
    $year += 1900;
    $mon += 1;
    $list_date = sprintf("%04d/%02d/%02d", $year, $mon, $mday);
print qq!
<option value="$list_date">$list_date
!;
}
    $t = time;
    my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($t);
    $year += 1900;
    $mon += 1;
    $list_date_today = sprintf("%04d/%02d/%02d", $year, $mon, $mday);
print qq!
<option value="$list_date_today" selected>$list_date_today
</select></td></tr>
<tr><td><B>【2】</B></td><td><b>使用金額</b></td></tr>
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
<tr><td><B>【3】</B></td><td><b>提供されたサービス</b></td></tr>
<tr><td></td><td>
<select name="a3" style='width: 400px; font-size: 0.7em'>
 <option value="N/A">選択してください</option>
 <option value="期待をかなり上回った">期待をかなり上回った</option>
 <option value="期待をやや上回った">期待をやや上回った</option>
 <option value="期待通り">期待通り</option>
 <option value="期待をやや下回った">期待をやや下回った</option>
 <option value="期待をかなり下回った">期待をかなり下回った</option>
</select>
</td></tr>
<tr><td><B>【4】</B></td><td><b>満足度</b></td></tr>
<tr><td></td><td>
<select name="a4" style='width: 400px; font-size: 0.7em'>
 <option value="N/A">選択してください</option>
 <option value="非常に満足">非常に満足</option>
 <option value="やや満足">やや満足</option>
 <option value="どちらともいえない">どちらともいえない</option>
 <option value="やや不満">やや不満</option>
 <option value="非常に不満">非常に不満</option>
</select>
</td></tr>
</font>
</TABLE>
<br>
	<P>
		<INPUT TYPE="hidden" NAME="first" VALUE="3">
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
    print "<a href='../../../../../mobile_top.cgi'>Top</a><hr>";
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
<TITLE>ご回答ありがとうございました。</TITLE>
</HEAD>
<BODY>
<BR>
<center>
<br>
<b>評価データの送信が完了しました。</b>
<br>
<b>自動的に<a href="../../../../../mobile_top.cgi">HP</a>へ戻ります。</b>
<br>
<meta http-equiv="refresh" content=" 2 ;url= ../../../../../mobile_top.cgi"> 
</center>
		<P>
	</BODY>
	</HTML>
	!;
	exit;
}
# アンケート結果を数字に置換  ---------------------------------------------------------------------------
sub ToNum
{
# i/o file open
    open(IN, "evaluation.log") or die "can not open file\n"; # initial 処理いる
    open(OUT, ">evaluation.dat") or die "can not open file for writing\n"; # initial 処理不要
    open(FIG, ">>evaluation_number.dat") or die "can not open file for writing\n"; # evaluation_number.datもintial処理が
# User file open
    $i = $user_name.".dat";
    open(USER, ">>../../../../../user/$i") or die "can not open file for writing\n"; # initial 処理いる
#
# management
#
    $,="\t"; #printf の文字区切りを半角spaceに
    $total_number = 0; #総評価数のカウント
# evaluatio.log を @dat に収納
    while(<IN>){
	$total_number += 1;
	chomp;
	@dat=split(/\t/);
	print OUT $user_name, $dat[0], $dat[1], $dat[2], $dat[3],$dat[4], $dat[5], $dat[6], $dat[7], "\n";
    }
# ディレクトリ名の獲得
    @script = split(/\//,$ENV{"SCRIPT_NAME"});
    $store_address = $script[3].$script[4].$script[5];
# total_evaluation_number.dat の作成
    open(TOTALIN, "../total_evaluation_number.dat"); #全ての店舗名と評価数のファイル
    @data = <TOTALIN>;
    close (TOTALIN);
    open(TOTALOUT, ">../total_evaluation_number.dat"); 
    foreach(@data){
	chomp($_);
	@subdata = split(/\t/, $_);
	if($subdata[0] =~ /$store_address/){ 
	    print TOTALOUT "$store_address\t$total_number\n";
	}else{
	    print TOTALOUT  "$subdata[0]\t$subdata[1]\n";
	}
    }
    close(TOTALOUT);
# comment.dat の作成
    open(COMMENT, ">>./comment.dat");
    print COMMENT $user_name, $dat[0], $dat[5], $dat[6], "\n";
    close(COMMENT);
# evaluation.dat を図で表示するために数値データに置換する操作が必要。perl で置換する
    print FIG "$user_name\t";
    print USER "$script_url[3]$script_url[4]$script_url[5]\t";
## Question 1: a number of timesradio
    if(!$dat[0]){
	$subdat = "\t";
    }elsif($dat[0]=~/回目/){
	$subdat = "1\t";
    }elsif($dat[0]=~/2回から4回/){
	$subdat = "2\t";
    }elsif($dat[0]=~/5回から7回/){
	$subdat = "3\t";
    }elsif($dat[0]=~/8回から10回/){
	$subdat = "4\t";
    }elsif($dat[0]=~/11回から13回/){
	$subdat = "5\t";
    }elsif($dat[0]=~/14回以上/){
	$subdat = "6\t";
    }else{
	$subdat = "\t";
    }
    print FIG $subdat;
    print USER $subdat;
## Question 2: 期待
			if(!$dat[1]){
			    print FIG "\t";
			    print USER "\t";
			}elsif($dat[1]=~/非常に期待/){
			    print FIG "5\t";
			    print USER "5\t";
			}elsif($dat[1]=~/やや期待/){
			    print FIG "4\t";
			    print USER "4\t";
			}elsif($dat[1]=~/どちらとも/){
			    print FIG "3\t";
			    print USER "3\t";
			}elsif($dat[1]=~/あまり期待/){
			    print FIG "2\t";
			    print USER "2\t";
			}else{
			    print FIG "1\t";
			    print USER "1\t";
			}
## Question 3: cost
			if(!$dat[2]){
			    print USER "\t";
			}elsif($dat[2]=~/500以下/){
			    print USER "500以下\t";
			}elsif($dat[2]=~/500円から1000円/){
			    print USER "500円から1000円\t";
			}elsif($dat[2]=~/1000円から1500円/){
			    print USER "1000円から1500円\t";
			}elsif($dat[2]=~/1500円から2000円/){
			    print USER "1500円から2000円\t";
			}elsif($dat[2]=~/2000円以上/){
			    print USER "2000円以上\t";
			}else{
			    print USER "\t";
			}
## Question 4;　Degree of Satisfaction 
			if(!$dat[3]){
			    print FIG "\t";
			    print USER "\t";
			}elsif($dat[3]=~/非常に満足/){
			    print FIG "5\t";
			    print USER "5\t";
			}elsif($dat[3]=~/やや満足/){
			    print FIG "4\t";
			    print USER "4\t";
			}elsif($dat[3]=~/どちらとも/){
			    print FIG "3\t";
			    print USER "3\t";
			}elsif($dat[3]=~/やや不満/){
			    print FIG "2\t";
			    print USER "2\t";
			}else{
			    print FIG "1\t";
			    print USER "1\t";
			}
## Question 5: Degree of modefied expectationradio
			if(!$dat[4]){
			    $subdat = "\t";
			}elsif($dat[4]=~/期待をかなり上回った/){
			    $subdat = "2\t";
			}elsif($dat[4]=~/期待をやや上回った/){
			    $subdat = "1\t";
			}elsif($dat[4]=~/期待通りであった/){
			    $subdat = "0\t";
			}elsif($dat[4]=~/期待をやや下回った/){
			    $subdat = "-1\t";
			}else{
			    $subdat = "-2\t";
			}
                        print FIG $subdat;
                        print USER $subdat;
## Question 6: Comment
			print FIG "$dat[5]\t";
			print USER "$dat[5]\t";
## date 2000-00-00 -
			print FIG "$dat[6]\n";
			print USER "$dat[6]\n";
# i/o file close
    close(IN);
    close(OUT);
    close(FIG);
    close(USER);
}
################################################
## 数値化したデータを回数別ファイルに分ける
################################################
sub SubData
{
# input
    open(IN, "evaluation_number.dat") or die "can not open file\n";
    @data = <IN>; 
    close(IN); 
# output
    for($i=1;$i<7;$i++){
	$j = "OUT".$i;
	$k = "data_".$i.".dat";
    open($j, ">$k"); # 1 .. 6 file open
    }
    foreach(@data){
	chomp($_);
   	@subdata = split(/\t/, $_);
    for($i=1;$i<7;$i++){
	$j = "OUT".$i;
	$k = "data_".$i.".dat";
        if($subdata[1] =~ /$i/){
	print $j $subdata[0],$subdata[2],$subdata[4],$subdata[3],$subdata[5],$subdata[6],"\n";
    }else{}
    }
    }
    for($i=1;$i<7;$i++){
	$j = "OUT".$i;
    close($j);
    }
}
##########################################################
## 時間の5区分毎に期待、期待とのズレ、満足度の平均分散をとる
########################################################
sub MeanVariance
{
# output
    open(OUT,">data_figure.gp");
# i番目のデータ処理
    for($i=1;$i<7;$i++){ 
# var initialize
	for($k=1;$k<4;$k++){
	    $count[$k] = 0;
	    $x[$k] = 0;
	    $x_x[$k] = 0;
	    $mean[$k] = 0;
	    $mean_upper[$k] = 0;
	    $mean_lower[$k] = 0;
	    $mean_mean[$k] = 0;
	    $sd[$k] = 0;
	}
	$j = "IN".$i;
	$k = "data_".$i.".dat";
	open($j, "$k") or die "can not open file for writing\n"; # 1 .. 6 file open
	@data = <$j>; # i file load    
	close($j);
	foreach(@data){
	    chomp($_);
	    @subdata = split(/\t/, $_);
	        if(!$subdata[1] and !$subdata[2]){
                }else{
		    $subdata[2] += $subdata[1]; 
		} 
	    for($k=1;$k<4;$k++){ # k1:ex k2:mev k3:cs 
		if(!$subdata[$k]){ # number of data
		$count[$k] += 0; 
		}else{
		$count[$k] += 1;
	        }
		if(!$subdata[$k]){
		    $x[$k] +=  0;
		    $x_x[$k] += 0;
		}else{
		$x[$k] +=  $subdata[$k];
		$x_x[$k] += $subdata[$k]*$subdata[$k]; # square
	        }
	    }
	}
	# 平均を取る(0で割るとエラーが出る)
	for($k=1;$k<4;$k++){
	    if(!$count[$k]){
		$mean[$k] = 0;
		$mean_mean[$k] = 0;
	    }else{
	    $mean[$k] = $x[$k]/$count[$k];
	    $mean_mean[$k] = $x_x[$k]/$count[$k];
	    $sq[$k] = sqrt($mean_mean[$k]-$mean[$k]*$mean[$k]);
	    $mean_upper[$k] = $mean[$k] + $sq[$k];
	    $mean_lower[$k] = $mean[$k] - $sq[$k];
	    }
	}
	$i_1=$i-0.28;
	$i_2=$i+0.28;
	print OUT $i, $i_1, $i_2, $count[1], $count[2], $count[3], $mean[1], $mean_upper[1], $mean_lower[1],$mean[2], $mean_upper[2], $mean_lower[2],$mean[3], $mean_upper[3], $mean_lower[3],"\n";
    }
    close(OUT);
}
#------------------ おしまい --------------------------------------------------
