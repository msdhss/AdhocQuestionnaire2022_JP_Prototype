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
<TITLE>回答項目の削除</TITLE>
<style type="text/css">
a {color: #017acd}
table {width: 800px; font-size: 0.8 em; text-align: center;}
div#container {width: 880px; margin-left: auto; margin-right: auto; font-size: 1.5em}
</style>
</HEAD>

<BODY>
<div id="container">
<div id="header">
ユーザ: $user_name &nbsp;&nbsp; 
<a href='./top.cgi'>Topページ</a>&nbsp;&nbsp;  
<a href='./history.cgi'>回答内容の確認</a>
</div>
<hr>
<form action="history_delete.cgi" method="POST">

<div align="left">
<br>
<p>
<input type="hidden" name="mode" value="del">
<input type="submit" value="チェックした項目を削除する" style="font-size: 1.0em">
</p>
<br>
</div>

<table class="table" border="4">
 <tr><th>　</th><th>訪問店舗名</th><th>訪問時刻</th><th>利用人数</th><th>利用回数</th><th>事前期待</th><th>期待とのギャップ</th><th>総合満足度</th><th>再訪問意向</th><th>推薦意向</th><th>使用金額</th></tr>
 !;
    open(IN, "./answer/$user_name.log") or die "Cannot open file\n";
    <IN>; # 1行 個人情報記載部分
    @data = <IN>;
    close(IN);
    @data = reverse(@data);
    foreach(@data){
	chomp($_);
	@subdata = split(/\t/, $_);
	print "<tr><td><input type='radio' name='id' value='$subdata[1]' style='width: 35pt; height: 35pt'></td><td>$subdata[2]</td><td>$subdata[3]</td><td>$subdata[4]</td><td>$subdata[5]</td><td>$subdata[6]</td><td>$subdata[8]</td><td>$subdata[9]</td><td>$subdata[10]</td><td>$subdata[11]</td><td>$subdata[7]円</td></tr>\n";
    }
    print qq!
</form>
</table>
<br>
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

# 完了ページの表示 
sub Print_Thanks
{
    print "Content-type: text/html\n\n";
    print qq!
<HTML>
<HEAD>
<META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
<TITLE>回答項目の削除</TITLE>
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
<b>チェックした回答項目の削除が完了しました。</b><br>
<b>自動的に<a href="./history_delete.cgi">回答項目の削除ページ</a>へ戻ります。</b><br>
</span>
<meta http-equiv="refresh" content=" 2 ;url= ./history_delete.cgi"> 
</center>
		<P>
	</BODY>
	</HTML>
	!;
	exit;
}
