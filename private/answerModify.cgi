#!/usr/bin/perl
require "cgi-lib.pl";
require "jcode.pl";

&ReadParse; # related to cgi-lib.pl
$user_name = $ENV{'REMOTE_USER'};

# Delete
if($in{'mode'} eq "del"){
    if($in{'id'}){ 
    $delid = $in{'id'};
    open(IN, "./user/$user_name.log") or die "cannno open\n";
    @data = <IN>;
    close(IN);
    $i = 0;
    foreach(@data){
	chomp $_;
	@subdata = split(/\t/, $_);
	$id_data[$i] = $subdata[0];
	$i++;
    }
    open(IN, "./user/$user_name.log") or die "cannno open\n";
    @data = <IN>;
    close(IN);
    open(OUT, ">./user/$user_name.log");
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
}
}
&Print_Thanks;
# 
sub Print_Thanks
{
    print "Content-type: text/html\n\n";
    print qq!
<HTML>
<HEAD>
<META Http-Equiv="Content-Type" Content="text/html;charset=EUC-JP">
<TITLE>サービスに対するアンケート調査評価サイト: 事前アンケートの修正</TITLE>
<style type="text/css">
a {color: #017acd}
table {width: 800px; font-size: 0.8 em; text-align: center;}
div#container {width: 880px; margin-left: auto; margin-right: auto; font-size: 1.5em}
</style>
</HEAD>
<BODY>
<div id="container">
<div id="header">
User: $user_name &nbsp;&nbsp; 
<a href='../top.cgi'>Top</a>
　　　　　　　
<a href='./answerList.cgi'>Back</a>
</div>
<hr>
<form action="answerModify.cgi" method="POST">
<div align="left">
<p>
<input type="hidden" name="mode" value="del">
<input type="submit" value="チェックした項目を削除する" style="font-size: 0.7em">
</p>
</div>
<table class="table" border="4">
 <tr><th>　　</th><th>id</th><th>店舗名</th><th>開始時間</th><th>利用回数</th><th>期待</th><th>プロセス</th><th>入力時間</th></tr>
 !;
    open(IN, "./user/$user_name.log") or die "Cannot open file\n";
    <IN>; # 1行 個人情報記載部分
    @data = <IN>;
    close(IN);
    @data = reverse(@data);
    foreach(@data){
	chomp($_);
	@subdata = split(/\t/, $_);
	print "<tr><td><input type='radio' name='id' value='$subdata[0]' style='width: 35pt; height: 35pt'></td><td>$subdata[1]</td><td>$subdata[2]</td><td>$subdata[3]</td><td>$subdata[4]</td><td>$subdata[5]</td><td>$subdata[6]</td><td>$subdata[7]</td></tr>\n"
    }
    print qq!
</form>
</table>
<hr>
</div>
</BODY>
</HTML>
	!;
	exit;
}

