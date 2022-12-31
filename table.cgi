#!/usr/bin/perl

# .../adhocQuestionnaire2022_JP_prototype/table.cgi

require "cgi-lib.pl";
require "jcode.pl";
&ReadParse; # related to cgi-lib.pl

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

&Print_List;

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
サービス利用に対するアンケート調査サイト: 回答状況の確認</TITLE>
<style type="text/css">
table {width: 880px; font-size: 0.8em; text-align: center;}
div#container {width: 880px; margin-left: auto; margin-right: auto; font-size: 1.5em}
</style>
</HEAD>

<BODY>
<div id="container">

<br>
<h4> $time 時点のアンケート調査回答状況</h4>
<h4> 回答者全員(テストユーザ含む)の合計回答数: 
  !;
    &Count;
    print qq!
</h4>
<br>

<table class="table" border="4">
 <tr><th>ユーザ名</th><th>回答数</th></tr>
 !;
    &Log;
    print qq!
</table>

<br>
<hr>

</div>
</BODY>
</HTML>
	!;
	exit;
}

sub Count {
open(IN, "./usrman/.users") or die "Cannot open file\n";
  @data = <IN>;
close(IN);
$count = 0; 
  foreach(@data){
    chomp($_);
    @subdata = split(/:/,$_);
    $name = $subdata[0].".log";
    open(IN1,"./private/answer/$name") or die "Cannot open file\n";
    @answer = <IN1>;
    close(IN1);
    $count += $#answer;
  }
    print "$count";
}

sub Log {
open(IN, "./usrman/.users") or die "Cannot open file\n";
  @data = <IN>;
close(IN);
  foreach(@data){
    chomp($_);
    @subdata = split(/:/,$_);
    $name = $subdata[0].".log";
    open(IN1,"./private/answer/$name") or die "Cannot open file\n";
    @answer = <IN1>;
    close(IN1);

    print "<tr><td>$subdata[0]</td><td>$#answer</td></tr>\n";
  }
}
